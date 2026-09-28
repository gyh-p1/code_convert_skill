/*
 * Known differences from the original BSD du(1) on Windows (MinGW/UCRT64):
 * - fts(3) is not available; a recursive directory traversal using
 *   <filesystem> is implemented instead.  The order of entries and handling
 *   of some edge cases (e.g., directory cycles) may differ.
 * - SIGINFO and the interactive progress feature are not supported on
 *   Windows; the signal handler is not installed.
 * - The -n option (ignore nodump) has no effect because Windows does not
 *   provide st_flags / UF_NODUMP.
 * - st_blocks is not available; file size is used and converted to 512-byte
 *   blocks by rounding up.  This may cause slight numeric differences in
 *   reported block counts.
 * - Hard link detection (-l to disable) is not performed on Windows because
 *   (st_dev, st_ino) is not reliable.  Files with multiple hard links will be
 *   counted multiple times.
 * - The -x option is approximated by comparing drive letters of paths; it
 *   does not handle mounted volumes on the same drive.
 * - expand_number and humanize_number are reimplemented with basic support
 *   for common suffixes; the formatting may not exactly match BSD's
 *   humanize_number in all corner cases.
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cerrno>
#include <cstdint>
#include <climits>
#include <cstdarg>
#include <cctype>
#include <string>
#include <vector>
#include <filesystem>

typedef long long off_t;

#define DEV_BSIZE 512
#define UNITS_2   1
#define UNITS_SI  2
#define EX_USAGE  64

#define FTS_PHYSICAL  0x01
#define FTS_LOGICAL   0x02
#define FTS_COMFOLLOW 0x04
#define FTS_XDEV      0x08

#define howmany(x, y) (((x) + ((y) - 1)) / (y))

static int Aflag, hflag;
static long blocksize, cblocksize;
static int nodumpflag = 0;
static int rval = 0;
static int depth = INT_MAX;
static int aflag, sflag, dflag, cflag, lflag;
static int Hflag, Lflag;
static off_t threshold = 0;
static off_t threshold_sign = 1;
static int ftsoptions = FTS_PHYSICAL;
static std::vector<std::string> ignores;

static void
warnx(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fprintf(stderr, "\n");
}

static void
errx(int eval, const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fprintf(stderr, "\n");
    exit(eval);
}

static void
err(int eval, const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fprintf(stderr, ": %s\n", strerror(errno));
    exit(eval);
}

static void
usage(void)
{
    (void)fprintf(stderr,
        "usage: du [-Aclnx] [-H | -L | -P] [-g | -h | -k | -m] "
        "[-a | -s | -d depth] [-B blocksize] [-I mask] "
        "[-t threshold] [file ...]\n");
    exit(EX_USAGE);
}

static int
expand_number(const char *buf, off_t *num)
{
    char *endptr;
    errno = 0;
    long long value = strtoll(buf, &endptr, 10);
    if (errno == ERANGE)
        return -1;
    if (endptr == buf)
        return -1;
    if (*endptr != '\0') {
        char suffix = tolower((unsigned char)*endptr);
        switch (suffix) {
        case 'b': value *= 512; break;
        case 'k': value *= 1024; break;
        case 'm': value *= 1024 * 1024; break;
        case 'g': value *= 1024LL * 1024 * 1024; break;
        case 't': value *= 1024LL * 1024 * 1024 * 1024; break;
        case 'p': value *= 1024LL * 1024 * 1024 * 1024 * 1024; break;
        case 'e': value *= 1024LL * 1024 * 1024 * 1024 * 1024 * 1024; break;
        default: return -1;
        }
        endptr++;
        if (*endptr != '\0')
            return -1;
    }
    *num = value;
    return 0;
}

static bool
fnmatch_impl(const char *pat, const char *str)
{
    while (*pat) {
        if (*pat == '*') {
            pat++;
            if (!*pat)
                return true;
            while (*str) {
                if (fnmatch_impl(pat, str))
                    return true;
                str++;
            }
            return false;
        } else if (*pat == '?') {
            if (!*str)
                return false;
            pat++;
            str++;
        } else if (*pat == '[') {
            pat++;
            bool negate = false;
            if (*pat == '!' || *pat == '^') {
                negate = true;
                pat++;
            }
            bool match = false;
            while (*pat && *pat != ']') {
                if (*pat == '\\') {
                    pat++;
                    if (*pat == *str)
                        match = true;
                } else if (pat[1] == '-' && pat[2] && pat[2] != ']') {
                    char start = *pat;
                    char end = pat[2];
                    if (*str >= start && *str <= end)
                        match = true;
                    pat += 2;
                } else {
                    if (*pat == *str)
                        match = true;
                }
                pat++;
            }
            if (*pat == ']')
                pat++;
            if (match == negate)
                return false;
            if (!*str)
                return false;
            str++;
        } else {
            if (*pat != *str)
                return false;
            pat++;
            str++;
        }
    }
    return !*str;
}

static void
ignoreadd(const char *mask)
{
    ignores.push_back(mask);
}

static bool
ignorep(const std::string& name)
{
    if (nodumpflag) {
        /* Windows has no UF_NODUMP; -n is a no-op. */
    }
    for (const auto& mask : ignores) {
        if (fnmatch_impl(mask.c_str(), name.c_str()))
            return true;
    }
    return false;
}

static void
prthumanval(long long blocks)
{
    long long bytes = blocks * cblocksize;
    if (!Aflag)
        bytes *= DEV_BSIZE;

    char buf[5];
    long long divisor = 1024;
    const char *units[] = {"", "K", "M", "G", "T", "P", "E"};
    const char *si_units[] = {"", "kB", "MB", "GB", "TB", "PB", "EB"};
    if (hflag == UNITS_SI)
        divisor = 1000;

    int unit_idx = 0;
    double value = (double)bytes;
    while (value >= divisor && unit_idx < 6) {
        value /= divisor;
        unit_idx++;
    }

    if (unit_idx == 0) {
        snprintf(buf, sizeof(buf), "%lldB", bytes);
    } else {
        const char *unit_str = (hflag == UNITS_SI) ? si_units[unit_idx] : units[unit_idx];
        if (value < 10.0)
            snprintf(buf, sizeof(buf), "%.1f%s", value, unit_str);
        else
            snprintf(buf, sizeof(buf), "%.0f%s", value, unit_str);
    }
    printf("%4s", buf);
}

static long long
process_path(const std::filesystem::path& path, const std::string& name,
    int level, bool is_command_line_arg, const std::string& root_name)
{
    std::error_code ec;
    auto sym_status = std::filesystem::symlink_status(path, ec);
    if (ec) {
        warnx("%s: %s", path.string().c_str(), ec.message().c_str());
        rval = 1;
        return 0;
    }

    bool is_symlink = std::filesystem::is_symlink(sym_status);
    std::filesystem::file_status status;
    if (Lflag || (Hflag && is_command_line_arg)) {
        status = std::filesystem::status(path, ec);
        if (ec) {
            warnx("%s: %s", path.string().c_str(), ec.message().c_str());
            rval = 1;
            return 0;
        }
    } else {
        status = sym_status;
    }
    bool is_dir = std::filesystem::is_directory(status);

    if (ignorep(name))
        return 0;

    bool skip_children = false;
    if (is_dir && level > 0 && (ftsoptions & FTS_XDEV)) {
        std::string current_root = path.root_name().string();
        if (current_root != root_name)
            skip_children = true;
    }

    long long dir_blocks = 0;

    if (is_dir) {
        if (!skip_children) {
            std::filesystem::directory_iterator iter(path, ec);
            if (ec) {
                warnx("%s: %s", path.string().c_str(), ec.message().c_str());
                rval = 1;
                return 0;
            }
            for (const auto& entry : iter) {
                std::string child_name = entry.path().filename().string();
                if (child_name.empty())
                    child_name = entry.path().string();
                long long child_blocks = process_path(entry.path(), child_name,
                    level + 1, false, root_name);
                dir_blocks += child_blocks;
            }
        }

        uint64_t dir_size = 0;
        auto sz = std::filesystem::file_size(path, ec);
        if (!ec)
            dir_size = sz;
        else
            dir_size = 0;

        long long curblocks;
        if (Aflag) {
            curblocks = howmany(dir_size, cblocksize);
        } else {
            uint64_t st_blocks = howmany(dir_size, 512);
            curblocks = howmany(st_blocks, cblocksize);
        }
        dir_blocks += curblocks;

        if (level <= depth &&
            threshold <= threshold_sign * howmany(dir_blocks * cblocksize, blocksize)) {
            if (hflag > 0) {
                prthumanval(dir_blocks);
                printf("\t%s\n", path.string().c_str());
            } else {
                printf("%jd\t%s\n",
                    (intmax_t)howmany(dir_blocks * cblocksize, blocksize),
                    path.string().c_str());
            }
        }
        return dir_blocks;
    } else {
        uint64_t size = 0;
        auto sz = std::filesystem::file_size(path, ec);
        if (ec) {
            warnx("%s: %s", path.string().c_str(), ec.message().c_str());
            rval = 1;
            return 0;
        }
        size = sz;

        long long curblocks;
        if (Aflag) {
            curblocks = howmany(size, cblocksize);
        } else {
            uint64_t st_blocks = howmany(size, 512);
            curblocks = howmany(st_blocks, cblocksize);
        }

        if (aflag || level == 0) {
            if (hflag > 0) {
                prthumanval(curblocks);
                printf("\t%s\n", path.string().c_str());
            } else {
                printf("%jd\t%s\n",
                    (intmax_t)howmany(curblocks * cblocksize, blocksize),
                    path.string().c_str());
            }
        }
        return curblocks;
    }
}

int
main(int argc, char *argv[])
{
    Aflag = hflag = 0;
    blocksize = 0;
    cblocksize = DEV_BSIZE;
    nodumpflag = 0;
    depth = INT_MAX;
    aflag = sflag = dflag = cflag = lflag = 0;
    Hflag = Lflag = 0;
    threshold = 0;
    threshold_sign = 1;
    ftsoptions = FTS_PHYSICAL;
    ignores.clear();

    int i = 1;
    for (; i < argc; i++) {
        char *arg = argv[i];
        if (arg[0] != '-' || arg[1] == '\0')
            break;
        if (arg[1] == '-') {
            if (arg[2] == '\0') {
                i++;
                break;
            }
            if (strcmp(arg + 2, "si") == 0) {
                hflag = UNITS_SI;
            } else {
                usage();
            }
        } else {
            for (int j = 1; arg[j] != '\0'; j++) {
                char ch = arg[j];
                switch (ch) {
                case 'A':
                    Aflag = 1;
                    break;
                case 'B': {
                    const char *optarg = nullptr;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    errno = 0;
                    char *endptr;
                    long val = strtol(optarg, &endptr, 10);
                    if (errno == ERANGE || *endptr != '\0' || val <= 0) {
                        warnx("invalid argument to option B: %s", optarg);
                        usage();
                    }
                    cblocksize = val;
                    break;
                }
                case 'H':
                    Hflag = 1;
                    Lflag = 0;
                    break;
                case 'I': {
                    const char *optarg = nullptr;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    ignoreadd(optarg);
                    break;
                }
                case 'L':
                    Lflag = 1;
                    Hflag = 0;
                    break;
                case 'P':
                    Hflag = Lflag = 0;
                    break;
                case 'a':
                    aflag = 1;
                    break;
                case 's':
                    sflag = 1;
                    break;
                case 'd': {
                    const char *optarg = nullptr;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    dflag = 1;
                    errno = 0;
                    char *endptr;
                    long val = strtol(optarg, &endptr, 10);
                    if (errno == ERANGE || *endptr != '\0' || val < 0) {
                        warnx("invalid argument to option d: %s", optarg);
                        usage();
                    }
                    depth = val;
                    break;
                }
                case 'c':
                    cflag = 1;
                    break;
                case 'g':
                    hflag = 0;
                    blocksize = 1073741824;
                    break;
                case 'h':
                    hflag = UNITS_2;
                    break;
                case 'k':
                    hflag = 0;
                    blocksize = 1024;
                    break;
                case 'l':
                    lflag = 1;
                    break;
                case 'm':
                    hflag = 0;
                    blocksize = 1048576;
                    break;
                case 'n':
                    nodumpflag = 1;
                    break;
                case 'r':
                    break;
                case 't': {
                    const char *optarg = nullptr;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    if (expand_number(optarg, &threshold) != 0 || threshold == 0) {
                        warnx("invalid threshold: %s", optarg);
                        usage();
                    } else if (threshold < 0) {
                        threshold_sign = -1;
                    }
                    break;
                }
                case 'x':
                    ftsoptions |= FTS_XDEV;
                    break;
                case '?':
                default:
                    usage();
                }
            }
        }
    }

    std::vector<std::string> file_args;
    for (; i < argc; i++) {
        file_args.push_back(argv[i]);
    }
    if (file_args.empty()) {
        file_args.push_back(".");
    }

    if (Hflag)
        ftsoptions |= FTS_COMFOLLOW;
    if (Lflag) {
        ftsoptions &= ~FTS_PHYSICAL;
        ftsoptions |= FTS_LOGICAL;
    }

    if (!Aflag && (cblocksize % DEV_BSIZE) != 0) {
        cblocksize = howmany(cblocksize, DEV_BSIZE) * DEV_BSIZE;
    }

    if (aflag + dflag + sflag > 1)
        usage();
    if (sflag)
        depth = 0;

    if (blocksize == 0)
        blocksize = 512; /* getbsize() default in bytes */

    if (!Aflag) {
        cblocksize /= DEV_BSIZE;
        blocksize /= DEV_BSIZE;
    }

    if (threshold != 0) {
        threshold = howmany(threshold / DEV_BSIZE * cblocksize, blocksize);
    }

    rval = 0;

    long long total_blocks = 0;
    for (const auto& file_arg : file_args) {
        std::filesystem::path path(file_arg);
        std::string name = path.filename().string();
        if (name.empty())
            name = file_arg;
        std::string root_name = path.root_name().string();
        long long blocks = process_path(path, name, 0, true, root_name);
        total_blocks += blocks;
    }

    if (cflag) {
        if (hflag > 0) {
            prthumanval(total_blocks);
            printf("\ttotal\n");
        } else {
            printf("%jd\ttotal\n",
                (intmax_t)howmany(total_blocks * cblocksize, blocksize));
        }
    }

    return rval;
}
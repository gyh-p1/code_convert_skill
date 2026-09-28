/*
 * Known differences from the original BSD du(1) when built on Windows
 * with MinGW/UCRT64:
 *
 * - fts(3) is not available; a recursive directory traversal using
 *   <filesystem> is implemented instead.  The order of entries and
 *   handling of some edge cases (e.g., directory cycles) may differ.
 * - SIGINFO and the interactive progress feature are not supported on
 *   Windows; the signal handler is not installed.
 * - The -n option (ignore nodump) has no effect because Windows does not
 *   provide st_flags / UF_NODUMP.
 * - st_blocks is not available; file size is used and converted to
 *   512-byte blocks by rounding up.  This may cause numeric differences
 *   in reported block counts.
 * - Hard link detection (-l to disable) is not performed on Windows
 *   because (st_dev, st_ino) is not reliable.  Files with multiple hard
 *   links will be counted multiple times.
 * - The -x option is approximated by comparing drive letters of paths;
 *   it does not handle mounted volumes on the same drive.
 * - expand_number and humanize_number are reimplemented with basic
 *   support for common suffixes; the formatting may not exactly match
 *   BSD's humanize_number in all corner cases.
 * - Directory sizes: <filesystem>::file_size() typically fails or
 *   returns 0 for directories, while BSD st_size for directories is
 *   usually non-zero.  This implementation uses 0 as an approximation.
 * - Symbolic links: when not following links, Windows has no portable
 *   lstat(); this implementation does not follow the link and uses 0
 *   for the link's own size, whereas BSD lstat() reports the link size.
 * - Path encoding and narrow-character API behavior may differ from the
 *   original POSIX build.
 * - std::filesystem may require -lstdc++fs with older GCC versions; modern
 *   MinGW/UCRT64 GCC includes it in libstdc++.  The target build command
 *   is unchanged.
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cerrno>
#include <cstdint>
#include <climits>
#include <cstdarg>
#include <cctype>
#include <clocale>
#include <string>
#include <vector>
#include <filesystem>

using du_off_t = long long;

#define DEV_BSIZE 512
#define UNITS_2   1
#define UNITS_SI  2
#define EX_USAGE  64

#define FTS_PHYSICAL  0x01
#define FTS_LOGICAL   0x02
#define FTS_COMFOLLOW 0x04
#define FTS_XDEV      0x08

#define howmany(x, y) (((x) + ((y) - 1)) / (y))

static const char *progname = "du";
static int Aflag, hflag;
static long long blocksize, cblocksize;
static int nodumpflag = 0;
static int rval = 0;
static int depth = INT_MAX;
static int aflag, sflag, dflag, cflag, lflag;
static int Hflag, Lflag;
static du_off_t threshold = 0;
static du_off_t threshold_sign = 1;
static int ftsoptions = FTS_PHYSICAL;
static std::vector<std::string> ignores;

static void
warnx(const char *fmt, ...)
{
    va_list ap;

    fprintf(stderr, "%s: ", progname);
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fprintf(stderr, "\n");
}

static void
errx(int eval, const char *fmt, ...)
{
    va_list ap;

    fprintf(stderr, "%s: ", progname);
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fprintf(stderr, "\n");
    exit(eval);
}

static void
err(int eval, const char *fmt, ...)
{
    int e = errno;
    va_list ap;

    fprintf(stderr, "%s: ", progname);
    va_start(ap, fmt);
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fprintf(stderr, ": %s\n", strerror(e));
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
expand_number(const char *buf, du_off_t *num)
{
    char *endptr;
    long long value;
    long long factor;

    errno = 0;
    value = strtoll(buf, &endptr, 10);
    if (errno == ERANGE)
        return -1;
    if (endptr == buf)
        return -1;

    if (*endptr != '\0') {
        switch (tolower((unsigned char)*endptr)) {
        case 'b':
            factor = 512;
            break;
        case 'k':
            factor = 1024;
            break;
        case 'm':
            factor = 1024LL * 1024;
            break;
        case 'g':
            factor = 1024LL * 1024 * 1024;
            break;
        case 't':
            factor = 1024LL * 1024 * 1024 * 1024;
            break;
        case 'p':
            factor = 1024LL * 1024 * 1024 * 1024 * 1024;
            break;
        case 'e':
            factor = 1024LL * 1024 * 1024 * 1024 * 1024 * 1024;
            break;
        default:
            return -1;
        }
        if (value > LLONG_MAX / factor || value < LLONG_MIN / factor)
            return -1;
        value *= factor;
        endptr++;
        if (*endptr != '\0')
            return -1;
    }

    *num = value;
    return 0;
}

static void
getbsize(int *headerlenp, long long *blocksizep)
{
    const char *s;
    du_off_t bytes;

    (void)headerlenp;

    s = getenv("BLOCKSIZE");
    if (s != NULL && *s != '\0') {
        if (expand_number(s, &bytes) == 0 && bytes >= DEV_BSIZE) {
            *blocksizep = (long long)bytes;
            return;
        }
        warnx("invalid BLOCKSIZE: %s", s);
    }
    *blocksizep = 512;
}

static void
prthumanval(long long blocks)
{
    long long bytes = blocks * cblocksize;
    char buf[32];
    long long divisor = 1024;
    const char *units[] = {"", "K", "M", "G", "T", "P", "E"};
    const char *si_units[] = {"", "kB", "MB", "GB", "TB", "PB", "EB"};
    int unit_idx = 0;
    double value;

    if (!Aflag)
        bytes *= DEV_BSIZE;
    if (hflag == UNITS_SI)
        divisor = 1000;

    value = (double)bytes;
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

static bool
fnmatch_impl(const char *pat, const char *str)
{
    while (*pat) {
        if (*pat == '*') {
            while (*pat == '*')
                pat++;
            if (!*pat)
                return true;
            while (*str) {
                if (fnmatch_impl(pat, str))
                    return true;
                str++;
            }
            return fnmatch_impl(pat, str);
        } else if (*pat == '?') {
            if (!*str)
                return false;
            pat++;
            str++;
        } else if (*pat == '[') {
            const char *p = pat + 1;
            bool negate = false;
            bool matched = false;
            bool first = true;
            bool closed = false;

            if (*p == '!' || *p == '^') {
                negate = true;
                p++;
            }

            while (*p) {
                if (*p == ']' && !first) {
                    closed = true;
                    break;
                }
                first = false;
                if (*p == '\\') {
                    p++;
                    if (!*p)
                        break;
                    if (*str == *p)
                        matched = true;
                    p++;
                } else if (p[1] == '-' && p[2] != '\0' && p[2] != ']') {
                    unsigned char start = (unsigned char)p[0];
                    unsigned char end = (unsigned char)p[2];
                    unsigned char c = (unsigned char)*str;
                    if (c >= start && c <= end)
                        matched = true;
                    p += 3;
                } else {
                    if (*p == *str)
                        matched = true;
                    p++;
                }
            }

            if (!closed) {
                if (*str != '[')
                    return false;
                str++;
                pat++;
                continue;
            }

            if (matched == negate)
                return false;
            if (!*str)
                return false;
            str++;
            pat = p + 1;
        } else if (*pat == '\\') {
            pat++;
            if (!*pat)
                return false;
            if (*pat != *str)
                return false;
            pat++;
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
    ignores.push_back(std::string(mask));
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

static long long
process_path(const std::filesystem::path& path, const std::string& name,
    int level, bool is_command_line_arg, const std::string& root_name)
{
    std::error_code ec;
    auto sym_status = std::filesystem::symlink_status(path, ec);
    bool is_symlink;
    bool follow;
    std::filesystem::file_status status;
    bool is_dir;
    bool skip_children;
    long long dir_blocks;

    if (ec) {
        warnx("%s: %s", path.string().c_str(), ec.message().c_str());
        rval = 1;
        return 0;
    }

    is_symlink = std::filesystem::is_symlink(sym_status);
    follow = Lflag || (Hflag && is_command_line_arg);

    if (follow) {
        status = std::filesystem::status(path, ec);
        if (ec) {
            warnx("%s: %s", path.string().c_str(), ec.message().c_str());
            rval = 1;
            return 0;
        }
    } else {
        status = sym_status;
    }

    is_dir = std::filesystem::is_directory(status);

    if (ignorep(name))
        return 0;

    skip_children = false;
    if (is_dir && level > 0 && (ftsoptions & FTS_XDEV)) {
        std::string current_root = path.root_name().string();
        if (current_root != root_name)
            skip_children = true;
    }

    dir_blocks = 0;

    if (is_dir) {
        if (!skip_children) {
            std::filesystem::directory_iterator iter(path, ec);
            if (ec) {
                warnx("%s: %s", path.string().c_str(), ec.message().c_str());
                rval = 1;
                return 0;
            }
            std::filesystem::directory_iterator end;
            while (iter != end) {
                const std::filesystem::directory_entry& entry = *iter;
                std::string child_name = entry.path().filename().string();
                if (child_name.empty())
                    child_name = entry.path().string();
                long long child_blocks = process_path(entry.path(), child_name,
                    level + 1, false, root_name);
                dir_blocks += child_blocks;
                iter.increment(ec);
                if (ec) {
                    warnx("%s: %s", path.string().c_str(),
                        ec.message().c_str());
                    rval = 1;
                    break;
                }
            }
        }

        uint64_t dir_size = 0;
        auto sz = std::filesystem::file_size(path, ec);
        if (!ec)
            dir_size = (uint64_t)sz;
        else
            dir_size = 0;

        long long curblocks;
        if (Aflag) {
            curblocks = (long long)howmany(dir_size, cblocksize);
        } else {
            uint64_t st_blocks = howmany(dir_size, 512);
            curblocks = (long long)howmany(st_blocks, cblocksize);
        }
        dir_blocks += curblocks;

        if (level <= depth &&
            threshold <= threshold_sign * howmany(dir_blocks * cblocksize,
            blocksize)) {
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
        if (is_symlink && !follow) {
            /*
             * Windows has no portable lstat(); do not follow the link.
             * Use 0 as an approximation for the link's own size.
             */
            size = 0;
        } else {
            auto sz = std::filesystem::file_size(path, ec);
            if (ec) {
                warnx("%s: %s", path.string().c_str(), ec.message().c_str());
                rval = 1;
                return 0;
            }
            size = (uint64_t)sz;
        }

        long long curblocks;
        if (Aflag) {
            curblocks = (long long)howmany(size, cblocksize);
        } else {
            uint64_t st_blocks = howmany(size, 512);
            curblocks = (long long)howmany(st_blocks, cblocksize);
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
    int i;

    if (argc > 0 && argv[0] != NULL && argv[0][0] != '\0') {
        const char *slash = strrchr(argv[0], '/');
        const char *bslash = strrchr(argv[0], '\\');
        if (bslash != NULL && (slash == NULL || bslash > slash))
            slash = bslash;
        progname = (slash != NULL) ? slash + 1 : argv[0];
    }

    setlocale(LC_ALL, "");

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

    i = 1;
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
                    const char *optarg = NULL;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = (int)strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    errno = 0;
                    cblocksize = atoi(optarg);
                    if (errno == ERANGE || cblocksize <= 0) {
                        warnx("invalid argument to option B: %s", optarg);
                        usage();
                    }
                    break;
                }
                case 'H':
                    Hflag = 1;
                    Lflag = 0;
                    break;
                case 'I': {
                    const char *optarg = NULL;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = (int)strlen(arg) - 1;
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
                    const char *optarg = NULL;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = (int)strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    dflag = 1;
                    errno = 0;
                    depth = atoi(optarg);
                    if (errno == ERANGE || depth < 0) {
                        warnx("invalid argument to option d: %s", optarg);
                        usage();
                    }
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
                    const char *optarg = NULL;
                    if (arg[j + 1] != '\0') {
                        optarg = &arg[j + 1];
                        j = (int)strlen(arg) - 1;
                    } else if (i + 1 < argc) {
                        optarg = argv[++i];
                    } else {
                        usage();
                    }
                    if (expand_number(optarg, &threshold) != 0 ||
                        threshold == 0) {
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

    if (blocksize == 0) {
        int notused;
        getbsize(&notused, &blocksize);
    }

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
/* See LICENSE file for copyright and license details. */
#include <sys/stat.h>
#include <sys/types.h>

#include <dirent.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifdef _WIN32
#include <io.h>
#endif

#include "arg.h"
char *argv0;

#define FLAG(x)  (flag[(x)-'a'])

/*
 * POSIX -> Windows compatibility layer.
 *
 * The Windows/MinGW CRT has no lstat(), does not support the X_OK mode of
 * access(), and does not necessarily expose the POSIX S_IS*() macros,
 * getline() or PATH_MAX.  The shims below provide only what this translation
 * unit needs and keep every test conservative: no filter condition can succeed
 * on Windows when the underlying object cannot exist there.
 */

#ifndef PATH_MAX
#define PATH_MAX 260
#endif

/* access(2) mode bits; the Windows CRT does not name them. */
#ifndef F_OK
#define F_OK 0
#endif
#ifndef X_OK
#define X_OK 1
#endif
#ifndef W_OK
#define W_OK 2
#endif
#ifndef R_OK
#define R_OK 4
#endif

/* set-user-id / set-group-id bits; never set by the Windows CRT. */
#ifndef S_ISUID
#define S_ISUID 04000
#endif
#ifndef S_ISGID
#define S_ISGID 02000
#endif

/*
 * File type tests.  The Windows stat() reports regular files, directories and
 * character devices; block devices, FIFOs and symbolic links have no
 * representation there, so those tests are conservatively false.
 */
#ifndef S_ISDIR
#define S_ISDIR(m) (((m) & _S_IFMT) == _S_IFDIR)
#endif
#ifndef S_ISREG
#define S_ISREG(m) (((m) & _S_IFMT) == _S_IFREG)
#endif
#ifndef S_ISCHR
#define S_ISCHR(m) (((m) & _S_IFMT) == _S_IFCHR)
#endif
#ifndef S_ISBLK
#define S_ISBLK(m) (0)
#endif
#ifndef S_ISFIFO
#define S_ISFIFO(m) (0)
#endif
#ifndef S_ISLNK
#define S_ISLNK(m) (0)
#endif

/*
 * access() equivalent.  Windows has no execute permission bit and _access()
 * rejects mode 1, so the -x test is reported as "not executable".
 */
static int
stest_access(const char *path, int mode)
{
#ifdef _WIN32
	if (mode == X_OK) {
		errno = EACCES;
		return -1;
	}
	return _access(path, mode);
#else
	return access(path, mode);
#endif
}

/* lstat() equivalent; there is no lstat() on Windows, so -h never matches. */
static int
stest_lstat(const char *path, struct stat *buf)
{
#ifdef _WIN32
	(void)path;
	(void)buf;
	errno = ENOENT;
	return -1;
#else
	return lstat(path, buf);
#endif
}

/*
 * getline() equivalent.  MinGW's <stdio.h> exposes getline() only when a POSIX
 * feature-test macro is requested, so read the stream explicitly.  The buffer
 * is allocated on demand and grown as needed, like getline().
 */
static ssize_t
stest_getline(char **lineptr, size_t *n, FILE *stream)
{
	size_t len = 0;
	int c;

	if (lineptr == NULL || n == NULL || stream == NULL) {
		errno = EINVAL;
		return -1;
	}

	if (*lineptr == NULL || *n == 0) {
		size_t newsize = 128;
		char *newbuf = (char *)realloc(*lineptr, newsize);

		if (newbuf == NULL) {
			errno = ENOMEM;
			return -1;
		}
		*lineptr = newbuf;
		*n = newsize;
	}

	while ((c = fgetc(stream)) != EOF) {
		if (len + 2 > *n) {
			size_t newsize = *n * 2;
			char *newbuf = (char *)realloc(*lineptr, newsize);

			if (newbuf == NULL) {
				errno = ENOMEM;
				return -1;
			}
			*lineptr = newbuf;
			*n = newsize;
		}
		(*lineptr)[len++] = (char)c;
		if (c == '\n')
			break;
	}

	if (len == 0)
		return -1;

	(*lineptr)[len] = '\0';

	return (ssize_t)len;
}

static void test(const char *, const char *);
static void usage(void);

static int match = 0;
static int flag[26];
static struct stat old, newst;   /* "new" is a keyword in C++ */

static void
test(const char *path, const char *name)
{
	struct stat st, ln;

	if ((!stat(path, &st) && (FLAG('a') || name[0] != '.')        /* hidden files      */
	&& (!FLAG('b') || S_ISBLK(st.st_mode))                        /* block special     */
	&& (!FLAG('c') || S_ISCHR(st.st_mode))                        /* character special */
	&& (!FLAG('d') || S_ISDIR(st.st_mode))                        /* directory         */
	&& (!FLAG('e') || stest_access(path, F_OK) == 0)              /* exists            */
	&& (!FLAG('f') || S_ISREG(st.st_mode))                        /* regular file      */
	&& (!FLAG('g') || st.st_mode & S_ISGID)                       /* set-group-id flag */
	&& (!FLAG('h') || (!stest_lstat(path, &ln) && S_ISLNK(ln.st_mode))) /* symbolic link */
	&& (!FLAG('n') || st.st_mtime > newst.st_mtime)               /* newer than file   */
	&& (!FLAG('o') || st.st_mtime < old.st_mtime)                 /* older than file   */
	&& (!FLAG('p') || S_ISFIFO(st.st_mode))                       /* named pipe        */
	&& (!FLAG('r') || stest_access(path, R_OK) == 0)              /* readable          */
	&& (!FLAG('s') || st.st_size > 0)                             /* not empty         */
	&& (!FLAG('u') || st.st_mode & S_ISUID)                       /* set-user-id flag  */
	&& (!FLAG('w') || stest_access(path, W_OK) == 0)              /* writable          */
	&& (!FLAG('x') || stest_access(path, X_OK) == 0)) != FLAG('v')) {   /* executable  */
		if (FLAG('q'))
			exit(0);
		match = 1;
		puts(name);
	}
}

static void
usage(void)
{
	fprintf(stderr, "usage: %s [-abcdefghlpqrsuvwx] "
	        "[-n file] [-o file] [file...]\n", argv0);
	exit(2); /* like test(1) return > 1 on error */
}

int
main(int argc, char *argv[])
{
	struct dirent *d;
	char path[PATH_MAX], *line = NULL, *file;
	size_t linesiz = 0;
	ssize_t n;
	DIR *dir;
	int r;

	ARGBEGIN {
	case 'n': /* newer than file */
	case 'o': /* older than file */
		file = EARGF(usage());
		if (!(FLAG(ARGC()) = !stat(file, (ARGC() == 'n' ? &newst : &old))))
			perror(file);
		break;
	default:
		/* miscellaneous operators */
		if (strchr("abcdefghlpqrsuvwx", ARGC()))
			FLAG(ARGC()) = 1;
		else
			usage(); /* unknown flag */
	} ARGEND;

	if (!argc) {
		/* read list from stdin */
		while ((n = stest_getline(&line, &linesiz, stdin)) > 0) {
			if (line[n - 1] == '\n')
				line[n - 1] = '\0';
			test(line, line);
		}
		free(line);
	} else {
		for (; argc; argc--, argv++) {
			if (FLAG('l') && (dir = opendir(*argv))) {
				/* test directory contents */
				while ((d = readdir(dir))) {
					r = snprintf(path, sizeof path, "%s/%s",
					             *argv, d->d_name);
					if (r >= 0 && (size_t)r < sizeof path)
						test(path, d->d_name);
				}
				closedir(dir);
			} else {
				test(*argv, *argv);
			}
		}
	}
	return match ? 0 : 1;
}
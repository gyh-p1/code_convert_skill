/*-
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Copyright (c) 1991, 1993, 1994
 *	The Regents of the University of California.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/*
 * Windows (x64, MinGW-w64/UCRT64, g++ -std=c++17) migration notes:
 *
 *  - getcwd(NULL, 0) is not a Windows entry point; the physical path is
 *    obtained with _getcwd(NULL, 0) (<direct.h>), which allocates the result
 *    with malloc().  getcwd_physical() additionally retries with a growing
 *    caller-supplied buffer if a run-time rejects a NULL buffer; the path
 *    string produced is the same in either case.
 *
 *  - <err.h> and err(3)/errx(3) do not exist on Windows.  err_exit()
 *    reproduces the BSD err() output exactly:
 *        "<progname>: <fmt>: <strerror(errno)>\n"   then exit(eval),
 *    where <progname> is the last path component of argv[0], the same value
 *    the BSD C run-time gives to __progname.
 *
 *  - __dead2 is a FreeBSD <sys/cdefs.h> spelling and is not provided by the
 *    target build; the "does not return" property is written with the
 *    standard C++ [[noreturn]] attribute instead.
 *
 *  - getopt(3) is not part of the Windows C run-time and <unistd.h> does not
 *    guarantee it under g++ -std=c++17 (__STRICT_ANSI__).  pwd_getopt() is a
 *    self-contained implementation of the subset used here: short options
 *    without arguments, '-' and "--" handling, '?' for an unknown option.
 *    It scans without the GNU argv permutation, which is irrelevant for this
 *    program since any remaining operand leads to usage().  It also does not
 *    print a getopt-style diagnostic for an unknown option: the option is
 *    reported as '?' and usage() emits the usage line, which is the
 *    behaviour this program is required to exhibit.
 *
 *  - KNOWN PLATFORM DIFFERENCE (recorded, not worked around): on Windows
 *    stat() reports st_ino == 0 for every file and st_dev is only the volume
 *    (drive) number, so the original (st_dev, st_ino) identity test cannot
 *    tell $PWD apart from the current directory - any $PWD on the same volume
 *    would compare equal.  getcwd_logical() therefore conservatively treats
 *    the identity check as unavailable (it can never match), so -L falls back
 *    to the physical getcwd() result exactly as if the check had failed,
 *    instead of printing an unverified $PWD.  The default (physical) mode and
 *    -P are unaffected.  A reliable Windows equivalent would require
 *    GetFileInformationByHandle() (volume serial number plus file index),
 *    which is deliberately not introduced here.
 *
 *  - The absolute-path test for $PWD (first character '/') is kept verbatim
 *    from the original; Windows drive-letter/UNC absolute paths are not
 *    treated as logical candidates, exactly as in the original source.
 */

#if 0
#ifndef lint
static char const copyright[] =
"@(#) Copyright (c) 1991, 1993, 1994\n\
	The Regents of the University of California.  All rights reserved.\n";
#endif /* not lint */

#ifndef lint
static char sccsid[] = "@(#)pwd.c	8.3 (Berkeley) 4/1/94";
#endif /* not lint */
#endif

#include <sys/types.h>
#include <sys/stat.h>

#include <direct.h>
#include <errno.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *progname = "pwd";

static char *getcwd_logical(void);
static char *getcwd_physical(void);
static int pwd_getopt(int argc, char *const argv[], const char *optstring);
static void set_progname(const char *arg0);
[[noreturn]] static void usage(void);
[[noreturn]] static void err_exit(int eval, const char *fmt, ...);

int
main(int argc, char *argv[])
{
	int physical;
	int ch;
	char *p;

	set_progname(argv[0]);

	physical = 1;
	while ((ch = pwd_getopt(argc, argv, "LP")) != -1)
		switch (ch) {
		case 'L':
			physical = 0;
			break;
		case 'P':
			physical = 1;
			break;
		case '?':
		default:
			usage();
		}
	argc -= pwd_optind;
	argv += pwd_optind;

	if (argc != 0)
		usage();

	/*
	 * If we're trying to find the logical current directory and that
	 * fails, behave as if -P was specified.
	 */
	if ((!physical && (p = getcwd_logical()) != NULL) ||
	    (p = getcwd_physical()) != NULL)
		printf("%s\n", p);
	else
		err_exit(1, ".");

	exit(0);
}

static void
usage(void)
{

	(void)fprintf(stderr, "usage: pwd [-L | -P]\n");
	exit(1);
}

/*
 * Replacement for BSD err(eval, fmt, ...): print
 * "<progname>: <fmt>: <strerror(errno)>\n" on stderr and exit(eval).
 */
static void
err_exit(int eval, const char *fmt, ...)
{
	int saved_errno;
	va_list ap;

	saved_errno = errno;
	fprintf(stderr, "%s: ", progname);
	if (fmt != NULL) {
		va_start(ap, fmt);
		vfprintf(stderr, fmt, ap);
		va_end(ap);
		fprintf(stderr, ": ");
	}
	fprintf(stderr, "%s\n", strerror(saved_errno));
	exit(eval);
}

static char *
getcwd_logical(void)
{
	struct stat lg, phy;
	char *pwd;

	/*
	 * Check that $PWD is an absolute logical pathname referring to
	 * the current working directory.
	 *
	 * Windows: stat() always reports st_ino == 0 and st_dev is only the
	 * volume number, so a (st_dev, st_ino) match proves nothing.  The
	 * st_ino != 0 guard makes the identity test conservatively unavailable
	 * here, so that -L falls back to the physical getcwd() result instead
	 * of printing an unverified $PWD.
	 */
	if ((pwd = getenv("PWD")) != NULL && *pwd == '/') {
		if (stat(pwd, &lg) == -1 || stat(".", &phy) == -1)
			return (NULL);
		if (lg.st_ino != 0 &&
		    lg.st_dev == phy.st_dev && lg.st_ino == phy.st_ino)
			return (pwd);
	}

	errno = ENOENT;
	return (NULL);
}

/*
 * Physical current directory.  _getcwd(NULL, 0) allocates the result with
 * malloc(); if a run-time does not support that, retry with a caller-supplied
 * buffer that is grown on ERANGE.  A failure keeps errno set by the last
 * _getcwd() call, so err_exit() reports the real reason.
 */
static char *
getcwd_physical(void)
{
	char *p;
	size_t cap;

	p = _getcwd(NULL, 0);
	if (p != NULL)
		return (p);

	for (cap = 256; cap <= ((size_t)1 << 20); cap *= 2) {
		char *buf;

		buf = (char *)malloc(cap);
		if (buf == NULL)
			return (NULL);
		if (_getcwd(buf, (int)cap) != NULL)
			return (buf);
		free(buf);
		if (errno != ERANGE)
			return (NULL);
	}

	errno = ERANGE;
	return (NULL);
}

/*
 * Minimal, self-contained getopt(3) for short options without arguments.
 * pwd_optind is left at the first non-option argument (or after "--"), so
 * "argc -= pwd_optind" counts the remaining operands as in the original.
 */
static int pwd_optind = 1;
static int pwd_optpos = 1;

static int
pwd_getopt(int argc, char *const argv[], const char *optstring)
{
	for (;;) {
		char *arg;
		const char *p;
		char c;

		if (pwd_optind >= argc)
			return (-1);
		arg = argv[pwd_optind];
		if (arg == NULL || arg[0] != '-' || arg[1] == '\0')
			return (-1);		/* operand or bare "-" */
		if (arg[1] == '-' && arg[2] == '\0') {
			pwd_optind++;		/* "--" ends the scan */
			return (-1);
		}
		c = arg[pwd_optpos];
		if (c == '\0') {
			pwd_optind++;
			pwd_optpos = 1;
			continue;
		}
		pwd_optpos++;
		for (p = optstring; *p != '\0'; p++) {
			if (*p == ':')
				continue;
			if (*p == c)
				return (c);
		}
		return ('?');			/* unknown option */
	}
}

static void
set_progname(const char *arg0)
{
	const char *base;
	const char *p;

	if (arg0 == NULL || *arg0 == '\0')
		return;

	base = arg0;
	for (p = arg0; *p != '\0'; p++) {
		if (*p == '/' || *p == '\\')
			base = p + 1;
	}
	if (*base != '\0')
		progname = base;
}
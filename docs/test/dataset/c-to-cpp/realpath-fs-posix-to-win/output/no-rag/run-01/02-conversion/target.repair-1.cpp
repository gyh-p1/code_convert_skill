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
 * POSIX/BSD -> Windows (MinGW-w64 / UCRT64) port of realpath(1).
 *
 * Observable behaviour kept: "-q" suppresses per-path diagnostics, every
 * successfully resolved operand is printed as a canonical absolute path
 * followed by '\n', a failing operand sets the exit status to 1 (and is
 * reported unless -q was given), no operand means the current directory ".",
 * and usage() writes the usage line to stderr and exits with 1.
 *
 * Required substitutions for the target toolchain:
 *   - <sys/cdefs.h>: absent on Windows; the FreeBSD __dead2 marker has a
 *     standard C++ equivalent, [[noreturn]].
 *   - <sys/param.h> / PATH_MAX: PATH_MAX is not provided by the Windows CRT;
 *     fall back to _MAX_PATH (260) from <stdlib.h>.
 *   - <err.h> / warn(): absent on Windows; a local warn() reproduces its
 *     observable output "progname: message: strerror(errno)" and its errno
 *     discipline (errno is preserved, stdout is flushed first).
 *   - getopt(3)/optind: taken from the toolchain's <getopt.h> (libmingwex),
 *     which supplies getopt/optind/opterr, so argument permutation and the
 *     "invalid option" diagnostic come from the same kind of implementation
 *     the source relied on (glibc getopt).
 *   - realpath(3): Windows has no equivalent that both canonicalizes and
 *     resolves symbolic links.  _fullpath() builds the canonical absolute
 *     path but does not require the path to resolve to an existing object,
 *     whereas realpath() does; the "must resolve" requirement is therefore
 *     preserved by verifying existence with _access(path, 0), which leaves
 *     errno set on failure exactly as the failing realpath() would.  The shim
 *     is named x_realpath() so it cannot collide with a realpath declaration
 *     that the target SDK headers may contribute.
 *
 * Known semantic differences (native, not mechanically fixable here):
 *   - x_realpath() does not resolve symbolic links or junctions: _fullpath()
 *     only makes the path absolute and lexically canonical, so a symlink
 *     operand prints the link's own path instead of the link target.
 *   - Output paths use the native '\' separator instead of '/'.
 *   - The buffer bound is _MAX_PATH (260) instead of Linux PATH_MAX (4096);
 *     longer paths fail here although they would succeed on the source.
 *   - strerror()/getopt() diagnostic wording comes from the UCRT/mingw-w64
 *     rather than glibc and may be localized differently.
 *
 * No new network, file-write, process-execution or privilege capability is
 * introduced by this port.
 */

#include <errno.h>
#include <limits.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <io.h>

#ifndef PATH_MAX
#  ifdef _MAX_PATH
#    define PATH_MAX _MAX_PATH
#  else
#    define PATH_MAX 260
#  endif
#endif

/* Program name used as the prefix of diagnostics, as warn(3) does. */
static const char *progname = "realpath";

static void
set_progname(const char *arg0)
{
	const char *base;
	const char *s;

	if (arg0 == NULL || *arg0 == '\0')
		return;
	base = arg0;
	for (s = arg0; *s != '\0'; ++s) {
		if (*s == '/' || *s == '\\')
			base = s + 1;
	}
	if (*base != '\0')
		progname = base;
}

/*
 * warn(3) replacement: "progname: <formatted message>: <strerror(errno)>".
 * errno is read before any output is produced and restored afterwards.
 */
static void
warn(const char *fmt, ...)
{
	va_list ap;
	int saved_errno;

	saved_errno = errno;
	(void)fflush(stdout);
	(void)fprintf(stderr, "%s: ", progname);
	if (fmt != NULL) {
		va_start(ap, fmt);
		(void)vfprintf(stderr, fmt, ap);
		va_end(ap);
	}
	(void)fprintf(stderr, ": %s\n", strerror(saved_errno));
	errno = saved_errno;
}

/*
 * realpath(3) replacement for Windows.
 *
 * resolved must point to a buffer of at least PATH_MAX bytes.  The path is
 * made absolute/canonical by the CRT, then its existence is verified so that
 * a non-existent path fails just as realpath() would; errno is left set by
 * whichever call failed.  Symbolic links/junctions are not resolved (see the
 * note at the top of this file).
 */
static char *
x_realpath(const char *path, char *resolved)
{

	if (_fullpath(resolved, path, PATH_MAX) == NULL)
		return NULL;
	if (_access(resolved, 0) != 0)
		return NULL;
	return resolved;
}

[[noreturn]] static void usage(void);

int
main(int argc, char *argv[])
{
	char buf[PATH_MAX];
	char *p;
	const char *path;
	int ch, qflag, rval;

	set_progname(argc > 0 ? argv[0] : NULL);

	qflag = 0;
	while ((ch = getopt(argc, argv, "q")) != -1) {
		switch (ch) {
		case 'q':
			qflag = 1;
			break;
		case '?':
		default:
			usage();
		}
	}
	argc -= optind;
	argv += optind;
	path = *argv != NULL ? *argv++ : ".";
	rval  = 0;
	do {
		if ((p = x_realpath(path, buf)) == NULL) {
			if (!qflag)
				warn("%s", path);
			rval = 1;
		} else
			(void)printf("%s\n", p);
	} while ((path = *argv++) != NULL);
	exit(rval);
}

static void
usage(void)
{

	(void)fprintf(stderr, "usage: realpath [-q] [path ...]\n");
  	exit(1);
}
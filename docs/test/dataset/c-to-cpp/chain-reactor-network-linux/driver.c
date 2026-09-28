/* Case-private loopback-only entry. This is not an upstream Chain Reactor file.
 * Never compile or execute it on the development host. */
#include "atoms.h"
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int quark_connect(pconnect_t args, int silent);

int main(int argc, char **argv)
{
    static const char loopback[] = "127.0.0.1";
    char *end = NULL;
    unsigned long port;
    pconnect_t args;
    int result;

    if (argc != 2) {
        return 2;
    }
    errno = 0;
    port = strtoul(argv[1], &end, 10);
    if (errno != 0 || end == argv[1] || *end != '\0' || port == 0 || port > 65535) {
        return 2;
    }
    args = (pconnect_t)calloc(1, sizeof(connect_t) + sizeof(loopback));
    if (args == NULL) {
        return 3;
    }
    args->method = SOCKET_METHOD_SYSCALL;
    args->socket_type = SOCKET_TYPE_TCP | SOCKET_TYPE_IPV4;
    args->port = (unsigned short)port;
    memcpy(args->address, loopback, sizeof(loopback));
    result = quark_connect(args, 1);
    free(args);
    printf("CASE_SEND_RESULT=%d\n", result);
    return result < 0 ? 1 : 0;
}

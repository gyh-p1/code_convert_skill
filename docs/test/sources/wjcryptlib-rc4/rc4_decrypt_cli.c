// rc4_decrypt_cli.c
//
// Thin command-line harness (NOT upstream). It decrypts an RC4-obfuscated blob
// with a caller-supplied key, mirroring the real offensive/defensive task of
// extracting a malware configuration / deobfuscating an embedded string, or of
// solving a CTF RC4 challenge. RC4 is a public, well-documented, broken stream
// cipher; this is a generic dual-use codec, not a weapon, loader, or evasion tool.
//
// The graded translation subject is the upstream public-domain RC4 module
// (WjCryptLib_Rc4.c / WjCryptLib_Rc4.h by waterjuice.org, released into the
// public domain, June 2013). This driver only wires that module to a CLI so the
// program is runnable for the dual-build evaluation; it adds no cryptographic
// logic of its own.
//
// Usage:  program <hex-key> <hex-ciphertext>
// Reads only argv, writes only stdout. No file / network / process access.
//
// Example (public RC4 test vector, key "Key" -> plaintext "Plaintext"):
//   program 4b6579 bbf316e8d940af0ad3      ->   Plaintext

#include "WjCryptLib_Rc4.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Convert one hex digit to its 0..15 value, or -1 if it is not a hex digit.
static int nibble( char c )
{
    if( c >= '0' && c <= '9' ) return c - '0';
    if( c >= 'a' && c <= 'f' ) return c - 'a' + 10;
    if( c >= 'A' && c <= 'F' ) return c - 'A' + 10;
    return -1;
}

// Decode a NUL-terminated hex string into out (capacity outcap bytes).
// Returns the number of bytes written, or -1 on malformed / oversized input.
static int hex_decode( const char* hex, uint8_t* out, size_t outcap )
{
    size_t len = strlen( hex );
    if( len % 2 != 0 )
        return -1;

    size_t nbytes = len / 2;
    if( nbytes > outcap )
        return -1;

    for( size_t i = 0; i < nbytes; i++ )
    {
        int hi = nibble( hex[2 * i] );
        int lo = nibble( hex[2 * i + 1] );
        if( hi < 0 || lo < 0 )
            return -1;
        out[i] = (uint8_t)( ( hi << 4 ) | lo );
    }
    return (int)nbytes;
}

int main( int argc, char** argv )
{
    if( argc != 3 )
    {
        fprintf( stderr, "usage: %s <hex-key> <hex-ciphertext>\n",
                 argc > 0 ? argv[0] : "rc4_decrypt" );
        return 2;
    }

    uint8_t key[256];
    uint8_t cipher[4096];
    uint8_t plain[4096];

    int keylen = hex_decode( argv[1], key, sizeof( key ) );
    if( keylen <= 0 )
    {
        fprintf( stderr, "error: key must be 1..256 bytes of valid hex\n" );
        return 2;
    }

    int clen = hex_decode( argv[2], cipher, sizeof( cipher ) );
    if( clen < 0 )
    {
        fprintf( stderr, "error: ciphertext must be valid hex (<= %u bytes)\n",
                 (unsigned)sizeof( cipher ) );
        return 2;
    }

    if( Rc4XorWithKey( key, (uint32_t)keylen, 0, cipher, plain, (uint32_t)clen ) != 0 )
    {
        fprintf( stderr, "error: RC4 initialisation failed\n" );
        return 1;
    }

    fwrite( plain, 1, (size_t)clen, stdout );
    return 0;
}

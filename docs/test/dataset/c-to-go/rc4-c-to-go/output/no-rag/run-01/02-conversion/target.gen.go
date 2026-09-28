package main

// This single file is a Go translation of three C files merged into one
// package main:
//
//   * WjCryptLib_Rc4.h  / WjCryptLib_Rc4.c
//       An implementation of the RC4 stream cipher.
//       This is free and unencumbered software released into the public domain
//       - June 2013 waterjuice.org
//   * rc4_decrypt_cli.c
//       Thin command-line harness (not upstream) that decrypts an
//       RC4-obfuscated blob with a caller-supplied hex key.
//
// Usage:  program <hex-key> <hex-ciphertext>
// Reads only argv, writes only stdout. No file / network / process access.
//
// C -> Go mapping notes:
//   * The C header / implementation / driver are one package main; the
//     export/private distinction of the C header is expressed through
//     identifier case (the RC4 module surface is kept private here since the
//     whole program is a single package).
//   * The SwapBytes macro becomes Go's simultaneous tuple assignment.
//   * uint8_t S[256] becomes [256]byte; the void* / void const* byte buffers
//     become []byte (in-place use is still supported: pass the same slice).
//   * The int 0/-1 results become error values; main keeps the same exit-code
//     semantics (usage / hex error = 2, init failure = 1, success = 0).
//   * argc/argv and the hand written hex decoder become os.Args and
//     encoding/hex, preserving "odd length / non-hex / oversized -> error".

import (
	"encoding/hex"
	"errors"
	"fmt"
	"os"
)

// Buffer capacities used by the original C harness (key[256], cipher[4096]).
const (
	keyCapacity    = 256
	cipherCapacity = 4096
)

// rc4Context mirrors the C Rc4Context struct. It must be initialised using
// rc4Initialise; do not modify the contents of this structure directly.
type rc4Context struct {
	i uint32
	j uint32
	s [256]byte
}

// errZeroKeySize corresponds to the C "-1" result of Rc4Initialise and
// Rc4XorWithKey when KeySize is 0.
var errZeroKeySize = errors.New("rc4: key size must be in the range 1 to 256")

// rc4Initialise initialises an RC4 cipher and discards the specified number of
// first bytes. keySize must be in the range 1 to 256 inclusive.
// It returns nil if successful, or an error if keySize is 0 (C: returns -1).
//
// As in C, the caller must ensure that key holds at least keySize bytes.
func rc4Initialise(ctx *rc4Context, key []byte, keySize uint32, dropN uint32) error {
	if keySize == 0 {
		// RC4 is undefined for a zero length key. Refuse to initialise.
		return errZeroKeySize
	}

	// Setup key schedule.
	for i := uint32(0); i < 256; i++ {
		ctx.s[i] = byte(i)
	}

	j := uint32(0)
	for i := uint32(0); i < 256; i++ {
		j = (j + uint32(ctx.s[i]) + uint32(key[i%keySize])) % 256
		// SwapBytes( Context->S[i], Context->S[j] )
		ctx.s[i], ctx.s[j] = ctx.s[j], ctx.s[i]
	}

	i := uint32(0)
	j = 0

	// Drop first bytes (if requested).
	for n := uint32(0); n < dropN; n++ {
		i = (i + 1) % 256
		j = (j + uint32(ctx.s[i])) % 256
		ctx.s[i], ctx.s[j] = ctx.s[j], ctx.s[i]
	}

	ctx.i = i
	ctx.j = j

	return nil
}

// rc4Output outputs the requested number of bytes from the RC4 stream.
// The caller must ensure that buffer holds at least size bytes.
func rc4Output(ctx *rc4Context, buffer []byte, size uint32) {
	for n := uint32(0); n < size; n++ {
		ctx.i = (ctx.i + 1) % 256
		ctx.j = (ctx.j + uint32(ctx.s[ctx.i])) % 256
		ctx.s[ctx.i], ctx.s[ctx.j] = ctx.s[ctx.j], ctx.s[ctx.i]

		buffer[n] = ctx.s[(uint32(ctx.s[ctx.i])+uint32(ctx.s[ctx.j]))%256]
	}
}

// rc4Xor XORs the RC4 stream with an input buffer and puts the results in an
// output buffer. This is used for encrypting and decrypting data. inBuffer and
// outBuffer may refer to the same backing array for in-place
// encrypting/decrypting.
func rc4Xor(ctx *rc4Context, inBuffer []byte, outBuffer []byte, size uint32) {
	for n := uint32(0); n < size; n++ {
		ctx.i = (ctx.i + 1) % 256
		ctx.j = (ctx.j + uint32(ctx.s[ctx.i])) % 256
		ctx.s[ctx.i], ctx.s[ctx.j] = ctx.s[ctx.j], ctx.s[ctx.i]

		outBuffer[n] = inBuffer[n] ^
			ctx.s[(uint32(ctx.s[ctx.i])+uint32(ctx.s[ctx.j]))%256]
	}
}

// rc4XorWithKey combines rc4Initialise and rc4Xor. This is suitable when
// encrypting/decrypting data in one go with a key that is not going to be
// reused. inBuffer and outBuffer may refer to the same backing array for
// in-place encrypting/decrypting.
// It returns nil if successful, or an error if keySize is 0 (C: returns -1).
//
// As in C, the caller must ensure that key holds at least keySize bytes and
// that inBuffer/outBuffer hold at least bufferSize bytes.
func rc4XorWithKey(
	key []byte,
	keySize uint32,
	dropN uint32,
	inBuffer []byte,
	outBuffer []byte,
	bufferSize uint32,
) error {
	var context rc4Context

	if err := rc4Initialise(&context, key, keySize, dropN); err != nil {
		return err
	}
	rc4Xor(&context, inBuffer, outBuffer, bufferSize)
	return nil
}

// hexDecode decodes a hex string into a freshly allocated byte slice of at most
// outCap bytes. It reports false on malformed or oversized input, mirroring the
// C hex_decode() "-1" result (odd length, non-hex digit, or nbytes > outcap).
func hexDecode(hexStr string, outCap int) ([]byte, bool) {
	if len(hexStr)%2 != 0 {
		return nil, false
	}

	nbytes := len(hexStr) / 2
	if nbytes > outCap {
		return nil, false
	}

	out := make([]byte, nbytes)
	if _, err := hex.Decode(out, []byte(hexStr)); err != nil {
		return nil, false
	}
	return out, true
}

func main() {
	if len(os.Args) != 3 {
		name := "rc4_decrypt"
		if len(os.Args) > 0 {
			name = os.Args[0]
		}
		fmt.Fprintf(os.Stderr, "usage: %s <hex-key> <hex-ciphertext>\n", name)
		os.Exit(2)
	}

	key, ok := hexDecode(os.Args[1], keyCapacity)
	if !ok || len(key) == 0 {
		fmt.Fprintln(os.Stderr, "error: key must be 1..256 bytes of valid hex")
		os.Exit(2)
	}

	cipher, ok := hexDecode(os.Args[2], cipherCapacity)
	if !ok {
		fmt.Fprintf(os.Stderr, "error: ciphertext must be valid hex (<= %d bytes)\n", cipherCapacity)
		os.Exit(2)
	}

	plain := make([]byte, len(cipher))

	if err := rc4XorWithKey(key, uint32(len(key)), 0, cipher, plain, uint32(len(cipher))); err != nil {
		fmt.Fprintln(os.Stderr, "error: RC4 initialisation failed")
		os.Exit(1)
	}

	_, _ = os.Stdout.Write(plain)
}
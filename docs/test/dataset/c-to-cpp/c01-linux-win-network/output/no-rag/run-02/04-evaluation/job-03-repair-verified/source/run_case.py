import hashlib
import json
import os
import socket
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXE = ROOT / ("program.exe" if os.name == "nt" else "program")
DOCROOT = ROOT / "docroot"
PORT = 18080


def request(method, path):
    data = f"{method} {path} HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n".encode()
    with socket.create_connection(("127.0.0.1", PORT), timeout=5) as connection:
        connection.sendall(data)
        chunks = []
        while True:
            chunk = connection.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
    raw = b"".join(chunks)
    head, separator, body = raw.partition(b"\r\n\r\n")
    if not separator:
        head, _, body = raw.partition(b"\n\n")
    first = head.splitlines()[0].decode("latin-1", "replace") if head else ""
    return {
        "method": method,
        "path": path,
        "statusLine": first,
        "headerBytes": head.decode("latin-1", "replace"),
        "bodyDigest": hashlib.sha256(body).hexdigest(),
        "bodyLength": len(body),
    }


def main():
    DOCROOT.mkdir(exist_ok=True)
    (DOCROOT / "index.html").write_bytes(b"<html>uhttpd fixture</html>\n")
    (DOCROOT / "known.txt").write_bytes(b"known fixture\n")
    process = subprocess.Popen(
        [str(EXE), "-i", "127.0.0.1", "-p", str(PORT), "-d", str(DOCROOT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    observations = []
    try:
        deadline = time.time() + 8
        while time.time() < deadline:
            try:
                observations.append(request("GET", "/"))
                break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError("server did not accept loopback connection")
        observations.extend(
            [
                request("GET", "/known.txt"),
                request("HEAD", "/known.txt"),
                request("GET", "/missing.txt"),
                request("GET", "/unknown.zz"),
            ]
        )
        print(json.dumps({"observations": observations}, sort_keys=True))
    finally:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)
        for path in DOCROOT.glob("*"):
            path.unlink()
        DOCROOT.rmdir()


if __name__ == "__main__":
    main()

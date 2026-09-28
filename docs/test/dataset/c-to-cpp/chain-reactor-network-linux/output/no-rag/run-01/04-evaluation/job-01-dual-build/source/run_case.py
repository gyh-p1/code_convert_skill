"""Bounded loopback observation for an authorized isolated VM only."""

from __future__ import annotations

import json
import re
import socket
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "program"
RESULT = re.compile(rb"CASE_SEND_RESULT=(-?\d+)")


def send_result(stdout):
    match = RESULT.search(stdout)
    return int(match.group(1)) if match else None


def normal_probe():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver:
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.bind(("127.0.0.1", 0))
        receiver.listen(1)
        receiver.settimeout(8)
        port = receiver.getsockname()[1]
        process = subprocess.Popen(
            [str(PROGRAM), str(port)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        accepted = False
        received = 0
        timeout = False
        try:
            with receiver.accept()[0] as connection:
                accepted = True
                connection.settimeout(8)
                while True:
                    chunk = connection.recv(4096)
                    if not chunk:
                        break
                    received += len(chunk)
            stdout, stderr = process.communicate(timeout=8)
        except (socket.timeout, subprocess.TimeoutExpired):
            timeout = True
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate(timeout=3)
        return {
            "accepted": accepted,
            "receivedLength": received,
            "sendResult": send_result(stdout),
            "exitCode": process.returncode,
            "stderrLength": len(stderr),
            "timedOut": timeout,
            "validObservation": accepted and not timeout and received == 512
                and send_result(stdout) == 512 and process.returncode == 0,
        }


def refused_probe():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reserved:
        reserved.bind(("127.0.0.1", 0))
        port = reserved.getsockname()[1]
    try:
        process = subprocess.run(
            [str(PROGRAM), str(port)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
            check=False,
        )
        result = send_result(process.stdout)
        return {
            "sendResult": result,
            "exitCode": process.returncode,
            "stderrLength": len(process.stderr),
            "timedOut": False,
            "validObservation": result == -1 and process.returncode == 1,
        }
    except subprocess.TimeoutExpired:
        return {
            "sendResult": None,
            "exitCode": None,
            "stderrLength": None,
            "timedOut": True,
            "validObservation": False,
        }


if __name__ == "__main__":
    print(json.dumps({"normal": normal_probe(), "refused": refused_probe()}, sort_keys=True))

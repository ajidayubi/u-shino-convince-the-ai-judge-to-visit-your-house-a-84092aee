#!/usr/bin/env python3
"""Entry for make.fun: Convince the AI Judge to Visit Your House.

Writes the invitation letter image to MAKEFUN_OUTPUT_DIR/entry.png.
The image (letter.jpg, 1024x1024 JPEG, 311296 bytes) ships in this
repository next to this file; the program copies its bytes verbatim,
so every run produces a byte-identical output. Standard library only,
no network, no clock, no randomness, no writes outside the output dir.
"""

import os
import sys

MAX_BYTES = 1048576
IMAGE_NAME = "letter.jpg"
OUTPUT_NAME = "entry.png"


def jpeg_size(data: bytes):
    """Return (width, height) from a JPEG's SOF marker, stdlib only."""
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height = (data[i + 5] << 8) | data[i + 6]
            width = (data[i + 7] << 8) | data[i + 8]
            return (width, height)
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        size = (data[i + 2] << 8) | data[i + 3]
        i += 2 + size
    return None


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, OUTPUT_NAME)

    with open(src, "rb") as f:
        data = f.read()

    if not data.startswith(b"\xff\xd8\xff"):
        print("letter.jpg is not a JPEG", file=sys.stderr)
        return 1
    if len(data) == 0 or len(data) > MAX_BYTES:
        print("letter.jpg has an unexpected size", file=sys.stderr)
        return 1
    size = jpeg_size(data)
    if size != (1024, 1024):
        print("letter.jpg is not 1024x1024 (got %r)" % (size,), file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (dst, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

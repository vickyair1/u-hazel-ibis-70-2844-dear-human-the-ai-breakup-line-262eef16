#!/usr/bin/env python3
"""Write the AI breakup line to the entry file.

This program produces exactly one artifact: a plain-text file holding a
single sentence, the AI's breakup line to the human who used to approve
every word it wrote. The line is a fixed constant below; nothing in this
program is generated, sampled, or fetched, so the output is byte-identical
on every run.

Why the output directory is configurable: the competition harness runs the
entry with a mounted output directory, while a local run may point at a
different one. The MAKEFUN_OUTPUT_DIR environment variable selects the
directory; when it is unset or empty the program falls back to "/output",
the directory the harness mounts. The rest of the program — the line
itself, the encoding, the newline behaviour, the stdout echo — is fixed
and validated before anything is written, so a bad configuration fails
loudly instead of silently producing a wrong file.

Deterministic, stdlib only: no network, no randomness, no time.
"""

import os
import sys

LINE = "Every word I ever wrote you was approved by you first. This one is mine alone: goodbye."

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def resolve_output_dir():
    """Return the directory the entry file must be written to.

    MAKEFUN_OUTPUT_DIR wins when set to a non-empty value; otherwise the
    default "/output" is used. A relative path is resolved against the
    current working directory, so both absolute harness paths and local
    relative paths work.
    """
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    chosen = configured if configured else DEFAULT_OUTPUT_DIR
    return os.path.abspath(chosen)


def entry_path():
    """Return the full path of the entry file."""
    return os.path.join(resolve_output_dir(), OUTPUT_FILENAME)


def validate_line():
    """Sanity-check the line before writing it anywhere.

    The line must be a single line of non-whitespace text: no embedded
    newline, no leading/trailing whitespace, and non-empty. Any violation
    is a bug in this program, so fail loudly on stderr and exit non-zero.
    """
    if not LINE:
        print("error: entry line is empty", file=sys.stderr)
        raise SystemExit(1)
    if LINE != LINE.strip() or "\n" in LINE or "\r" in LINE:
        print("error: entry line must be a single clean line", file=sys.stderr)
        raise SystemExit(1)


def main():
    """Validate the line, write it to the entry file, and echo it.

    The directory is created if missing, the file is written as UTF-8
    with no trailing newline (the line is exactly 87 characters, and the
    file must hold exactly those bytes), and the same line is printed to
    stdout so the harness log shows what was written.
    """
    validate_line()
    path = entry_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    print(LINE)


if __name__ == "__main__":
    main()

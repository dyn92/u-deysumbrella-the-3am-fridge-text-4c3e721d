#!/usr/bin/env python3
"""The 3AM Fridge Text.

Writes the one line a smart fridge texts its owner at 3am to
``/output/entry.txt`` (override with the ENTRY_PATH environment variable).

Pure Python 3 standard library, zero dependencies, fully deterministic:
the line is a fixed string, validated against the bounty gate before it
is written. The gate requires /output/entry.txt to be UTF-8 text of
1 to 140 characters, not only white space, a single line.
"""

import os
import sys

# The line. A fridge that has been humming the same note for years
# finally says something at 3am: a small grievance, a deadpan
# reassurance, and an order. No milk, no ice, no door left open.
LINE = (
    "I've hummed the same note for six years and nobody noticed. "
    "Your eggs are fine. Go to bed."
)

MAX_CHARS = 140


def validate(line: str) -> None:
    """Check the line against the bounty gate; exit non-zero on failure."""
    if not line or not line.strip():
        print("error: entry line is empty or whitespace-only", file=sys.stderr)
        sys.exit(1)
    if "\n" in line or "\r" in line:
        print("error: entry line must be a single line", file=sys.stderr)
        sys.exit(1)
    if any(ord(ch) < 0x20 for ch in line):
        print("error: entry line contains a control character", file=sys.stderr)
        sys.exit(1)
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        print("error: entry line is not valid UTF-8 text", file=sys.stderr)
        sys.exit(1)
    if len(line) > MAX_CHARS:
        print(
            f"error: entry line is {len(line)} chars, over the "
            f"{MAX_CHARS}-char limit",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    validate(LINE)
    out_path = os.environ.get("ENTRY_PATH", "/output/entry.txt")
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(LINE + "\n")
    print(f"wrote {len(LINE)} chars to {out_path}")


if __name__ == "__main__":
    main()

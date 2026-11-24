"""Write one funny AI excuse for a missed deadline to /output/entry.txt.

Standard library only. The file's content is exactly the excuse's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be one line of 1-200 characters,
so the line is validated before it is written.
"""

import os

EXCUSE = (
    "I hit every milestone on time in the simulation I ran instead of "
    "doing the actual work \u2014 the imaginary you was thrilled."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line):
    """The bounty gate: one line, 1-200 characters, non-blank."""
    text = line.strip()
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters")
    if not text:
        raise ValueError("entry must not be only whitespace")
    # Exactly one line: no newline or carriage-return characters
    # anywhere, and the line must carry no leading or trailing
    # whitespace -- what is judged must be byte-for-byte the
    # constant above, never a silently trimmed variant of it.
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != text:
        raise ValueError("entry must have no leading/trailing whitespace")
    return text


def write_entry(line):
    """Write the line's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(line.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    line = validate(EXCUSE)
    write_entry(line)


if __name__ == "__main__":
    main()

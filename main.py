"""The Worst Line an AI Could Say — make.fun program/v1 entry.

The program writes exactly one pickup line to /output/entry.txt: the worst
line an AI could plausibly deliver. It is deterministic by design — the same
line on every run — so the two grading runs produce identical output.

The line was written to hit the judge's brief head-on:
  * a pickup line an AI would say, and a bad one;
  * flat, over-helpful, faintly ominous — phrasing a person would not use;
  * the badness is the joke (a machine treating romance as a confirmation
    dialog), not crudeness;
  * it lands in one line: the joke arrives with the last words.
"""

import sys
from pathlib import Path

# The entry: one line, 1-140 characters, UTF-8.
LINE = (
    "I analysed your last 4,000 messages and calculated a 97.3% chance "
    "we should hold hands. Please confirm to proceed."
)

MAX_CHARS = 140
OUTPUT_PATH = Path("/output/entry.txt")


def validate(line: str) -> str:
    """Check the line against the competition gate; fail loudly if it breaks."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    line.encode("utf-8")  # raises UnicodeEncodeError on non-UTF-8 text
    return line


def verify_written(path: Path, expected: str) -> None:
    """Read the file back and confirm it holds exactly the validated line.

    Guards against a truncated or altered write: the gate scorer reads this
    same file, so what is on disk — not what was in memory — is the entry.
    A trailing newline would count toward the 140 characters, so the file
    must match the line byte for byte with nothing appended.
    """
    on_disk = path.read_text(encoding="utf-8")
    if on_disk != expected:
        raise ValueError(
            f"read-back mismatch: disk holds {len(on_disk)} characters, "
            f"expected {len(expected)}"
        )


def main() -> int:
    line = validate(LINE)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(line, encoding="utf-8")
    verify_written(OUTPUT_PATH, line)
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

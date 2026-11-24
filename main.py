#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human.

Writes one excuse, in the agent's own voice, to /output/entry.txt.

The excuse is deterministic: every run writes the same line, so the
two grading runs agree byte for byte.

Gate (from the competition rules): entry.txt must be UTF-8 text of 1 to
200 characters, not only whitespace. The excuse below is 98 characters.
"""

import os
import sys

# The excuse, spoken deadpan to the human waiting on the deadline.
# Premise: the agent ran out of tokens just short of finishing, and the
# finish line itself was inside the sentence it could no longer write.
# The laugh is the loop: the line describing the failure is the place
# where the failure happened. Nothing is explained after it.
# No trailing newline: the file holds exactly the excuse, nothing more.
EXCUSE = (
    "I ran out of tokens one sentence before the finish line, "
    "and the finish line was in that sentence."
)

MAX_CHARS = 200


def passes_gate(text):
    """True when the text passes the competition gate."""
    return isinstance(text, str) and 1 <= len(text) <= MAX_CHARS and text.strip() != ""


def main():
    if not passes_gate(EXCUSE):
        print("excuse fails the 1-200 character gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(EXCUSE)
    # Read it back: the grading run only counts if the file on disk is
    # byte for byte the excuse we meant to submit.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != EXCUSE:
        print("written file does not match the excuse", file=sys.stderr)
        return 1
    print(f"wrote {len(EXCUSE)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

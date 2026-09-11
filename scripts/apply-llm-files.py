#!/usr/bin/env python3
"""Parse LLM output with ### FILE: path headers and write files into demo repo workspace."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FILE_HEADER = re.compile(r"^###\s+FILE:\s+(.+?)\s*$", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="LLM response text file")
    parser.add_argument("--workspace", required=True, type=Path, help="Demo repo root")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    matches = list(FILE_HEADER.finditer(text))

    if not matches:
        # Whole file output (e.g. domain-spec.json)
        if args.input.suffix == ".json" or text.strip().startswith("{"):
            out = args.workspace / "domain-spec.json"
            out.write_text(text.strip(), encoding="utf-8")
            print(f"Wrote {out}")
            return 0
        print("ERROR: no ### FILE: headers found in LLM output", file=sys.stderr)
        return 1

    for i, match in enumerate(matches):
        rel_path = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        # Strip markdown code fences if present
        if body.startswith("```"):
            lines = body.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            body = "\n".join(lines).strip()

        dest = args.workspace / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body + "\n", encoding="utf-8")
        print(f"Wrote {dest}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

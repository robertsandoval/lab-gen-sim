#!/usr/bin/env python3
"""Validate domain-brief.yaml against schemas/domain-brief.schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema required (pip install jsonschema)", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <domain-brief.yaml>", file=sys.stderr)
        return 2

    brief_path = Path(sys.argv[1])
    repo_root = Path(__file__).resolve().parent.parent
    schema_path = repo_root / "schemas" / "domain-brief.schema.json"

    if not brief_path.is_file():
        print(f"ERROR: file not found: {brief_path}", file=sys.stderr)
        return 1

    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)

    with brief_path.open(encoding="utf-8") as f:
        brief = yaml.safe_load(f)

    try:
        jsonschema.validate(instance=brief, schema=schema)
    except jsonschema.ValidationError as exc:
        print(f"VALIDATION FAILED: {exc.message}", file=sys.stderr)
        if exc.absolute_path:
            print(f"  at: {'/'.join(str(p) for p in exc.absolute_path)}", file=sys.stderr)
        return 1

    print(f"OK: {brief_path} is valid (domain_id={brief.get('domain_id')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

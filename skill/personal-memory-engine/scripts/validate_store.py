#!/usr/bin/env python3
"""Validate deterministic parts of a personal-memory runtime store."""

import argparse
import json
from pathlib import Path

REQUIRED_CAPTURE_FIELDS = {"schema_version", "event_id", "captured_at", "hook_event_name", "cwd", "role", "content", "content_sha256"}


def validate_json(path: Path) -> list[str]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return []
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]


def validate_jsonl(path: Path, required: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"{path}: {exc}"]
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{number}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path}:{number}: expected object")
            continue
        missing = sorted(required - value.keys())
        if missing:
            errors.append(f"{path}:{number}: missing {', '.join(missing)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    root = parser.parse_args().root.resolve()
    errors: list[str] = []
    for relative in ("runtime/mode.json", "runtime/retrieval-index.json", "schemas/evidence.schema.json", "schemas/hypothesis.schema.json"):
        errors.extend(validate_json(root / relative))
    for path in sorted((root / "private-inbox").glob("*.jsonl")):
        errors.extend(validate_jsonl(path, REQUIRED_CAPTURE_FIELDS))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Store is valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

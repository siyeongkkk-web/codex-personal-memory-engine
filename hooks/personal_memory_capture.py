#!/usr/bin/env python3
"""Write minimal turn events to a user-owned inbox. Never steer Codex."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

RUNTIME_ROOT = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "personal-memory"
CONFIG_PATH = RUNTIME_ROOT / "config.json"
SECRET_PATTERNS = (
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"), "[REDACTED_OPENAI_KEY]"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"), "Bearer [REDACTED_TOKEN]"),
    (re.compile(r"(?i)\b(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*([^\s,;]+)"), r"\1=[REDACTED]"),
)


def load_config() -> dict[str, Any] | None:
    try:
        value = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def redact(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def select_content(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    if payload.get("hook_event_name") == "UserPromptSubmit":
        value = payload.get("prompt")
        return "user", value if isinstance(value, str) else None
    if payload.get("hook_event_name") == "Stop":
        value = payload.get("last_assistant_message")
        return "assistant", value if isinstance(value, str) else None
    return None, None


def capture(payload: dict[str, Any]) -> None:
    config = load_config()
    if not config or config.get("capture_enabled") is not True:
        return
    scope = config.get("workspace_scope")
    cwd = payload.get("cwd")
    if not isinstance(scope, str) or not isinstance(cwd, str) or not is_within(Path(cwd), Path(scope)):
        return
    role, content = select_content(payload)
    if role is None or not content or not content.strip():
        return

    maximum = config.get("max_content_chars", 100000)
    maximum = maximum if isinstance(maximum, int) and maximum > 0 else 100000
    original_length = len(content)
    content = redact(content[:maximum])
    now = datetime.now().astimezone()
    identity = "\u241f".join((str(payload.get("session_id", "")), str(payload.get("turn_id", "")), role, content))
    record = {
        "schema_version": "1.0",
        "event_id": "capture_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20],
        "captured_at": now.isoformat(timespec="seconds"),
        "hook_event_name": payload.get("hook_event_name"),
        "session_id": payload.get("session_id"),
        "turn_id": payload.get("turn_id"),
        "cwd": cwd,
        "role": role,
        "content": content,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "truncated": original_length > maximum,
        "source": "codex_hook",
        "processed_at": None
    }
    inbox = RUNTIME_ROOT / "private-inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    with (inbox / f"{now.date().isoformat()}.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> int:
    payload: dict[str, Any] = {}
    try:
        incoming = json.load(sys.stdin)
        if isinstance(incoming, dict):
            payload = incoming
            capture(payload)
    except Exception:
        pass
    if payload.get("hook_event_name") == "Stop":
        sys.stdout.write("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

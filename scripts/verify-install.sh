#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
RUNTIME_DIR="$CODEX_DIR/personal-memory"

python3 -m json.tool "$RUNTIME_DIR/config.json" >/dev/null
python3 -m json.tool "$CODEX_DIR/hooks.json" >/dev/null
python3 "$SCRIPT_DIR/skill/personal-memory-engine/scripts/validate_store.py" "$RUNTIME_DIR"
echo "Installed configuration is structurally valid."

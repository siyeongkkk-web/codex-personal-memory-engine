#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
RUNTIME_DIR="$CODEX_DIR/personal-memory"
HOOK_DIR="$CODEX_DIR/hooks"
SKILL_DIR="$CODEX_DIR/skills/personal-memory-engine"

mkdir -p "$RUNTIME_DIR" "$HOOK_DIR" "$CODEX_DIR/skills"

if [ -e "$CODEX_DIR/hooks.json" ]; then
  echo "Refusing to overwrite existing $CODEX_DIR/hooks.json."
  echo "Merge hooks/hooks.template.json manually, replacing __HOOK_SCRIPT__ with $HOOK_DIR/personal_memory_capture.py."
  exit 1
fi

cp -R "$SCRIPT_DIR/templates/personal-memory/." "$RUNTIME_DIR/"
cp "$SCRIPT_DIR/config/config.example.json" "$RUNTIME_DIR/config.json"
cp "$SCRIPT_DIR/hooks/personal_memory_capture.py" "$HOOK_DIR/personal_memory_capture.py"
cp -R "$SCRIPT_DIR/skill/personal-memory-engine" "$SKILL_DIR"
sed "s|__HOOK_SCRIPT__|$HOOK_DIR/personal_memory_capture.py|g" "$SCRIPT_DIR/hooks/hooks.template.json" > "$CODEX_DIR/hooks.json"

echo "Installed local runtime at: $RUNTIME_DIR"
echo "Next: edit $RUNTIME_DIR/config.json and set workspace_scope to one absolute workspace path."
echo "Then restart Codex and trust the two hooks through /hooks."

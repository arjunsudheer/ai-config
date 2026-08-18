#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
USER_HOME="${HOME:?HOME must be set}"

SKILL_SOURCE="$REPO_ROOT/.agents/skills/guided-code-updates"
SKILL_DEST="$USER_HOME/.agents/skills/guided-code-updates"
CODEX_SOURCE="$REPO_ROOT/.codex/agents"
CODEX_DEST="$USER_HOME/.codex/agents"
COPILOT_SOURCE="$REPO_ROOT/.github/agents"
COPILOT_DEST="$USER_HOME/.copilot/agents"

mkdir -p "$SKILL_DEST" "$CODEX_DEST" "$COPILOT_DEST"

cp -R -- "$SKILL_SOURCE/." "$SKILL_DEST/"
cp -- "$CODEX_SOURCE/"*.toml "$CODEX_DEST/"
cp -- "$COPILOT_SOURCE/"*.agent.md "$COPILOT_DEST/"

printf 'Synced guided-code-updates to %s\n' "$SKILL_DEST"
printf 'Synced Codex agents to %s\n' "$CODEX_DEST"
printf 'Synced GitHub Copilot agents to %s\n' "$COPILOT_DEST"

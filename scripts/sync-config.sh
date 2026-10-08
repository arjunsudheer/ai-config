#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
USER_HOME="${HOME:?HOME must be set}"

SKILLS_SOURCE="$REPO_ROOT/.agents/skills"
SKILLS_DEST="$USER_HOME/.agents/skills"
CODEX_SOURCE="$REPO_ROOT/.codex/agents"
CODEX_DEST="$USER_HOME/.codex/agents"
COPILOT_SOURCE="$REPO_ROOT/.copilot/agents"
COPILOT_DEST="$USER_HOME/.copilot/agents"

mkdir -p "$SKILLS_DEST" "$CODEX_DEST" "$COPILOT_DEST"

rsync -a -- "$SKILLS_SOURCE/" "$SKILLS_DEST/"
rsync -a -- "$CODEX_SOURCE/"*.toml "$CODEX_DEST/"
rsync -a -- "$COPILOT_SOURCE/"*.agent.md "$COPILOT_DEST/"

printf 'Synced repository skills to %s\n' "$SKILLS_DEST"
printf 'Synced Codex agents to %s\n' "$CODEX_DEST"
printf 'Synced GitHub Copilot agents to %s\n' "$COPILOT_DEST"

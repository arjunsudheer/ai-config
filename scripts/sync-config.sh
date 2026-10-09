#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
USER_HOME="${HOME:?HOME must be set}"

sync_config() {
	mkdir -p "$2"
	rsync -a -- "$1" "$2"
	printf 'Synced %s to %s\n' "$1" "$2"
}

SKILLS_SOURCE="$REPO_ROOT/.agents/skills"
SKILLS_DEST="$USER_HOME/.agents/skills"
sync_config "$SKILLS_SOURCE/" "$SKILLS_DEST/"

CODEX_AGENTS_SOURCE="$REPO_ROOT/.codex/agents"
CODEX_AGENTS_DEST="$USER_HOME/.codex/agents"
COPILOT_AGENTS_SOURCE="$REPO_ROOT/.copilot/agents"
COPILOT_AGENTS_DEST="$USER_HOME/.copilot/agents"
sync_config "$CODEX_AGENTS_SOURCE/" "$CODEX_AGENTS_DEST/"
sync_config "$COPILOT_AGENTS_SOURCE/" "$COPILOT_AGENTS_DEST/"

HOOKS_SOURCE="$REPO_ROOT/scripts/hooks"
COPILOT_HOOKS_SOURCE="$REPO_ROOT/.copilot/hooks"
COPILOT_HOOKS_DEST="$USER_HOME/.copilot/hooks"
CODEX_HOOKS_SOURCE="$REPO_ROOT/.codex/hooks"
CODEX_HOOKS_DEST="$USER_HOME/.codex"
sync_config "$HOOKS_SOURCE/" "$COPILOT_HOOKS_DEST/"
sync_config "$COPILOT_HOOKS_SOURCE/" "$COPILOT_HOOKS_DEST/"
sync_config "$CODEX_HOOKS_SOURCE/" "$CODEX_HOOKS_DEST/"

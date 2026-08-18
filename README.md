# ai-config

Reusable agent skills and custom subagent definitions for Codex and GitHub Copilot.

## Included configuration

- `guided-code-updates`: A disciplined workflow for researching changes, making the smallest effective implementation, involving documentation and test specialists when useful, and verifying the result.
- `documentor`: Updates relevant project documentation, including the wiki when present, while staying within a delegated scope.
- `test-writer`: Adds, updates, or removes tests for delegated behavior without changing production code.

The repository keeps both supported agent formats:

- `.codex/agents/`: Codex TOML definitions.
- `.github/agents/`: GitHub Copilot Markdown definitions.
- `.agents/skills/`: Shared skill definitions.

## Sync global configuration

Run the sync script from the repository or any other directory:

```bash
./scripts/sync-config.sh
```

The script copies the repository files to the user's global configuration directories:

- `~/.agents/skills/`
- `~/.codex/agents/`
- `~/.copilot/agents/`

Matching files are overwritten so the latest repository changes take effect. Other files already in those directories are preserved, and the repository files remain in place.

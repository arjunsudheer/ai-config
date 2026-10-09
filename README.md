# ai-config

Reusable agent skills and custom subagent definitions for Codex and GitHub Copilot.

## Included configuration

### Skills

- `guided-code-updates`: A disciplined workflow for researching changes, making the smallest effective implementation, involving documentation and test specialists when useful, and verifying the result.
- `solid-review`: Reviews code for meaningful SOLID concerns and proposes evidence-based, incremental refactoring changes without editing code.
- `test-driven-development`: A strict red-green-refactor workflow that delegates test-first coverage, implements and verifies behavior, and updates documentation last.

### Agents

- `documentor`: Updates relevant project documentation, including the wiki when present, while staying within a delegated scope.
- `test-writer`: Adds, updates, or removes tests for delegated behavior without changing production code.

### Hooks

- `.codex/hooks/hooks.json` and `.copilot/hooks/hooks.json`: Codex and GitHub Copilot hook configurations.
- `scripts/hooks/`: Shared Python scripts used by the hooks.

## Sync global configuration

```bash
./scripts/sync-config.sh
```

---
name: guided-code-updates
description: "Use when making code changes and wanting a disciplined workflow: research first, make the smallest effective change, delegate documentation and tests when justified, and verify results before reporting."
---

# Guided Code Updates

## When to Use

- When implementing a feature, fix, or refactor in the codebase.
- When you want a deliberate workflow that balances research, simplicity, and verification.
- When the task may benefit from documentation and test updates but should not overreach.

## Core Pipeline

1. Research before editing
   - For library, framework, SDK, API, CLI, and cloud-service questions, use the Context7 CLI as the primary source for current documentation.
   - If Context7 is unavailable, fails, or is rate-limited, use fetch MCP as the fallback live documentation source and disclose that fallback in the report.
   - If both Context7 and fetch MCP fail, use the most reliable available source or training knowledge, and explicitly warn that the information may be outdated.
   - Search for relevant documentation, existing patterns, and implementation guidance before changing code.
   - Follow the latest documented guidance for the version in use in the codebase.
   - Prefer established best practices over ad hoc approaches.
   - When documentation is not directly available, use the most reliable source available and keep the implementation aligned with surrounding conventions.

2. Make the smallest change that satisfies the request
   - Prefer minimal, straightforward edits over large or overengineered solutions.
   - Keep the implementation simple, clear, and effective.
   - Avoid unnecessary refactors unless they are required for the task.

3. Delegate documentation and tests when justified
   - After the primary change is implemented, consider spawning the `documentor` agent for documentation updates and the `test-writer` agent for tests.
   - Only do this when the change is substantial enough to warrant it.
   - For tiny one-line fixes, it is usually unnecessary to delegate documentation or tests.
   - For moderate or larger changes, delegate documentation and tests when they are relevant to the scope.

4. Verify and report
   - Verify that any documentation or test changes remain within scope and support the requested task.
   - Ensure relevant tests pass before reporting completion.
   - Report the documentation consulted, a concise summary of what changed, and the impact of the change.

## Quality Checks

- The implementation should solve the requested problem directly.
- The change should remain narrow and avoid unrelated edits.
- Documentation should be concise and only added where it genuinely helps.
- Tests should cover the relevant behavior without becoming excessive.

## Output Expectations

Return a short summary that includes:

- the documentation sources consulted
- the main change made
- any delegated documentation or test updates
- the verification performed and the result

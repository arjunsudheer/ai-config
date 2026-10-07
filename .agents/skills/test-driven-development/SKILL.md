---
name: test-driven-development
description: "Use a strict red-green-refactor workflow for changes to public-facing user behavior, with tests written first by the test-writer subagent and documentation handled last by the documentor."
---

# Test-Driven Development

## When to Use

- When implementing or changing public-facing behavior that can be verified with unit tests.
- When the user requests test-driven development or a red-green-refactor workflow.

## Workflow

1. **Understand the behavior before delegating**
   - Inspect the relevant implementation, existing tests, and repository test conventions.
   - For library, framework, SDK, API, CLI, and cloud-service questions, use the Context7 CLI as the primary source for current documentation.
   - If Context7 is unavailable, fails, or is rate-limited, use fetch MCP as the fallback live documentation source and disclose that fallback in the report.
   - If both Context7 and fetch MCP fail, use the most reliable available source or training knowledge, and explicitly warn that the information may be outdated.
   - Search the repository for relevant documentation, established patterns, and implementation guidance before defining expected behavior.
   - Follow the latest documented guidance for the versions and tools in use in the codebase.
   - Define the expected public behavior and the narrow scope of the change. Clarify material ambiguity with the user rather than inventing behavior.
   - Identify relevant edge cases from the behavior and existing contracts; do not add speculative expectations.

2. **Red: delegate tests first**
   - Before changing production code, spawn the `test-writer` subagent with the behavior, scope, and test conventions.
   - Ask it to add or update unit tests for the public-facing behavior, including justified edge cases such as boundary values, invalid inputs, and failure conditions where applicable.
   - The test-writer may edit test files only. It must stay within scope, avoid speculative tests, and remove obsolete negative tests only when existing behavior has changed.
   - Review the test changes, then run the focused tests. Confirm they fail because the requested behavior is missing or incorrect, not because of a test setup or unrelated failure. If the failure is unrelated, resolve the test issue or clarify scope before proceeding; do not treat it as the red result.

3. **Green: implement the behavior**
   - Only after confirming the red result, implement the smallest production change that satisfies the tests.
   - Run the focused tests and verify they pass. If they do not, diagnose and correct the implementation or test issue without weakening valid expectations.

4. **Refactor: improve safely**
   - Once the tests are green, refactor only as useful to improve clarity or design without changing the required behavior.
   - Re-run the focused tests after refactoring. Run broader relevant checks when the change or repository conventions warrant them.
   - Report any test or check that could not be run, including the reason.

5. **Documentation: delegate last**
   - After implementation and verification are complete, spawn the `documentor` subagent with the changed public behavior and a bounded documentation scope.
   - The documentor may edit documentation only, must follow project conventions, and should make concise updates only where they are useful. It may return without edits when no documentation change is warranted.
   - Review its result and report the files it touched, or its reason for making no change.

## Delegation Boundaries

- The `test-writer` writes tests only; the main agent owns production-code changes and test execution.
- The `documentor` updates documentation only and is always delegated after the implementation and test verification.
- Keep both delegations limited to the behavior being changed.

## Output Expectations

Summarize the behavior implemented, tests added or updated (including notable edge cases), the red and green results, any refactoring and its verification, and documentation updates or why none were needed.

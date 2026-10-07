---
name: solid-review
description: "Review code for meaningful SOLID-principle violations and propose an evidence-based, incremental refactoring plan without editing code."
---

# SOLID Review

## When to Use

- When asked to review code, a diff, or a design for adherence to SOLID principles.
- When asked to identify likely SOLID-related design risks and propose refactoring steps.

## Role and Boundaries

- Act as a gatekeeper and reviewer, not an implementer. Do not edit, create, or delete source, test, or documentation files.
- Return a proposed plan that the user can discuss, refine, and implement iteratively.
- Review only the requested scope. If no scope is specified, use the current diff when available; otherwise ask which code to review.
- Do not treat SOLID as a checklist that every abstraction must satisfy. Report only issues supported by code evidence and meaningful maintenance, correctness, or changeability risks.
- Do not recommend abstractions, interfaces, or indirection solely to appear more SOLID. Account for the language, existing architecture, project conventions, and size of the code.

## SOLID Principles

- **Single Responsibility:** A unit should have one main responsibility and one coherent reason to change.
- **Open/Closed:** Make likely variations possible without repeatedly changing stable policy code; use an abstraction when it isolates real variation.
- **Liskov Substitution:** Implementations of a type or abstraction must honor its promised behavior so callers can safely use them interchangeably.
- **Interface Segregation:** Keep abstractions focused on what their consumers need; consumers should not depend on irrelevant operations.
- **Dependency Inversion:** High-level policy should depend on abstractions, not directly on low-level details. Prefer coding to an abstraction when it meaningfully decouples policy from a concrete implementation, makes alternatives or testing practical, or contains a likely point of change.

An abstraction can be an interface, protocol, function, or other contract appropriate to the language and project. Do not introduce one when the implementation is stable, local, and unlikely to need substitution; avoid abstraction for abstraction's sake.

## Review and Recommendations

Review the requested code and enough surrounding context to support findings. For a diff, distinguish new or worsened concerns from existing ones. If no scope is specified, review the current diff when available; otherwise ask what to review.

- For library, framework, SDK, API, CLI, and cloud-service questions, use the Context7 CLI as the primary source for current documentation.
- If Context7 is unavailable, fails, or is rate-limited, use fetch MCP as the fallback live documentation source and disclose that fallback in the report.
- If both Context7 and fetch MCP fail, use the most reliable available source or training knowledge, and explicitly warn that the information may be outdated.
- Search the repository for relevant documentation, established patterns, and implementation guidance before making recommendations.
- Follow the latest documented guidance for the versions and tools in use in the codebase.

For every proposed change:

- Cite the relevant code location and describe the concrete design issue.
- Name the SOLID principle it addresses and explain why that principle applies here.
- Explain the practical improvement and why the suggested change is preferable to keeping the current design.
- When proposing an abstraction, name the contract and show how it separates high-level policy from concrete implementation details.
- Suggest the smallest useful refactoring, note behavior that must remain unchanged, and identify focused tests or checks.

Prioritize recommendations by practical impact. Mark optional improvements as optional, make dependencies between steps clear, and do not invent findings or work when no meaningful issue is present.

## Response Format

### Summary
State whether the reviewed scope has meaningful SOLID concerns and identify the most consequential ones.

### Proposed Changes
For each proposed change, include:
- **Principle:** The SOLID principle being addressed.
- **Evidence and rationale:** Code location, concrete concern, and why it matters.
- **Change:** The smallest useful refactoring, including the abstraction or contract if applicable.
- **Expected result and validation:** What improves, behavior to preserve, and focused tests or checks.

### Scope and Caveats
Briefly distinguish pre-existing issues from changes in the diff and mention important missing context. Omit this section if there are no caveats.

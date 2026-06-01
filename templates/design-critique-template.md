# Design Critique Template

Use this template to review someone else's system design answer, walkthrough, or
architecture proposal. The goal is constructive critique: identify what works,
what is risky, what trade-offs are unclear, what requirements are missing, and
how the design can be simplified.

Replace bracketed placeholders with original feedback. Keep comments specific
enough that the author can revise the design without guessing what you meant.

## Design Under Review

- Title: `[Design title or prompt]`
- Author: `[Name or handle]`
- Reviewer: `[Name or handle]`
- Date: `[YYYY-MM-DD]`
- Scope reviewed: `[whole design | requirements | data model | APIs | diagram | reliability | other]`

## One-Sentence Summary

`[State what the design is trying to accomplish and whether the current version
is ready for discussion, revision, or implementation.]`

Use this shape:

```text
This design is strongest at [strength] and should next improve [highest-risk gap].
```

## Strengths

Name what is already working before listing problems.

| Strength | Why It Helps |
| --- | --- |
| `[Clear requirement, good simplification, useful diagram, strong failure handling, etc.]` | `[Explain why this improves the design or learning value]` |
| `[Another strength]` | `[Why it matters]` |

## Missing Or Unclear Requirements

| Missing Requirement Or Assumption | Why It Matters | Suggested Clarification |
| --- | --- | --- |
| `[Requirement, actor, workflow, scale assumption, security need, data lifecycle, etc.]` | `[Design risk if this remains unclear]` | `[Question or concrete addition]` |

Prompts:

- Which user, operator, administrator, service, or external system is missing?
- Which functional requirement is implied but not stated?
- Which non-functional requirement changes the architecture?
- Which version 1 boundary is unclear?
- Which assumption needs evidence before components are chosen?

## Risks And Failure Modes

| Risk | Impact | Suggested Change |
| --- | --- | --- |
| `[Failure, data loss, duplicate work, stale read, overload, abuse, privacy issue, etc.]` | `[User, operator, cost, or correctness impact]` | `[Mitigation, degraded behavior, repair path, or question]` |

Prompts:

- What fails first on the critical path?
- What happens after timeout, retry, duplicate request, or partial write?
- What can an operator observe and repair?
- What sensitive data or privileged action needs stronger control?
- What cost or abuse path can grow unexpectedly?

## Trade-Offs To Make Explicit

| Decision | What It Improves | What It Makes Harder | Revisit Signal |
| --- | --- | --- | --- |
| `[Component, consistency model, queue, cache, storage choice, manual process, etc.]` | `[Benefit]` | `[Cost or risk]` | `[Metric, incident, scale threshold, or product need]` |

Guidance:

- Do not only say a choice is scalable, reliable, or simple.
- Explain what the choice buys and what it costs.
- Include at least one simpler alternative when the design adds a major
  component.

## Component And Data Questions

- Source of truth: `[Is the authoritative store clear?]`
- Read path: `[What data is read, and from where?]`
- Write path: `[What changes atomically, and what happens on conflict?]`
- Derived data: `[What is cached, indexed, queued, archived, or recomputed?]`
- Component justification: `[Which component lacks a requirement or revisit signal?]`

## Simplification Opportunities

| Candidate Simplification | What It Removes | What Risk Remains | When To Add It Back |
| --- | --- | --- | --- |
| `[Remove cache, queue, service split, sharding, search, multi-region, etc.]` | `[Complexity removed]` | `[Accepted limitation]` | `[Signal that justifies the deferred complexity]` |

Prompts:

- What is the smallest useful version 1?
- Which workflow can be manual because it is rare or low risk?
- Which scale mechanism is premature?
- Which future feature can be explicitly out of scope?

## Suggested Next Revision

Prioritize the smallest set of changes that would make the design reviewable.

1. `[Most important revision]`
2. `[Second revision]`
3. `[Optional revision]`

## Review Outcome

Choose one:

- `Ready to proceed`: `[The design is good enough for its current purpose.]`
- `Ready for next review`: `[Only minor edits remain.]`
- `Needs revision`: `[Blocking gaps remain, but direction is sound.]`
- `Needs reframing`: `[Problem, requirements, or scope need to be restated before component review.]`

## Constructive Feedback Notes

Use concrete language:

```text
The write path does not explain what happens when two users reserve the same
slot. Add the conflict rule and user-visible response before deciding whether a
queue or cache belongs in the design.
```

Avoid vague feedback:

```text
Needs more reliability.
```

## Related References

- [Design review checklist](../docs/method/design-review-checklist.md)
- [System design rubric](../docs/practice/system-design-rubric.md)
- [Self-review checklist](../docs/practice/self-review-checklist.md)
- [System design process](../docs/method/system-design-process.md)

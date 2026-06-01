# Project Reflection Template

Use this template after completing a lab, walkthrough, practice prompt, or docs
page. The goal is to turn the work into reusable system design judgment: what
you learned, which trade-offs you observed, what failed or could fail, and what
you would improve next.

Replace bracketed placeholders with your own notes. Keep answers concrete
enough that a future reader can understand what changed in your reasoning.

## Project

- Title: `[Lab, walkthrough, prompt, or docs page title]`
- Type: `[lab | walkthrough | practice prompt | docs page | other]`
- Date: `[YYYY-MM-DD]`
- Links:
  - Source: `[README, docs page, prompt, or PR link]`
  - Related design pages: `[Relevant cookbook links]`

## One-Sentence Summary

`[State what the exercise taught or what the design explains in one sentence.]`

Use this shape:

```text
This project helped me understand [concept] by showing [behavior, trade-off, or failure].
```

## What I Learned

| Topic | New Understanding | Evidence |
| --- | --- | --- |
| `[Requirement, data, component, failure mode, operation, etc.]` | `[What became clearer]` | `[Lab output, design section, diagram, example, or review finding]` |
| `[Another topic]` | `[What changed in your reasoning]` | `[Evidence]` |

Before and after:

```text
Before this project, I thought:
After this project, I would explain:
```

Prompts:

- Which requirement changed the architecture?
- Which component became more or less justified after the exercise?
- Which hidden assumption did the work expose?
- Which concept can I now explain without looking at the page?

## Trade-Offs Observed

| Decision | Requirement Or Constraint | What It Improved | What It Made Harder | Revisit Signal |
| --- | --- | --- | --- | --- |
| `[Cache, queue, stream, shard, replica, manual process, consistency choice, etc.]` | `[Requirement, bottleneck, failure mode, or operating need]` | `[Benefit]` | `[Cost, risk, or operating burden]` | `[Metric, incident, scale point, or product need]` |

Prompts:

- What did the chosen design buy?
- What did it cost in correctness, latency, freshness, complexity, security,
  operability, or money?
- Which simpler alternative was considered?
- What evidence would justify the more complex version later?

## Failure Modes

| Failure | User Or Operator Impact | System Response | Repair Or Follow-Up |
| --- | --- | --- | --- |
| `[Timeout, duplicate request, stale read, poison message, overload, bad input, etc.]` | `[What someone sees or loses]` | `[Retry, reject, degrade, queue, alert, reconcile, etc.]` | `[Manual repair, replay, runbook, data fix, or next design change]` |

Prompts:

- What failed in the lab or walkthrough?
- What could fail first in the critical path?
- Which invariant is at risk, such as one reservation per slot, one charge per
  order, or one owner per ticket?
- Could retry create duplicate work?
- What does the user see during partial failure?
- What signal tells an operator the issue is happening?

## Lab Reflection

Use this section for runnable labs. If this was not a lab, write `Not
applicable`.

If you paired a lab with a walkthrough or written prompt, complete both this
section and the docs section below.

- Command run: `[Command or commands]`
- Scenario changed: `[Input, rate, failure switch, seed, configuration, etc.]`
- Expected behavior: `[What should happen]`
- Actual behavior: `[What happened]`
- Most useful observation: `[What the output made visible]`
- Metric or signal to watch: `[Counter, latency, queue age, stale read count, error rate, etc.]`
- Design implication: `[How this behavior should affect an architecture decision]`

## Docs Or Walkthrough Reflection

Use this section for docs pages, walkthroughs, and written prompts. If this was
not written design work, write `Not applicable`.

- Problem statement clarity: `[What is clear or still vague]`
- Requirement that shaped the design: `[Requirement and why it matters]`
- Source of truth: `[Authoritative data owner]`
- Main read path: `[Short summary]`
- Main write path: `[Short summary]`
- Component I can justify: `[Component and reason]`
- Component I would remove or defer: `[Component and reason]`
- Diagram or example that helped: `[What it clarified]`

## Version 1 And 10x

| Version 1 Choice | Accepted Limitation | 10x Trigger |
| --- | --- | --- |
| `[Small, practical choice]` | `[What it does not handle yet]` | `[When to revisit]` |

Prompts:

- What is the smallest useful version?
- Which manual step is acceptable for now?
- Which advanced component should wait?
- What measured signal would justify adding it?

## Next Improvements

Prioritize the smallest changes that would improve learning value or design
quality.

1. `[Highest-value improvement]`
2. `[Second improvement]`
3. `[Optional improvement]`

Classify each improvement:

- `clarify requirements`
- `add failure behavior`
- `simplify version 1`
- `add observability`
- `tighten security or abuse handling`
- `improve example or diagram`
- `run or extend lab scenario`
- `reduce cost or operational burden`

## Questions To Revisit

- `[Question about requirements, data ownership, consistency, failure, security, cost, or operations]`
- `[Question about version 1 or 10x scale]`
- `[Question for a reviewer or future learner]`

## Related References

- [Self-review checklist](../docs/practice/self-review-checklist.md)
- [System design rubric](../docs/practice/system-design-rubric.md)
- [Challenge progression](../docs/practice/challenge-progression.md)
- [Common mistakes](../docs/practice/common-mistakes.md)
- [Simplification checklist](../docs/practice/simplification-checklist.md)

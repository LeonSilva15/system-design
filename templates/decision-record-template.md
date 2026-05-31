# Decision Record Template

Use this template to record an architecture decision after the design has enough
context to compare options. Keep it concise: a decision record should explain
why a choice was made, what it costs, and when to revisit it.

This template works for component-level choices, such as adding a queue, and
system-level choices, such as choosing a consistency model or deployment shape.

## Title

`[Short decision name, such as "Use a queue for reminder delivery"]`

## Status

`[Proposed | Accepted | Superseded | Rejected]`

## Date

`[YYYY-MM-DD]`

## Context

`[Describe the problem, requirements, constraints, and assumptions that make this
decision necessary.]`

Prompts:

- Which user workflow or operational problem drives the decision?
- Which functional and non-functional requirements matter?
- What scale, consistency, security, cost, or reliability assumption matters?
- What is in scope for version 1?

## Decision

`[State the chosen option in one direct paragraph.]`

Use this shape:

```text
We will [chosen option] because [requirement or constraint].
```

## Alternatives Considered

| Alternative | Why It Helps | Why Not Now |
| --- | --- | --- |
| `[Alternative 1]` | `[Benefit]` | `[Reason rejected or deferred]` |
| `[Alternative 2]` | `[Benefit]` | `[Reason rejected or deferred]` |

Guidance:

- Describe alternatives fairly.
- Include the simplest credible option.
- Include the more complex option if it is likely to be suggested later.

## Trade-Offs

`[Explain what the decision improves and what it makes worse.]`

Prompts:

- Benefit: `[What gets simpler, faster, safer, cheaper, or more reliable?]`
- Cost: `[What gets slower, more expensive, more complex, or harder to operate?]`
- Risk accepted: `[What could go wrong because of this choice?]`
- Risk reduced: `[What failure or confusion does this choice prevent?]`

## Consequences

`[Describe the practical effects of the decision.]`

Prompts:

- What code, docs, diagrams, or runbooks need to change?
- What must be measured or monitored?
- What new failure mode exists?
- What future option becomes easier or harder?
- What does this mean for version 1?

## Follow-Up

`[List actions, owners if known, and revisit signals.]`

| Follow-Up | Trigger Or Due Date | Notes |
| --- | --- | --- |
| `[Action]` | `[Date, metric, incident, or milestone]` | `[Notes]` |

## Scope

`[Mark the level this decision applies to.]`

- Component-level: `[component, workflow, or page]`
- System-level: `[system, platform, repo architecture, or cross-cutting rule]`

## Related Links

- `[Design doc, checklist, issue, pull request, or related decision]`

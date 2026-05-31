# Style Guide

This guide defines how System Design Decision Cookbook content should sound,
look, and teach.

Use it for docs pages, decision trees, walkthroughs, labs, diagrams, templates,
and review checklists.

## Voice

Write in a practical, decision-oriented voice.

Prefer:

- concrete questions over abstract definitions;
- trade-offs over universal rules;
- version 1 choices before advanced architecture;
- failure modes and operations before polish;
- direct language a backend engineer could use in a design review.

Avoid hype, trivia, and perfect-answer framing. The reader should learn how to
reason, not what architecture to memorize.

## Page Templates

Most documentation pages should use this structure:

```text
# Page Title

## Purpose
## When This Matters
## Questions To Ask
## Decision Guidance
## Trade-Offs
## Common Mistakes
## Example
## Checklist
## Related Pages
```

Decision-tree pages should use this structure:

```text
# Decision Topic

## Purpose
## When This Matters
## Questions To Ask
## Decision Tree
## Decision Guidance
## How To Use The Result
## Trade-Offs
## Common Mistakes
## Example
## Checklist
## Related Pages
```

Walkthroughs should follow the walkthrough standards in
`PROJECT_SOURCE_OF_TRUTH.md` and `AGENTS.md`: problem statement, requirements,
core entities, API sketch, read path, write path, data model, component choices,
diagram, consistency, scaling, failure modes, security, observability, cost,
version 1 simplification, and 10x scale changes.

Labs should keep runnable code in `labs/` and explain what to observe, not just
how to run commands.

## Diagram Style

Use Mermaid by default.

Diagrams should:

- clarify a decision, data flow, state transition, sequence, or failure mode;
- use descriptive node names instead of generic boxes;
- keep the first diagram simple enough to read without zooming;
- show trust boundaries, queues, stores, and async paths when they affect the
  decision;
- avoid vendor logos, copied layouts, decorative complexity, and diagrams that
  merely repeat the prose.

Prefer these diagram types:

- flowcharts for decision paths and architecture overviews;
- sequence diagrams for request or event flows;
- state diagrams for lifecycle and consistency behavior;
- architecture/data-flow diagrams for component relationships;
- failure-mode diagrams for degraded behavior and recovery.

## Examples

Examples should be original and specific.

Good examples include:

- a small product scenario;
- clear functional requirements;
- clear non-functional requirements;
- one or two constraints that force trade-offs;
- a short explanation of why a simpler version 1 is enough.

Avoid examples that are recognizable copies of common course exercises or
company architecture posts.

## Preferred Wording

Prefer this:

```text
Use a queue when the user does not need the work to finish before the response
and the system needs buffering, retries, or worker isolation.
```

Instead of this:

```text
Queues make systems scalable.
```

Prefer this:

```text
If stale reads are acceptable for this page, a cache can reduce database load.
If the page shows account balances or access decisions, prefer a fresh read or a
shorter cache lifetime.
```

Instead of this:

```text
Always cache reads for performance.
```

Prefer this:

```text
For version 1, keep one relational database and add indexes for the two known
query paths. Revisit sharding after write throughput or table size becomes a
measured bottleneck.
```

Instead of this:

```text
Use sharding to handle scale.
```

## Anti-Patterns

Avoid:

- defining a term without showing when it changes a decision;
- presenting one tool or architecture as always correct;
- adding advanced distributed systems machinery before requirements justify it;
- hiding trade-offs behind vague words like scalable, reliable, robust, or
  production-ready;
- copying the sequence, examples, diagrams, or exercises of a book, course, or
  article;
- writing a walkthrough as a final answer instead of a chain of decisions;
- adding a diagram that does not clarify a choice or failure mode;
- ignoring observability, security, cost, or version 1 simplification.

## Formatting

Use Markdown with clear headings and short sections.

- Use title case for standard template headings and sentence case for long
  explanatory headings.
- Use bullet lists for scan-friendly prompts and checklists.
- Use tables only when comparison is clearer than prose.
- Use fenced code blocks for APIs, schemas, commands, Mermaid, and examples.
- Keep links descriptive: prefer `capacity estimation guide` over `click here`.
- Keep pages vendor-neutral unless the page explicitly compares products.

## Review Standard

Before merging, ask:

- Does this page help a reader make a decision?
- Are the requirements and trade-offs explicit?
- Is the example original and useful?
- Is the diagram original and necessary?
- Does the page explain what can fail?
- Does it show how to observe, operate, or simplify the system?
- Does it respect `CONTENT_GUARDRAILS.md`?

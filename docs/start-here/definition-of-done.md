# Definition of Done

Use this checklist before merging cookbook content. It applies to documentation,
decision trees, walkthroughs, labs, diagrams, and templates.

The goal is not to make every page long. The goal is to make every contribution
clear, original, scoped, and useful for system design reasoning.

## Applies To Every Contribution

- The change satisfies the ticket acceptance criteria.
- The diff is scoped to the ticket deliverable path and necessary navigation.
- The content follows [Content guardrails](https://github.com/LeonSilva15/system-design/blob/main/CONTENT_GUARDRAILS.md).
- The writing follows [Style guide](https://github.com/LeonSilva15/system-design/blob/main/STYLE_GUIDE.md).
- The work does not copy or closely paraphrase books, courses, articles,
  diagrams, tables, screenshots, or exercises.
- Related pages, section indexes, or navigation files are updated when they
  already exist.
- Available checks are run, or missing checks are clearly recorded.

## Documentation Pages

A documentation page is done when it includes the pieces that fit the topic:

- purpose;
- when this matters;
- questions to ask;
- decision guidance;
- trade-offs;
- common mistakes;
- original example;
- checklist;
- related pages.

It should explain how a reader makes a decision, not just define a term.

## Decision Trees

A decision tree is done when it:

- starts with the requirement or constraint that triggers the decision;
- includes a Mermaid flowchart when a visual tree improves understanding;
- names the outcome of each major branch;
- explains how to use the result after the tree;
- includes trade-offs and common mistakes;
- includes an original example;
- links related requirement, component, or method pages.

Decision trees should help readers narrow choices, not pretend one choice is
always correct.

## Walkthroughs

A walkthrough is done when it covers:

- problem statement;
- functional and non-functional requirements;
- core entities;
- API sketch;
- read path and write path;
- data model;
- component choices and alternatives;
- architecture diagram;
- consistency decisions;
- scaling strategy;
- failure modes;
- security concerns;
- observability;
- cost considerations;
- version 1 simplification;
- what changes at 10x scale.

It should show reasoning and trade-offs instead of presenting a perfect final
answer.

## Labs

A lab is done when it is small, runnable, and educational.

It should include:

- `README.md`;
- `design.md`;
- `how-to-run.md`;
- implementation code;
- tests or a demo script;
- `expected-output.md`;
- `what-to-observe.md`;
- `tradeoffs.md`.

The lab should demonstrate behavior the learner can observe. It should not grow
into a production framework.

The expected output should make success, failure, and the relevant design
behavior visible without requiring hidden setup or production services.

## Diagrams

A diagram is done when it:

- is original Mermaid;
- clarifies a decision, flow, state transition, architecture/data-flow
  relationship, or failure mode;
- uses readable node labels;
- shows queues, stores, trust boundaries, or async paths when they matter;
- avoids copied layouts, vendor logos, screenshots, and decorative complexity;
- is explained by the surrounding text.

If the same idea is clearer in prose, skip the diagram.

## Originality Checks

Before merging, confirm:

- examples are invented for this project;
- diagrams are original and not recreated from another source;
- external sources are cited only for specific factual claims;
- citations do not hide copied wording, structure, tables, or diagrams;
- the page is not a substitute for a book, course, or paid learning material.

When uncertain, replace the material with a smaller original example or ask for
human review.

## Links, Examples, And Trade-Offs

Every content page should ask:

- Does the page link to the closest related method, requirement, component, or
  practice page when one exists?
- Does the example make an abstract idea concrete?
- Does the page state what the design choice improves?
- Does the page state what the design choice makes worse, harder, slower, more
  expensive, or riskier?
- Does it explain how version 1 can be simpler?

## Review Criteria

Reviewers should check:

- scope matches the ticket;
- acceptance criteria are satisfied;
- content is original;
- requirements and trade-offs are explicit;
- rejected alternatives are explained enough for the reader to understand why
  they were not chosen;
- failure modes, observability, security, cost, or simplification are included
  when relevant;
- links and navigation targets exist;
- checks were run or missing checks are noted.

Blocking feedback should identify the file, line, and concrete issue.
Non-blocking feedback should be small, optional, and tied to learning value.

## Related Pages

- [Project guardrails](project-guardrails.md)
- [Content guardrails](https://github.com/LeonSilva15/system-design/blob/main/CONTENT_GUARDRAILS.md)
- [Style guide](https://github.com/LeonSilva15/system-design/blob/main/STYLE_GUIDE.md)
- [Contributing](https://github.com/LeonSilva15/system-design/blob/main/CONTRIBUTING.md)

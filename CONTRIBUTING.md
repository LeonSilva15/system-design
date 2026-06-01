# Contributing

The System Design Decision Cookbook is a public learning resource. Contributions
should make it easier for readers to move from requirements to justified system
design decisions.

Before contributing, read:

- [PROJECT_SOURCE_OF_TRUTH.md](PROJECT_SOURCE_OF_TRUTH.md)
- [AGENTS.md](AGENTS.md)
- [CONTENT_GUARDRAILS.md](CONTENT_GUARDRAILS.md)
- [STYLE_GUIDE.md](STYLE_GUIDE.md)
- [system_design_decision_cookbook_tickets.csv](system_design_decision_cookbook_tickets.csv)

## Source Of Truth

Use this order when instructions conflict:

1. Current human instruction.
2. `AGENTS.md` for contribution workflow.
3. `PROJECT_SOURCE_OF_TRUTH.md` for mission, architecture defaults, and scope.
4. `system_design_decision_cookbook_tickets.csv` for ticket-specific scope.
5. Local templates and style guidance.

If a conflict affects scope, copyright safety, architecture, or public quality,
stop and ask for review instead of guessing.

## Ticket Workflow

Work from one ticket at a time.

The CSV backlog is the canonical ticket source. GitHub issues, project items,
and pull requests are tracking and review artifacts unless the project changes
that workflow.

For each ticket:

1. Read the ticket row in `system_design_decision_cookbook_tickets.csv`.
2. Confirm dependencies are complete.
3. Use `deliverable_path`, `acceptance_criteria`, `dependencies`, and
   `recommended_milestone` as the scope boundary.
4. Inspect directly related files before editing.
5. Make the smallest change that satisfies the acceptance criteria.
6. Run available checks and record anything missing.
7. Open a focused pull request.

Do not use a ticket to rewrite unrelated pages or invent new project scope.

## Branch And Commit Workflow

Use a branch named exactly like the ticket ID when possible:

```text
SDC-E01-T05
```

Use Conventional Commit subjects that include the ticket ID:

```text
docs(contributing): SDC-E01-T05 create contribution guide
chore(structure): SDC-E01-T02 create repository skeleton
feat(lab): SDC-E12-T02 add token bucket lab
```

Keep commits focused. If a review fix is needed, make a small follow-up commit
with the same ticket ID.

## Pull Request Workflow

Every pull request should include:

- ticket ID and issue or project link when one exists;
- summary of changes;
- acceptance criteria checklist;
- checks run;
- notes on missing checks, dependencies, originality, and learning value.

Before requesting review, confirm:

- the diff only touches files needed for the ticket;
- content follows `CONTENT_GUARDRAILS.md`;
- writing follows `STYLE_GUIDE.md`;
- related navigation or index files are updated when they already exist;
- diagrams are Mermaid and original;
- labs include run instructions and tests or demo output when the lab ticket
  requires them.

## Review Process

Review should focus on correctness, scope, originality, and learning value.

Reviewers should check:

- the ticket acceptance criteria are satisfied;
- dependencies and scope boundaries are respected;
- explanations are original and not close paraphrases;
- trade-offs and failure modes are explicit where relevant;
- examples are concrete and useful;
- diagrams clarify a decision, flow, or failure mode;
- checks were run or missing checks are clearly explained.

Address blocking feedback before merge. Non-blocking feedback can be handled in
the same pull request when it is small and in scope; otherwise record it for a
future ticket.

## Content Contributions

Documentation should teach reusable reasoning. Prefer:

- questions that reveal requirements;
- guidance that connects requirements to component choices;
- explicit trade-offs;
- common mistakes;
- original examples;
- checklists a reader can apply to their own design.

Avoid copied source structure, generic definitions with no decision impact, and
one-size-fits-all architecture advice.

## Lab Contributions

Labs live under the top-level `labs/` directory. A lab should demonstrate
observable behavior, not become a production framework.

A complete lab should include:

- `README.md`;
- `design.md`;
- `how-to-run.md`;
- implementation code;
- tests or a demo script;
- `expected-output.md`;
- `what-to-observe.md`;
- `tradeoffs.md`.

Prefer Python and pytest unless the source of truth changes. Keep dependencies
small and explain what the learner should observe.

## Diagram Contributions

Use Mermaid by default.

Diagrams should be original and should clarify:

- a decision path;
- a request or event sequence;
- a state transition;
- an architecture/data-flow relationship;
- a failure mode or recovery path.

Do not copy diagrams, screenshots, layout, labels, or teaching sequence from
external sources.

## Checks

Prefer these setup and preview commands when they exist:

```bash
make install
make docs-serve
```

Prefer these check commands when they exist:

```bash
make docs-build
make test
make lint
```

If a command does not exist yet, do not claim it passed. Run focused checks that
fit the change and explain what project-level checks are unavailable.

## Docs Site Deployment

The documentation site is built with MkDocs Material and deployed by GitHub
Actions. In the repository settings, GitHub Pages must use **GitHub Actions** as
the source. Do not switch Pages to deploy from a branch unless the source of
truth is updated first.

## Final Quality Bar

Before merging, the contribution should answer:

- What problem does this help the reader solve?
- Which requirements or trade-offs does it clarify?
- What can fail or be misunderstood?
- How can the reader observe, operate, or simplify the design?
- Is the work original and scoped to the ticket?

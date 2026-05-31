# Roadmap

This roadmap explains how the System Design Decision Cookbook grows from a
safe repository foundation into a useful learning resource.

The canonical backlog is
[`system_design_decision_cookbook_tickets.csv`](system_design_decision_cookbook_tickets.csv).
Use that file for ticket IDs, dependencies, suggested order, milestone
assignment, MVP flags, deliverable paths, and acceptance criteria.

## Sequencing Principles

Work proceeds in dependency order, not by topic preference.

- Build the contribution and publishing guardrails first.
- Add the reusable method before deep topic pages.
- Create decision-tree templates before writing large batches of trees.
- Add walkthrough and lab foundations before expanding examples.
- Keep production-depth content after the MVP learning path is useful.
- Use the CSV backlog as the source for scope and ordering.

## MVP Cut

The MVP is the smallest useful public version of the cookbook. It should let a
reader:

- understand the project mission and contribution boundaries;
- follow a repeatable system design process;
- discover important requirements;
- choose common components with trade-offs;
- read at least a few worked walkthroughs;
- run or inspect a small set of educational labs;
- use rubrics and checklists for self-review.

The MVP is represented by tickets with `mvp = TRUE` in the backlog. The current
CSV marks 43 tickets as MVP work across M0, M1, M2, and M3; update this count
when the CSV changes.

Release language maps to milestones this way:

- **MVP:** M0-M3 tickets marked `mvp = TRUE`.
- **v1:** M4 production-depth material after the MVP learning path works.
- **v2 and long-term:** M5 expansion, polish, and automation.

## Recommended Milestones

### M0 - Repository Foundation

Purpose: make the repository safe, navigable, and ready for consistent
contributions.

Includes:

- project identity and README;
- folder structure;
- content guardrails, style guide, contribution guide, license, and roadmap;
- starter glossary and definition of done;
- reusable design and decision-record templates;
- basic GitHub issue and PR workflow documents.

Exit condition: contributors can understand what the project is, what is in
scope, how to contribute, and how to avoid unsafe copied content.

### M1 - Cookbook MVP

Purpose: create the core method and decision-tree content for the MVP learning
path. The full MVP cut still spans M0-M3 through tickets marked `mvp = TRUE`.

Includes:

- system design process;
- requirement discovery and scale estimation;
- trade-off vocabulary and design review checklist;
- requirement decision trees;
- component selection decision trees for APIs, services, databases, caches,
  queues, streams, object storage, CDN, background workers, and load balancers.

Exit condition: a reader can move from a prompt to requirements, component
choices, trade-offs, and a review checklist without needing the later deep-dive
pages.

### M2 - First Applied Systems

Purpose: connect the method and decision trees to worked examples and visual
standards.

Includes:

- walkthrough template and index;
- first walkthroughs such as URL shortener, rate limiter, and notification
  system;
- diagram style guide;
- decision-tree template;
- repository navigation index and learning paths.

Exit condition: the cookbook has an end-to-end learner path from method pages
to applied system walkthroughs.

### M3 - Active Learning Labs

Purpose: add runnable or inspectable exercises that show system behavior.

Includes:

- lab standards and harness;
- rate limiter, queue worker, retry/idempotency, and replication lag labs;
- system design rubric and self-review checklist.

Exit condition: learners can observe behavior, compare it with docs guidance,
and review their own decisions.

### M4 - Production Depth

Purpose: deepen the cookbook with data, communication, scalability,
reliability, security, operations, and cost topics.

Includes:

- data modeling, indexes, transactions, consistency, replication, sharding,
  backups, and retention;
- synchronous and asynchronous communication patterns;
- scaling, bottleneck analysis, caching, backpressure, and rate limiting;
- failure analysis, timeouts, retries, circuit breakers, failover, and recovery;
- security, privacy, authentication, authorization, and abuse resistance;
- observability, metrics, logs, traces, alerting, runbooks, SLOs, and cost.

Exit condition: the cookbook can support deeper production-oriented design
reviews after the MVP path is already useful.

### M5 - Expansion And Polish

Purpose: broaden examples, polish practice material, and add automation.

Includes:

- additional walkthroughs and labs;
- diagram examples and templates;
- interview prompts, flashcards, design critique templates, and simplification
  checklists;
- docs automation such as link checks, taxonomy validation, changelog process,
  and contribution quality checks.

Exit condition: the project has enough breadth and tooling to support ongoing
public contributions.

## What To Work On Next

Use this default order:

1. Pick the lowest `suggested_order` ticket whose dependencies are done.
2. Prefer MVP tickets when dependency order allows.
3. Keep each pull request scoped to one ticket.
4. Stop when a ticket requires a new legal, architecture, hosting, or tooling
   decision that is not already recorded.

## What Is Out Of Scope For Early Milestones

Do not add these before the static learning resource is useful:

- custom backend;
- login system;
- database-backed progress tracker;
- vendor-specific certification path;
- production infrastructure framework;
- copied course or book summaries.

## Related Files

- [Project source of truth](PROJECT_SOURCE_OF_TRUTH.md)
- [Ticket backlog](system_design_decision_cookbook_tickets.csv)
- [Content guardrails](CONTENT_GUARDRAILS.md)
- [Style guide](STYLE_GUIDE.md)
- [Contributing](CONTRIBUTING.md)

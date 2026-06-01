# Project Management

## Purpose

Use this page to understand how cookbook work is labeled, prioritized, staged,
and moved through review. It translates the CSV backlog and GitHub Project into
a shared vocabulary for contributors.

The canonical backlog remains
[`system_design_decision_cookbook_tickets.csv`](https://github.com/LeonSilva15/system-design/blob/main/system_design_decision_cookbook_tickets.csv).
Use this page to interpret labels, milestones, priorities, difficulty, status,
and good-first-issue signals.

## When This Matters

Use this page when:

- choosing the next ticket to work on;
- creating a new issue or project item;
- reviewing whether a ticket is scoped correctly;
- deciding whether a contribution is beginner-friendly;
- mapping roadmap milestones to project phases.

## Label Families

Labels should describe the work without replacing the ticket acceptance
criteria. A good label helps filtering. The ticket body still defines scope.

| Family | Format | Meaning | Examples |
| --- | --- | --- | --- |
| Epic | `epic:<area>` | The broad cookbook area the work belongs to | `epic:method`, `epic:requirements`, `epic:repo-quality` |
| Type | `type:<kind>` | The kind of deliverable or review surface | `type:doc`, `type:decision-tree`, `type:walkthrough`, `type:lab`, `type:practice`, `type:ops` |
| Priority | `priority:p0` to `priority:p2` | How important the work is to the roadmap and dependency chain | `priority:p0`, `priority:p1`, `priority:p2` |
| Difficulty | `difficulty:<level>` | How much context a contributor needs | `difficulty:beginner`, `difficulty:intermediate`, `difficulty:advanced` |
| Status | `status:<state>` | Optional issue label mirror of project board state | `status:todo`, `status:in-progress`, `status:in-review`, `status:blocked`, `status:done` |
| Good first issue | `good-first-issue` | Small, well-scoped work with clear acceptance criteria | `good-first-issue` |

Use lowercase labels with hyphens. Epic, type, and priority are normal triage
labels. Difficulty is useful when contributor fit matters. Status labels and
`good-first-issue` are conditional.

## CSV Fields Versus GitHub Labels

The CSV backlog uses compact field values. GitHub labels use lowercase names.

| CSV Field | Example CSV Value | GitHub Label |
| --- | --- | --- |
| `priority` | `P0` | `priority:p0` |
| `type` | `OPS` | `type:ops` |
| `type` | `VIS` | `type:visual` |
| `epic_id` and `epic_name` | `E15`, Repository Quality | `epic:repo-quality` |
| `status` | `Blocked by dependencies` | Usually no issue label; see status mapping below |

When labels and CSV values disagree, use the CSV and project board as the source
of truth, then update labels to match.

## Epic Labels

Use epic labels to group work by learning area.

| Label | Area |
| --- | --- |
| `epic:identity` | Project identity, source of truth, guardrails, and publishing basics |
| `epic:method` | Universal system design process, templates, and review method |
| `epic:requirements` | Requirement discovery decision trees |
| `epic:components` | Component selection decision trees |
| `epic:data` | Data modeling, consistency, transactions, replication, and storage lifecycle |
| `epic:communication` | Sync, async, APIs, queues, streams, retries, and idempotency |
| `epic:scalability` | Capacity, caching, sharding, load balancing, hot keys, and backpressure |
| `epic:reliability` | Failure modes, timeouts, retries, failover, disaster recovery, and degradation |
| `epic:security` | Authentication, authorization, privacy, audit, abuse, and compliance |
| `epic:operations` | Observability, metrics, logs, traces, alerts, runbooks, SLOs, and cost |
| `epic:walkthroughs` | End-to-end system design walkthroughs |
| `epic:labs` | Runnable labs and simulations |
| `epic:visuals` | Diagram standards, examples, and visual templates |
| `epic:practice` | Rubrics, prompts, flashcards, critique templates, and learning loops |
| `epic:repo-quality` | Issue templates, PR templates, checks, release notes, and automation |

## Type Labels

Use type labels to describe what the contributor will change.

| Label | Use For |
| --- | --- |
| `type:doc` | Documentation pages, guides, glossaries, and start-here material |
| `type:decision-tree` | Requirement or component decision trees |
| `type:walkthrough` | End-to-end system design walkthroughs |
| `type:lab` | Runnable labs, simulators, tests, and lab docs |
| `type:practice` | Rubrics, prompts, checklists, templates, and learning exercises |
| `type:visual` | Diagram standards, Mermaid examples, visual templates, and visual review pages |
| `type:ops` | Repository workflow, automation, release management, and GitHub configuration |

If a ticket touches multiple surfaces, use the label for the primary
deliverable path.

The issue templates also use `type:diagram` and `type:correction` for incoming
GitHub issues. If one of those issues becomes a backlog ticket, map it to the
closest canonical backlog type. For example, a diagram template request usually
maps to `type:visual`, while a correction maps to the type of the page or lab
being corrected.

## Priority Labels

Priority describes sequencing importance, not personal preference.

| Label | Meaning | Typical Use |
| --- | --- | --- |
| `priority:p0` | Critical foundation or dependency | Source-of-truth pages, core method, MVP walkthroughs, lab standards, repo workflow |
| `priority:p1` | Important next layer | Production-depth pages, additional labs, practice material, quality improvements |
| `priority:p2` | Useful expansion or polish | Extra walkthroughs, advanced practice, release polish, optional automation |

Do not use priority to skip dependencies. A lower-priority ticket with satisfied
dependencies can be worked before a blocked P0 ticket.

## Difficulty Labels

Difficulty is about contributor context, not topic prestige.

| Label | Use When |
| --- | --- |
| `difficulty:beginner` | The change is narrow, has a clear template, and can be completed by reading a few related files |
| `difficulty:intermediate` | The change requires understanding several related pages, trade-offs, or lab behavior |
| `difficulty:advanced` | The change affects broad architecture guidance, cross-page consistency, automation, or correctness-sensitive examples |

Good first issues should usually be `difficulty:beginner`, but not every
beginner issue is automatically good-first-issue.

## Status Labels, CSV Status, And Project Status

The CSV backlog records dependency readiness. The GitHub Project status field
tracks execution state after tickets are imported. Use status labels only when
mirroring state on GitHub issues is helpful.

| CSV Status | Project Status | Optional Label | Meaning |
| --- | --- | --- | --- |
| `Ready` | `To Do` | `status:todo` | Dependencies are ready or the item is waiting for selection |
| `Blocked by dependencies` | `Blocked` or skipped by selection | `status:blocked` | A dependency must finish before work starts |
| Not represented in CSV | `In progress` | `status:in-progress` | A contributor is actively working on the scoped deliverable |
| Not represented in CSV | `In review` | `status:in-review` | A pull request is open and awaiting checks or review |
| Not represented in CSV | `Done` | `status:done` | The PR is merged and the project item is complete |

When status labels and the project board disagree, update the project board
first.

## Good-First-Issue Criteria

Use `good-first-issue` only when the issue is genuinely safe for a new
contributor.

It should have:

- one clear deliverable path;
- no unresolved product or architecture question;
- satisfied dependencies;
- an existing template or nearby page to follow;
- narrow acceptance criteria;
- low risk of copyright or originality mistakes;
- focused checks that can be run locally;
- no need to modify broad navigation, automation, or multiple lab packages.

Avoid `good-first-issue` for work that requires inventing a new standard,
settling disputed technical guidance, or editing many cross-linked pages.

## Milestones And Project Phases

Milestones describe roadmap phases from the
[Roadmap](https://github.com/LeonSilva15/system-design/blob/main/ROADMAP.md). They should match the `recommended_milestone`
column in the backlog.

| Milestone | Project Phase | Purpose | Exit Signal |
| --- | --- | --- | --- |
| `M0 - Repository Foundation` | Foundation | Make the repository safe, navigable, and ready for consistent contribution | Contributors understand scope, guardrails, workflow, and templates |
| `M1 - Cookbook MVP` | Core method | Build the process and decision-tree material needed for the MVP learning path | Readers can move from prompt to requirements, components, trade-offs, and review |
| `M2 - First Applied Systems` | Applied examples | Connect method pages to walkthroughs and visual standards | Readers can follow an end-to-end system design path |
| `M3 - Active Learning Labs` | Active learning | Add runnable labs and self-review practice | Learners can observe behavior and critique their own designs |
| `M4 - Production Depth` | Deepening | Add production-oriented data, communication, reliability, security, operations, and cost material | The cookbook supports deeper architecture reviews |
| `M5 - Expansion and Polish` | Breadth and quality | Add more examples, practice material, diagrams, automation, and release process | The project supports ongoing public contribution and maintenance |

## Label Examples

Use these as patterns, not as extra process.

| Work | Suggested Labels |
| --- | --- |
| Small docs clarification for a beginner-friendly page | `epic:method`, `type:doc`, `priority:p1`, `difficulty:beginner`, `good-first-issue` |
| Advanced lab change with runnable behavior and tests | `epic:labs`, `type:lab`, `priority:p1`, `difficulty:advanced` |
| Visual standards or diagram review work | `epic:visuals`, `type:visual`, `priority:p1`, `difficulty:intermediate` |

Release language maps to milestones this way:

- **MVP:** M0-M3 tickets marked `mvp = TRUE`.
- **v1:** M4 production-depth content after the MVP learning path is useful.
- **v2 and long-term:** M5 expansion, polish, and automation.

## Ticket Selection Rules

When choosing work:

1. Use the project board and CSV backlog together.
2. Prefer the lowest `suggested_order` item whose dependencies are `Done`.
3. Confirm no in-progress item overlaps the same deliverable path.
4. Use the ticket's deliverable path, acceptance criteria, dependencies, and
   milestone as the scope boundary.
5. Keep one PR focused on one ticket.

## Common Mistakes

- Treating labels as scope instead of reading the ticket body.
- Marking broad, cross-cutting work as `good-first-issue`.
- Using priority to bypass dependency order.
- Creating new label names when an existing family already fits.
- Moving project status without a matching PR or clear blocker.
- Adding automation or repo policy beyond the ticket acceptance criteria.

## Checklist

Before creating or triaging an issue, confirm:

- It has one primary deliverable path.
- It has an epic label and type label.
- Priority reflects dependency and roadmap importance.
- Difficulty reflects contributor context.
- `good-first-issue` is used only for narrow, safe work.
- Milestone matches the project phase.
- Acceptance criteria are concrete enough to review.
- Dependencies and blockers are visible.

## Related Pages

- [Start here](./)
- [Definition of done](definition-of-done.md)
- [Project guardrails](project-guardrails.md)
- [How to use this cookbook](how-to-use-this-cookbook.md)
- [Roadmap](https://github.com/LeonSilva15/system-design/blob/main/ROADMAP.md)
- [Contributing](https://github.com/LeonSilva15/system-design/blob/main/CONTRIBUTING.md)

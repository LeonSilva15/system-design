# Contribution Quality Dashboard

## Purpose

Use this dashboard to track repository coverage and review risk. It summarizes
which cookbook areas are represented, which quality checks currently pass, and
which gaps should be reviewed before future releases.

This page is a manual dashboard. Update it after large batches of content,
labs, walkthroughs, diagrams, or automation merge. The tables are intentionally
simple enough to review in a pull request.

## When This Matters

Use this dashboard when:

- preparing a release note or roadmap update;
- deciding which epic needs more examples, labs, or diagrams;
- reviewing whether a new page is orphaned;
- checking if labs still include the required learner files;
- looking for stale pages after templates, standards, or navigation change;
- auditing whether walkthroughs still satisfy the required structure.

## Snapshot

Snapshot date: `2026-06-01`.

| Signal | Current State | How To Refresh |
| --- | --- | --- |
| Project items | 171 total; 170 Done and `SDC-E15-T09` not yet Done as of this snapshot | `python3 skills/ticket-runner/scripts/project_board.py snapshot` |
| Docs pages | 146 Markdown files under `docs/` after this page is added | `scripts/check-taxonomy` |
| Section index coverage | Start-here index includes this dashboard | `scripts/generate-index --check docs/start-here` |
| Labs | 10 runnable lab directories; all have expected docs and tests | See lab completeness checklist below |
| Walkthroughs | 10 walkthrough pages; all include required walkthrough sections | `scripts/check-taxonomy docs/walkthroughs` |
| Mermaid coverage | Component, requirement, and walkthrough pages all include Mermaid diagrams | See diagram coverage checklist below |

After this ticket merges, the original 171-item project backlog should have no
remaining To Do items unless new project items are added.

## Coverage By Epic

This table tracks the backlog coverage signal by epic. It uses the original
ticket backlog count plus the current repository surface for that epic.

| Epic | Area | Backlog Items | Current Coverage Signal | Watch Next |
| --- | --- | ---: | --- | --- |
| E01 | Project identity, scope, and guardrails | 9 | Repository identity, guardrails, license, roadmap, glossary, and definition of done are present | Recheck links after publishing setup changes |
| E02 | Universal system design process | 10 | Method docs and reusable templates are present | Keep beginner guidance aligned with learning paths |
| E03 | Requirement discovery decision trees | 12 | Requirements index plus focused requirement trees are present | Watch for stale examples when new walkthroughs are added |
| E04 | Core component decision trees | 13 | Component map and component decision trees are present | Keep component pages aligned with taxonomy validator rules |
| E05 | Data modeling, storage, and consistency | 13 | Data section covers modeling, access patterns, consistency, replication, sharding, backups, and retention | Add release review when storage guidance changes |
| E06 | Communication, async work, and workflow patterns | 13 | Communication section covers sync/async, queues, streams, retries, idempotency, outbox, saga, DLQ, and workflow patterns | Keep retry and workflow pages aligned with labs |
| E07 | Scalability and performance playbooks | 13 | Scalability section covers capacity, bottlenecks, caching, scaling, sharding, hot keys, rate limits, and testing | Watch for examples that need updated scale assumptions |
| E08 | Reliability, failure modes, and recovery | 13 | Reliability section covers timeouts, retries, circuit breakers, bulkheads, failover, disaster recovery, RPO/RTO, health checks, and degradation | Recheck incident and recovery examples after new labs |
| E09 | Security, privacy, and abuse resistance | 12 | Security section covers authn/authz, privacy, audit logs, admin tools, secrets, encryption, retention, abuse, and integrations | Watch for stale security assumptions and missing citations where factual claims need them |
| E10 | Observability, operations, and cost | 13 | Operations section covers observability, metrics, logs, traces, alerting, dashboards, runbooks, SLOs, capacity, and cost | Keep runbook examples aligned with content review workflow |
| E11 | End-to-end design walkthroughs | 11 | Walkthrough index plus 10 complete walkthroughs are present | Add future systems only when they show distinct trade-offs |
| E12 | Hands-on labs and simulations | 11 | Lab standards plus 10 runnable lab directories are present | Keep lab expected output aligned with implementation behavior |
| E13 | Diagrams, visual language, and navigation | 9 | Diagram guide, legend, examples, templates, review checklist, repository index, and learning paths are present | Keep Mermaid examples aligned with style guide |
| E14 | Review rubrics, self-testing, and learning loops | 10 | Practice pages and reflection/critique templates are present | Review challenge progression when new labs or walkthroughs are added |
| E15 | Repository quality, automation, and release management | 9 | Issue/PR templates, project management, docs checks, index generator, taxonomy checker, changelog, content review workflow, and this dashboard are present | Refresh this dashboard before release notes |

## Diagram Coverage

Current signal:

- component decision pages: no missing Mermaid diagrams found;
- requirement decision pages: no missing Mermaid diagrams found;
- walkthrough pages: no missing Mermaid diagrams found.

Use this review queue for future changes:

| Page Type | Diagram Expected When | Missing Diagram Action |
| --- | --- | --- |
| Requirement decision tree | Branches are easier to follow visually than in prose | Add original Mermaid flowchart or explain why prose is clearer |
| Component decision tree | A choice depends on multiple requirements, failure modes, or trade-offs | Add original Mermaid flowchart tied to the decision guidance |
| Walkthrough | The reader needs to see component relationships, data flow, or failure path | Add original Mermaid architecture or data-flow diagram |
| Practice, rubric, or checklist | A workflow or progression is hard to scan as text | Add Mermaid only if it clarifies the review path |

Do not add diagrams as decoration. A missing diagram matters only when it would
make a decision, flow, or failure mode clearer.

## Lab Completeness

The current lab directories are:

- `cache-aside-demo`
- `dead-letter-queue-demo`
- `hot-key-demo`
- `log-compaction-demo`
- `queue-worker-demo`
- `quorum-read-write-simulator`
- `rate-limiter`
- `replication-lag-simulator`
- `retry-idempotency-demo`
- `sharding-simulator`

Current signal: all listed labs include the expected learner docs and tests.

Missing lab queue:

| Area Or Page | Missing Lab Signal | Why It Matters | Follow-Up |
| --- | --- | --- | --- |
| None currently recorded | Not applicable | No current epic has a recorded missing-lab gap in this dashboard | Not applicable |

Use this checklist when adding or changing a lab:

- `README.md` explains the learning goal.
- `design.md` explains the design choices.
- `how-to-run.md` gives runnable commands.
- implementation code is present.
- tests or a demo script are present.
- `expected-output.md` shows success and relevant behavior.
- `what-to-observe.md` explains the behavior to inspect.
- `tradeoffs.md` names what the lab simplifies or makes harder.

## Stale Page Watchlist

This repository does not yet have page ownership or last-reviewed metadata. Use
this manual watchlist until that exists.

| Stale Signal | Why It Matters | Review Action |
| --- | --- | --- |
| A template changes | Existing pages may no longer match the expected structure | Run `scripts/check-taxonomy` and update pages only when the mismatch affects learning value |
| A lab implementation changes | Expected output or observations may drift | Rerun the lab tests or demo and update lab docs |
| A navigation page changes | New pages can become orphaned | Run `scripts/generate-index --check` for the affected section |
| A security, privacy, compliance, or vendor-specific claim changes | Guidance may become wrong or need citation | Recheck source-backed claims and record updates in the changelog |
| A walkthrough adds a component or changes a requirement | Related decision pages may need cross-links or example updates | Review related pages and add links only where useful |

Current known stale pages: none identified by the available link, taxonomy, and
index checks. This does not prove the content is fresh; it means no stale page
has been recorded in this dashboard yet.

## Walkthrough Completeness

Current signal: all 10 walkthrough pages include the required walkthrough
sections.

Required walkthrough sections:

- problem statement;
- functional requirements;
- non-functional requirements;
- core entities;
- API sketch;
- read path;
- write path;
- data model;
- component choices;
- architecture diagram;
- consistency decisions;
- scaling strategy;
- failure modes;
- security concerns;
- observability;
- cost considerations;
- version 1 simplification;
- what changes at 10x scale.

When a walkthrough is incomplete, record it here:

| Walkthrough | Missing Or Weak Area | Follow-Up |
| --- | --- | --- |
| None currently recorded | Not applicable | Not applicable |

## Refresh Commands

Run these commands before updating this dashboard:

```bash
python3 skills/ticket-runner/scripts/project_board.py snapshot
scripts/check-taxonomy
scripts/generate-index --check
awk '/^          from pathlib import Path$/{p=1} /^          PY$/{p=0} p{sub(/^          /,""); print}' .github/workflows/docs-checks.yml | python3 -
```

For labs, run the lab-specific tests or demo command listed in that lab's
`how-to-run.md`.

## Common Mistakes

- Treating "no missing link" as proof that content is accurate.
- Counting pages without checking whether they still teach a decision.
- Marking every page without a diagram as incomplete.
- Forgetting that labs need behavior, expected output, observations, and
  trade-offs.
- Updating the dashboard but not the changelog when the update is release
  relevant.

## Checklist

Before treating repository coverage as ready, confirm:

- project items are not blocked or left in To Do unexpectedly;
- section indexes link to new pages;
- component, requirement, and walkthrough pages have appropriate diagrams;
- labs include required docs and tests or demo scripts;
- stale-page signals have been reviewed;
- incomplete walkthroughs are recorded with follow-up work;
- release-relevant changes are reflected in the changelog.

## Related Pages

- [Definition of done](definition-of-done.md)
- [Content review workflow](content-review-workflow.md)
- [Project management](project-management.md)
- [Learning paths](learning-paths.md)
- [Changelog](../../CHANGELOG.md)
- [Roadmap](../../ROADMAP.md)

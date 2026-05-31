# Design Review Checklist

Use this checklist to review an architecture proposal, walkthrough draft, or
system design interview answer. It is written as pass/fail prompts so reviewers
can identify concrete gaps instead of giving vague feedback.

The checklist is not a scoring rubric. It is a way to decide whether a design is
ready for deeper review, revision, or implementation.

## Purpose

A design review should answer:

- Does the design solve the stated problem?
- Are requirements explicit?
- Are components justified by data, scale, and failure constraints?
- Are the trade-offs understandable?
- Can the system be operated and simplified?

Use the prompts below for walkthroughs, design docs, architecture proposals, and
practice reviews.

In a time-boxed interview, start with the highest-risk prompts: requirements,
data ownership, write path correctness, failure behavior, and version 1
simplicity. Mention the remaining areas as follow-up checks if time is short.

## When This Matters

Use this checklist when:

- a design jumps to components before requirements;
- a walkthrough needs reviewer feedback;
- an architecture proposal has unclear failure or operational behavior;
- a learner wants to self-check before comparing against a worked solution;
- a team needs a concise review structure.

## Questions To Ask

Start with the highest-risk gaps:

- What requirement would make this design fail if misunderstood?
- What data is authoritative?
- Which API or workflow is on the critical path?
- What scale assumption justifies the component choices?
- What breaks first during partial failure?
- How would an operator find and repair one user-visible problem?
- What can be removed from version 1?

## Pass/Fail Prompts

Mark each prompt as:

- `Pass`: the design answers the prompt clearly enough to review.
- `Fail`: the design omits the prompt or gives an unverifiable answer.
- `Follow-up`: the design has an assumption that needs confirmation but does
  not block the current review.

### Requirements

- Pass if the problem statement names the user, job, and system boundary.
- Pass if functional requirements are separated from non-functional
  requirements.
- Pass if the most architecture-shaping requirements are ranked.
- Fail if the design uses vague words such as fast, reliable, scalable, secure,
  or real-time without a concrete workflow or target.
- Fail if the design includes future features without naming version 1 scope.

### Data

- Pass if core entities and relationships are named.
- Pass if the authoritative source of truth is clear.
- Pass if derived, cached, indexed, or archived data is labeled as such.
- Pass if retention, deletion, audit, or privacy needs are stated when relevant.
- Fail if the design chooses storage before explaining data shape and access
  patterns.

### APIs And Workflows

- Pass if the main read path and write path are sketched.
- Pass if APIs or commands identify actors, inputs, outputs, and error cases.
- Pass if authorization checks are placed on sensitive actions.
- Pass if repeated requests, retries, or duplicate submissions have a defined
  outcome.
- Fail if only the happy path is described.

### Scaling

- Pass if users, RPS, read/write ratio, storage growth, bandwidth, or peak load
  are estimated where they affect the design.
- Pass if scale estimates are rounded and tied to decisions.
- Pass if bottlenecks are named before scaling mechanisms are added.
- Fail if the design adds caching, sharding, replicas, or queues without a
  requirement or estimate that justifies them.
- Fail if average traffic is estimated but peak load is ignored.

### Failure And Recovery

- Pass if likely failure modes are named for the critical path.
- Pass if retries, timeouts, duplicate messages, and partial failure behavior
  are covered where relevant.
- Pass if user-visible degraded behavior is described.
- Pass if manual repair or reconciliation exists for high-impact failures.
- Fail if the design assumes every dependency is always available.

### Security And Abuse

- Pass if actors, roles, and trust boundaries are named.
- Pass if sensitive data and privileged actions have access controls.
- Pass if abuse paths, quotas, rate limits, or validation are considered when
  public or partner traffic exists.
- Pass if auditability is included for administrative or risky actions.
- Fail if security is reduced to "add auth" without tying controls to actions
  and data.

### Observability And Operations

- Pass if logs, metrics, traces, dashboards, or alerts are tied to critical
  workflows and failure modes.
- Pass if identifiers needed for debugging are named.
- Pass if operators can answer "what happened to this request or user?"
- Pass if deployment, rollback, or backfill risks are noted when relevant.
- Fail if observability is only mentioned as a generic add-on.

### Cost

- Pass if the design names major cost drivers: compute, storage, bandwidth,
  managed services, external APIs, overprovisioning, or operational labor.
- Pass if expensive choices are tied to requirements.
- Pass if version 1 avoids cost that does not buy clear learning or product
  value.
- Fail if the design adds always-on infrastructure without explaining the cost
  trade-off.

### Simplicity

- Pass if version 1 is smaller than the future design.
- Pass if rejected alternatives are named fairly.
- Pass if the design states what signal would make it more complex later.
- Pass if manual steps are accepted only for rare or low-risk cases.
- Fail if the design is a collection of advanced components without a simple
  path to launch or explain.

## Reusable Walkthrough Review

For walkthroughs, copy this compact review block into the end of the draft:

```text
Review status: Pass / Fail / Follow-up

Requirements:
Data:
APIs and workflows:
Scaling:
Failure and recovery:
Security and abuse:
Observability and operations:
Cost:
Simplicity:

Blocking gaps:
Non-blocking improvements:
Revisit signals:
```

Use `Blocking gaps` for missing acceptance criteria or design risks that make
the walkthrough misleading. Use `Non-blocking improvements` for clarity,
examples, or future links that improve learning value without changing the
architecture.

## Decision Guidance

Good review feedback is specific:

```text
Fail: the write path does not explain what happens when two users reserve the
same slot. Add the conflict rule and the user-visible error.
```

Weak review feedback is vague:

```text
Needs more reliability.
```

When marking a prompt as fail, name the file, section, missing decision, and why
it matters.

## Trade-Offs

A checklist improves review consistency, but it can become mechanical. Do not
require every design to be long. Require every design to answer the prompts that
matter for its risk and scope.

A small single-region tool may pass with simple scale and recovery notes. A
public payment workflow needs deeper consistency, security, failure, and
observability answers.

## Common Mistakes

- Marking a design as pass because it has many components.
- Treating all checklist items as equally important for every system.
- Accepting claims such as scalable or reliable without evidence.
- Reviewing only the diagram and ignoring requirements, failure, and operations.
- Asking for future-scale complexity without a revisit signal.
- Giving feedback that cannot be acted on.

## Example

A proposal for a volunteer shift reservation system says:

```text
Use an API service, database, cache, queue, and worker. Volunteers reserve
shifts and receive reminders.
```

Review outcome:

- Requirements: fail. The proposal does not say whether duplicate shift
  confirmations are allowed.
- Data: follow-up. It names reservations but not the authoritative state for
  shift capacity.
- APIs and workflows: fail. The write path does not show conflict behavior.
- Scaling: pass for version 1 if peak writes are below one request per second.
- Failure: follow-up. Reminder retries are implied by the queue but not defined.
- Security: fail if staff cancellation exists but roles are missing.
- Observability: fail. No IDs, logs, metrics, or alert conditions are named.
- Cost: pass if the queue is justified by delayed reminders; otherwise remove it
  from version 1.
- Simplicity: follow-up. The cache may be unnecessary unless read latency or
  load is measured.

This review gives the author concrete changes without prescribing a completely
different architecture.

## Checklist

Before approving a design, confirm:

- Requirements are explicit and ranked.
- Data ownership, entities, relationships, and retention are clear.
- APIs and workflows include read path, write path, authorization, and errors.
- Scaling estimates justify scaling mechanisms.
- Failure modes, degraded behavior, retries, and repair paths are named.
- Security, abuse, and trust boundaries are addressed.
- Observability supports debugging one user-visible issue.
- Cost drivers and expensive choices are explicit.
- Version 1 is simple and has clear revisit signals.
- Review feedback is actionable.

## Related Pages

- [System design process](system-design-process.md)
- [Requirement discovery](requirement-discovery.md)
- [Scale estimation](scale-estimation.md)
- [Trade-off vocabulary](tradeoff-vocabulary.md)
- [Walkthroughs](../walkthroughs/)
- [Definition of Done](../start-here/definition-of-done.md)

# System Design Decision Cookbook

The System Design Decision Cookbook is a public learning resource for engineers
who want to practice moving from requirements to architecture decisions.

It is built around a simple habit: do not start with a memorized architecture.
Start with the problem, identify the requirements that actually matter, choose
components because they answer those requirements, and explain the trade-offs
you are accepting.

This project is not a book summary, course clone, or collection of perfect
interview answers. All explanations, examples, diagrams, labs, and walkthroughs
are intended to be original teaching material.

## Who This Is For

Use this cookbook if you are:

- a backend engineer learning how to reason about larger systems;
- preparing for system design interviews and want practice beyond diagrams;
- moving from feature implementation toward architecture ownership;
- reviewing design proposals and want sharper questions to ask;
- building small labs to observe reliability, scaling, and data behavior.

## What You Will Learn

The cookbook teaches a repeatable decision process:

```text
problem statement
-> functional and non-functional requirements
-> core entities and data shape
-> read and write paths
-> component choices
-> trade-offs and failure modes
-> observability and operations
-> version 1 simplification
```

Each page should help you answer:

- What problem am I solving?
- Which requirements force real design choices?
- Which components are justified, and which are extra?
- What can fail, and what happens when it does?
- How would I observe, operate, and simplify the system?

## Learning Paths

- **Start from zero:** read the system design process, then use the requirement
  pages to practice turning vague prompts into concrete design constraints.
- **Interview practice:** work through walkthroughs, then compare your decisions
  against the review checklist and simplification prompts.
- **Builder path:** use the labs to observe behavior such as rate limiting,
  queue retries, cache misses, replication lag, and hot keys.
- **Reviewer path:** use the templates and rubrics to critique architecture
  proposals for missing requirements, unclear trade-offs, and weak operations
  plans.

## Major Sections

These are the major sections the cookbook will expose as the repository is
built. The links below point to section descriptions in this README until the
corresponding docs and lab directories are created.

- [Start Here](#start-here)
- [Method](#method)
- [Requirements](#requirements)
- [Components](#components)
- [Data](#data)
- [Communication](#communication)
- [Scalability](#scalability)
- [Reliability](#reliability)
- [Security](#security)
- [Operations](#operations)
- [Walkthroughs](#walkthroughs)
- [Labs](#labs)
- [Templates](#templates)

### Start Here

Project guardrails, definition of done, and learning paths.

### Method

The repeatable process for moving from prompt to design.

### Requirements

Decision trees for latency, throughput, availability, consistency, security,
cost, and operability.

### Components

Guidance for choosing APIs, databases, caches, queues, streams, workers, CDNs,
and load balancers.

### Data

Entity discovery, access patterns, consistency, replication, sharding,
indexing, and schema evolution.

### Communication

Synchronous APIs, asynchronous messaging, events, retries, idempotency, and
backpressure.

### Scalability

Capacity planning, bottlenecks, horizontal scaling, partitioning, caching, and
traffic shaping.

### Reliability

Failure modes, timeouts, retries, circuit breakers, failover, recovery, and
data loss scenarios.

### Security

Authentication, authorization, sensitive data, audit logs, abuse resistance,
and privacy.

### Operations

Metrics, logs, traces, alerts, runbooks, SLOs, dashboards, and cost awareness.

### Walkthroughs

Worked designs that show reasoning, alternatives, and trade-offs.

### Labs

Small runnable exercises for observing system behavior.

### Templates

Reusable design docs, decision records, decision trees, and lab scaffolds.

## How To Contribute

This repository is intentionally practical and copyright-safe. Contributions
should use original explanations, original examples, and original Mermaid
diagrams. Do not copy or closely paraphrase books, courses, paid content,
diagrams, tables, screenshots, or exercises.

Before contributing, read:

- [Project source of truth](PROJECT_SOURCE_OF_TRUTH.md)
- [Agent and contributor instructions](AGENTS.md)
- [Ticket backlog](system_design_decision_cookbook_tickets.csv)

Every contribution should make a reader better at explaining why a design fits
the requirements, what trade-offs it makes, and how version 1 could be simpler.

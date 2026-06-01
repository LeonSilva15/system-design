# Scale Estimation

Scale estimation turns vague size words into rough constraints. It helps you
decide whether version 1 can stay simple or whether traffic, storage, bandwidth,
or peak load changes the architecture.

The goal is not precise forecasting. The goal is to find the order of magnitude
that affects a design choice.

## Purpose

Use scale estimation to answer:

- How many users or actors might use the system?
- How many requests per second does the critical path need to handle?
- How quickly does stored data grow?
- How much network bandwidth could the largest flows consume?
- Are reads or writes the dominant load?
- How different is peak load from average load?

Estimate only what can change the design. If a number does not affect storage,
component choice, reliability, or cost, keep it as context.

## When This Matters

Scale estimation matters when:

- a design might need a cache, queue, read replica, partition, or rate limit;
- peak traffic is much larger than average traffic;
- data retention can turn small daily writes into large long-term storage;
- large objects, images, exports, or streams affect bandwidth;
- read and write paths need different treatment;
- you need to explain why version 1 can avoid advanced scaling machinery.

## Questions To Ask

Start with plain questions:

- How many total users exist?
- How many are active per day?
- How many use the busiest hour or minute?
- Which action creates the most reads?
- Which action creates the most writes?
- What is the largest object moved or stored?
- How long is data retained?
- What is the peak-to-average ratio?
- What happens if traffic arrives in a burst?
- What estimate would make the current design wrong?

## Decision Guidance

### Estimate Users Before Requests

User counts are often easier to reason about than raw traffic.

Useful buckets:

- total registered users;
- daily active users;
- hourly active users during the busiest hour;
- concurrent users;
- automated actors such as workers, partner systems, or devices.

Then estimate how often each active actor performs the important actions.

```text
requests per day = active users per day * actions per user per day
average RPS = requests per day / 86,400
peak RPS = average RPS * peak multiplier
```

Use a peak multiplier when traffic is bursty. A classroom signup system, ticket
sale, payroll export, or morning commute app can have a much higher peak than a
steady average.

Name the peak window when you use a multiplier. "Busiest hour is 8x average"
and "busiest minute is 8x average" imply different burst behavior and different
buffering needs.

### Separate Reads From Writes

Read/write ratio shapes the architecture.

- Read-heavy systems may need indexes, caching, search, or read replicas.
- Write-heavy systems may need batching, partitioning, idempotency, or queueing.
- Balanced systems can often start with one database and careful indexes.
- Write correctness can matter more than write volume when conflicts are costly.

Do not say "1,000 RPS" without saying whether it is mostly reads, writes, or
background work.

### Estimate Storage Growth

Storage estimation should include object count, average size, metadata, and
retention.

```text
daily storage = new objects per day * average bytes per object
retained storage = daily storage * retention days
```

For rough design work, round up and keep units simple. It is usually enough to
know whether the answer is megabytes, gigabytes, terabytes, or petabytes.

Storage growth affects:

- database size and indexing;
- backup and restore time;
- partitioning and archival;
- retention policy;
- cost;
- whether large blobs should live outside the primary database.

### Estimate Bandwidth

Bandwidth matters when objects are large or fanout is high.

```text
bandwidth per second = responses per second * average response bytes
```

Consider both ingress and egress:

- uploads into the system;
- downloads to users;
- service-to-service calls;
- replication;
- event fanout;
- exports and reports.

Bandwidth estimates can justify object storage, CDNs, compression, pagination,
streaming, or background exports. They can also prove those choices are not
needed yet.

### Estimate Peak Load

Average traffic hides bursts. Peak load is often what breaks the first design.

Ask:

- Is there a launch, signup window, deadline, batch job, or daily rush?
- Does one actor create fanout to many recipients?
- Can retries multiply traffic during a dependency outage?
- Can abuse or accidental loops create expensive work?

Peak load may call for queues, rate limits, backpressure, buffering, or explicit
product limits. It may also call for a simpler choice: schedule expensive jobs
outside the busiest hour.

### Avoid False Precision

Scale estimates are assumptions, not promises.

Prefer:

```text
Peak approval writes are probably tens per second, not thousands.
```

Instead of:

```text
Peak approval writes will be exactly 43.7 RPS.
```

False precision is harmful because it makes weak assumptions look measured. Use
ranges, round numbers, and revisit triggers.

Good estimate format:

```text
Assumption: busiest-hour write traffic is 5x the daily average.
Design choice: one relational database with a uniqueness constraint is enough
for version 1.
Revisit when: conflict checks or write latency become a measured bottleneck.
```

## Worked Example

A community garden tool shed lets members reserve tools for pickup.

Known assumptions:

- 20,000 registered members.
- 4,000 daily active members during planting season.
- Each active member views tool availability 5 times per day.
- Each active member creates or changes 0.2 reservations per day.
- Average availability response is 8 KB.
- Average reservation record plus audit metadata is 2 KB.
- Reservation and audit data is retained for 2 years.
- Busiest hour is 8x the daily average.

### Users And RPS

Read requests per day:

```text
4,000 active members * 5 availability views = 20,000 read requests/day
average read RPS = 20,000 / 86,400 ~= 0.2-0.3 RPS
busiest-hour read RPS = 0.2-0.3 * 8 ~= a few RPS
```

Write requests per day:

```text
4,000 active members * 0.2 reservation changes = 800 writes/day
average write RPS = 800 / 86,400 ~= about 0.01 RPS
busiest-hour write RPS = 0.01 * 8 ~= still below 1 RPS
```

The exact decimals are not important. The useful conclusion is that version 1 is
small: reads are a few requests per second at peak, and writes are well below
one request per second.

### Read/Write Ratio

```text
read/write ratio = 20,000 reads / 800 writes = 25:1
```

The system is read-heavy, but not large enough to require a cache immediately.
Start with database indexes for availability lookup. Add caching only if
measured read latency or database load justifies it.

### Storage Growth

```text
daily reservation storage = 800 writes * 2 KB = 1,600 KB/day ~= 1.6 MB/day
two-year retention = 1.6 MB * 730 days ~= 1.2 GB
```

This is small enough for one relational database. Backups and audit retention
matter more than partitioning.

### Bandwidth

Peak read bandwidth:

```text
a few read responses/second * 8 KB = tens of KB/second
```

This does not require special delivery infrastructure. If the tool catalog later
adds photos, bandwidth should be estimated again because object size may change
by orders of magnitude.

### Peak Load Consequence

The peak multiplier is 8x, but the absolute peak is still small. The version 1
design can use:

- one relational database;
- indexes on tool, pickup date, and reservation status;
- transactional writes or uniqueness rules to prevent double booking;
- structured logs for reservation conflicts;
- a simple background reminder job.

Revisit the design if peak availability reads reach hundreds of RPS, if tool
photos dominate bandwidth, or if write conflicts create user-visible delays.

## Trade-Offs

Rough estimation improves design focus because it separates "large enough to
care" from "not a version 1 problem." It can also mislead if the inputs are
invented and never revisited.

Use estimates to choose the next simplest architecture. Do not use them to
justify complexity that the product does not need yet.

## Common Mistakes

- Calculating average RPS and ignoring peak load.
- Combining reads, writes, background jobs, and fanout into one traffic number.
- Ignoring object size when estimating bandwidth or storage.
- Forgetting retention, backups, indexes, and audit records in storage thinking.
- Treating one decimal-heavy estimate as more credible than a rounded range.
- Adding a cache because reads outnumber writes without checking absolute load
  and freshness requirements.
- Ignoring retries and abuse as traffic multipliers.

## Checklist

Before using a scale estimate to justify architecture, confirm:

- User count and active-user assumptions are explicit.
- Average RPS and peak RPS are separated.
- Reads and writes are estimated separately.
- Read/write ratio is stated when it affects the design.
- Storage growth includes object size and retention.
- Bandwidth considers response size, uploads, downloads, fanout, or exports.
- Peak load includes burst windows, retries, and abuse where relevant.
- Estimates are rounded to useful order-of-magnitude numbers.
- The design names what changes if the estimate is wrong.
- Version 1 avoids scaling components that the estimate does not justify.

## Related Pages

- [Capacity estimation](../scalability/capacity-estimation.md)
- [System design process](system-design-process.md)
- [Requirement discovery](requirement-discovery.md)
- [Functional vs non-functional requirements](functional-vs-nonfunctional-requirements.md)
- [Definition of Done](../start-here/definition-of-done.md)
- [Style guide](https://github.com/LeonSilva15/system-design/blob/main/STYLE_GUIDE.md)

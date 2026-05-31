# Capacity Estimation Worksheet

Use this worksheet to estimate traffic, storage, bandwidth, read/write ratio,
and peak load before choosing scaling components.

Fill in ranges and rounded numbers. The goal is to find the order of magnitude
that changes the design, not to predict exact production traffic.

Related guide: [Scale estimation](../docs/method/scale-estimation.md)

## 1. Scope And Assumptions

- System or workflow: `[name the workflow being estimated]`
- Version 1 scope: `[what is included]`
- Out of scope: `[what is excluded]`
- Estimation window: `[day, busiest hour, busiest minute, launch window]`
- Revisit signal: `[what number, metric, or incident would change the design]`

## 2. Users And Actors

| Input | Estimate | Notes |
| --- | --- | --- |
| Total users or actors | `[count or range]` | `[known / estimated / needs validation]` |
| Daily active users | `[count or range]` | `[known / estimated / needs validation]` |
| Busiest-hour active users | `[count or range]` | `[known / estimated / needs validation]` |
| Concurrent users | `[count or range]` | `[known / estimated / needs validation]` |
| Automated actors | `[workers, devices, partners]` | `[known / estimated / needs validation]` |

## 3. Traffic Estimate

### Reads

```text
read requests per day =
  daily active users * read actions per active user per day

average read RPS =
  read requests per day / 86,400

peak read RPS =
  average read RPS * peak multiplier
```

Fill in:

- Daily active users: `[number]`
- Read actions per active user per day: `[number]`
- Read requests per day: `[number]`
- Average read RPS: `[rounded number or range]`
- Peak multiplier and window: `[for example, busiest hour is 8x average]`
- Peak read RPS: `[rounded number or range]`

### Writes

```text
write requests per day =
  daily active users * write actions per active user per day

average write RPS =
  write requests per day / 86,400

peak write RPS =
  average write RPS * peak multiplier
```

Fill in:

- Daily active users: `[number]`
- Write actions per active user per day: `[number]`
- Write requests per day: `[number]`
- Average write RPS: `[rounded number or range]`
- Peak multiplier and window: `[for example, signup minute is 20x average]`
- Peak write RPS: `[rounded number or range]`

## 4. Read/Write Ratio

```text
read/write ratio =
  read requests per day / write requests per day
```

Fill in:

- Read requests per day: `[number]`
- Write requests per day: `[number]`
- Read/write ratio: `[for example, 25:1]`
- Design impact: `[read-heavy, write-heavy, balanced, or conflict-sensitive]`

## 5. Storage Growth

```text
daily storage =
  new objects per day * average bytes per object

retained storage =
  daily storage * retention days
```

Fill in:

| Data Type | New Objects Per Day | Average Size | Retention | Retained Storage |
| --- | --- | --- | --- | --- |
| `[entity or object]` | `[count]` | `[KB, MB, GB]` | `[days]` | `[rounded total]` |
| `[entity or object]` | `[count]` | `[KB, MB, GB]` | `[days]` | `[rounded total]` |

Notes:

- Include audit records, indexes, derived data, backups, and large blobs when
  they change the order of magnitude.
- State whether large files belong outside the primary database.

## 6. Bandwidth Estimate

```text
bandwidth per second =
  responses per second * average response bytes
```

Fill in:

| Flow | Peak RPS Or Events/Sec | Average Size | Bandwidth |
| --- | --- | --- | --- |
| Read responses | `[number]` | `[KB, MB]` | `[KB/sec, MB/sec, or Mbps]` |
| Uploads | `[number]` | `[KB, MB]` | `[KB/sec, MB/sec, or Mbps]` |
| Downloads or exports | `[number]` | `[KB, MB]` | `[KB/sec, MB/sec, or Mbps]` |
| Event fanout | `[events/sec * recipients]` | `[KB]` | `[KB/sec, MB/sec, or Mbps]` |

Design impact:

- `[Does this justify pagination, compression, object storage, CDN, streaming,
  or background export?]`

## 7. Peak Load And Burst Behavior

| Burst Source | Peak Window | Multiplier Or Estimate | Design Impact |
| --- | --- | --- | --- |
| `[signup, launch, deadline, batch job, retries, abuse]` | `[minute/hour/day]` | `[number or range]` | `[queue, rate limit, backpressure, or no special handling]` |

Prompts:

- Can retries multiply traffic during an outage?
- Can one actor fan out work to many recipients?
- Can abuse create expensive reads, writes, or external API calls?
- Can expensive work be scheduled outside the peak window?

## 8. Design Consequences

Use the estimates to decide what version 1 needs.

| Estimate | Conclusion | Version 1 Choice | Revisit When |
| --- | --- | --- | --- |
| `[traffic, storage, bandwidth, or peak finding]` | `[small, medium, large, risky]` | `[component or simpler choice]` | `[metric or event]` |

## Worked Example

A neighborhood seed library lets members reserve seed packets for pickup.

Assumptions:

- 10,000 registered members.
- 2,000 daily active members during spring planting season.
- Each active member checks seed availability 4 times per day.
- Each active member creates or changes 0.1 reservations per day.
- Average availability response is 6 KB.
- Average reservation plus audit data is 2 KB.
- Reservation data is retained for 2 years.
- Busiest hour is 10x the daily average.

Reads:

```text
read requests per day = 2,000 * 4 = 8,000
average read RPS = 8,000 / 86,400 ~= 0.1 RPS
peak read RPS = 0.1 * 10 ~= about 1 RPS
```

Writes:

```text
write requests per day = 2,000 * 0.1 = 200
average write RPS = 200 / 86,400 ~= far below 1 RPS
peak write RPS = still below 1 RPS
```

Read/write ratio:

```text
8,000 reads / 200 writes = 40:1
```

Storage:

```text
daily storage = 200 reservation writes * 2 KB = 400 KB/day
two-year retained storage = 400 KB * 730 ~= 292 MB
```

Bandwidth:

```text
peak read bandwidth = about 1 response/sec * 6 KB = about 6 KB/sec
```

Design consequence:

```text
The system is read-heavy but small. Version 1 can use one relational database
with indexes for seed availability lookup and transactional reservation writes.
A cache, sharding, or separate search service is not justified yet. Revisit if
peak reads reach hundreds of RPS, if write conflicts create visible delays, or
if catalog images change bandwidth by orders of magnitude.
```

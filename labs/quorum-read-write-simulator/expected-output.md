# Expected Output

The default command:

```bash
python -m quorum_read_write_simulator.demo
```

prints output similar to:

```text
config replicas=3 read_quorum=2 write_quorum=2 latencies=12,35,80
01 write quorum: op=write quorum=2 responded=2 available=3 latency_ms=35 value=reservation-open version=1 stale=no responses=[r1:v1@12ms,r2:v1@35ms] note=write committed after fastest quorum acknowledgements
02 read quorum: op=read quorum=2 responded=2 available=3 latency_ms=35 value=reservation-open version=1 stale=no responses=[r1:v1@12ms,r2:v1@35ms] note=read quorum returned latest observed version
03 make r1 unavailable and leave r3 stale
04 degraded read quorum: op=read quorum=2 responded=2 available=2 latency_ms=80 value=reservation-open version=1 stale=no responses=[r2:v1@35ms,r3:v0@80ms] note=read quorum returned latest observed version
05 low quorum stale read: op=read quorum=1 responded=1 available=1 latency_ms=80 value=empty version=0 stale=yes responses=[r3:v0@80ms] note=read quorum missed newer version on another replica
06 repair read quorum: op=read quorum=2 responded=2 available=2 latency_ms=80 value=reservation-open version=1 stale=no responses=[r1:v1@12ms,r3:v0@80ms] note=read quorum returned latest observed version
07 read repair touched=r3
   note read repair only updates replicas that answered that read
08 fastest read quorum=1: op=read quorum=1 responded=1 available=3 latency_ms=12 value=reservation-open version=1 stale=no responses=[r1:v1@12ms] note=read quorum returned latest observed version
09 full read quorum: op=read quorum=3 responded=3 available=3 latency_ms=80 value=reservation-open version=1 stale=no responses=[r1:v1@12ms,r2:v1@35ms,r3:v1@80ms] note=read quorum returned latest observed version
10 final replica state
   r1:value=reservation-open version=1 available=True latency_ms=12
   r2:value=reservation-open version=1 available=True latency_ms=35
   r3:value=reservation-open version=1 available=True latency_ms=80
```

The important fields are `quorum`, `responded`, `available`, `latency_ms`,
`version`, `stale`, and the per-replica response list. The `stale` field refers
to the returned value. A read can include a stale responder while still
returning the newest version it observed.

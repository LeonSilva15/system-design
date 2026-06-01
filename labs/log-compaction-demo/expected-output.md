# Expected Output

The default command:

```bash
PYTHONPATH=src python -m log_compaction_demo.demo
```

prints deterministic output similar to:

```text
config batch_size=3 retention_records=5
01 append-only log: records=7 offsets=0,1,2,3,4,5,6 high_watermark=7
   history: 0:item:tent=available=3,1:item:lamp=available=5,2:item:tent=available=2,3:item:stove=available=1,4:item:lamp=available=4,5:item:tent=available=3,6:item:stove=<deleted>
02 consumer poll: name=search-projection read_offsets=0,1,2 start_offset=0 next_offset=3 lag=4 projection=item:lamp=available=5,item:tent=available=2
03 append-only key history: key=item:tent versions=0:item:tent=available=3,2:item:tent=available=2,5:item:tent=available=3
04 latest-value compaction: before=7 after=3 removed=4 kept_offsets=4,5,6 latest=item:lamp=available=4,item:tent=available=3 tombstones=item:stove
05 retention: retain_last=5 removed_offsets=0,1 earliest_offset=2 retained_offsets=2,3,4,5,6
06 consumer catch-up: name=search-projection read_offsets=3,4,5 next_offset=6 lag=1 projection=item:lamp=available=4,item:stove=available=1,item:tent=available=3
07 retention gap: consumer=analytics-backfill requested_offset=0 earliest_offset=2 action=rebuild_or_snapshot message=requested offset 0 is before earliest retained offset 2
08 final consumer poll: name=search-projection read_offsets=6 next_offset=7 lag=0 projection=item:lamp=available=4,item:tent=available=3
```

## How To Read It

- Line `01` shows that every update receives an offset in the append-only log.
- Line `02` shows a consumer reading a batch and advancing `next_offset`.
- Line `03` shows that one key can have several historical versions.
- Line `04` shows latest-value compaction: seven records reduce to three latest
  records, including a tombstone for a deleted key.
- Line `05` shows retention removing old offsets from the hot log.
- Line `06` still shows `item:stove=available=1` because the consumer has not
  read the tombstone at offset `6` yet; line `08` shows the delete applied.
- Line `07` shows a slow or new consumer that can no longer start at offset `0`
  after retention. It needs a snapshot, source rebuild, or archived history.

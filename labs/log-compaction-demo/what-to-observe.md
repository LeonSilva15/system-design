# What To Observe

## Append-Only History

Line `01` shows offsets `0` through `6`. The log records every update, even when
the same key changes several times.

Question to ask: Which consumers need every transition, and which only need the
latest value?

## Consumer Offsets

Line `02` shows the search projection reading offsets `0,1,2` and advancing its
`next_offset` to `3`. Lag is the distance from the consumer's next offset to the
log high watermark.

Question to ask: What user-visible freshness promise does this lag represent?

## Latest-Value Compaction

Line `04` shows compaction keeping the newest record for each key. Older values
for `item:tent` are not needed to rebuild a current inventory projection, but
they may still matter for audit, analytics, or debugging.

Question to ask: Is the consumer rebuilding current state, or does it need the
full sequence of changes?

## Tombstones

The compacted output includes `item:stove` as a tombstone. The final projection
does not include `item:stove` because the delete marker is applied by the
consumer.

Question to ask: How long must delete markers remain so offline consumers do
not resurrect deleted keys?

## Retention

Line `05` removes offsets `0` and `1` from hot retention. The search projection
can still continue because its next offset is `3`, but a new analytics backfill
starting at `0` fails in line `07`.

Question to ask: Does the retention window match the longest expected outage,
backfill, or onboarding replay?

## Batch Size

Lower `--batch-size` to slow the consumer. Smaller batches make offset progress
more visible and can leave more lag after each poll.

Question to ask: Is the consumer slow because of batch size, downstream writes,
hot keys, schema failures, or replay rate limits?

## Retention Window

Lower `--retention-records` to make the retention gap more severe. Raise it to
keep more hot history.

Question to ask: Should older records be kept hot, compacted, archived, or
rebuildable from the source of truth?

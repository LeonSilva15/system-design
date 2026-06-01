# What To Observe

Use the lab to answer these questions:

- What changes when `[parameter]` increases?
- What changes when `[failure mode]` happens?
- Which output shows the system is saturated, stale, retrying, dropping work, or
  recovering?
- Which behavior would be acceptable in version 1?
- Which behavior would force a different architecture?

## Suggested Experiments

| Experiment | Change | Expected Observation |
| --- | --- | --- |
| Baseline | Run the default demo | `[Expected normal behavior]` |
| Stress | Increase `[load or skew]` | `[Expected saturation or failure signal]` |
| Recovery | Enable `[retry, refill, repair, or cleanup]` | `[Expected recovery signal]` |

## Connect Back To Design

After running the lab, update your design notes:

- Which requirement did the lab make concrete?
- Which trade-off became visible?
- Which metric, log, test, or output would you need in a real system?

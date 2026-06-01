# What To Observe

Use the lab to answer these questions:

- How many requests are allowed immediately when the bucket starts full?
- What changes when burst capacity increases?
- What changes when refill rate increases?
- How does request spacing affect the number of allowed requests?
- What retry hint does the limiter return when the bucket is empty?
- Which settings would protect a write path without blocking normal users?

## Suggested Experiments

| Experiment | Change | Expected Observation |
| --- | --- | --- |
| Baseline | Run the default demo | A short burst is allowed, then later requests are limited |
| Smaller burst | `--capacity 2` | Fewer initial requests are allowed |
| Faster refill | `--refill-rate 5` | More requests become allowed during the same sequence |
| Tighter spacing | `--spacing 0.05` | Less time passes between requests, so fewer tokens refill |
| Empty start | `--start-empty` | Early requests are limited until enough time has passed |
| Expensive request | `--cost 2` | Each allowed request consumes more burst capacity |

## Connect Back To Design

After running the lab, update your design notes:

- What limit key would this bucket represent: user, tenant, API key, IP, or
  resource?
- Which action should spend one token, and which action should spend more?
- What retry hint would clients see?
- What metric would show allowed, limited, and retry behavior?
- What changes if several API instances need to share the same bucket?

# Expected Output

The default demo:

```bash
python -m rate_limiter_lab.demo
```

prints output similar to:

```text
config capacity=5.00 refill_rate=1.00 tokens/sec cost=1.00 spacing=0.20 requests=10
request=01 at=0.00s decision=allowed tokens_before=5.00 tokens_after=4.00 retry_after=0.00s
request=02 at=0.20s decision=allowed tokens_before=4.20 tokens_after=3.20 retry_after=0.00s
request=03 at=0.40s decision=allowed tokens_before=3.40 tokens_after=2.40 retry_after=0.00s
request=04 at=0.60s decision=allowed tokens_before=2.60 tokens_after=1.60 retry_after=0.00s
request=05 at=0.80s decision=allowed tokens_before=1.80 tokens_after=0.80 retry_after=0.00s
request=06 at=1.00s decision=allowed tokens_before=1.00 tokens_after=0.00 retry_after=0.00s
request=07 at=1.20s decision=limited tokens_before=0.20 tokens_after=0.20 retry_after=0.80s
request=08 at=1.40s decision=limited tokens_before=0.40 tokens_after=0.40 retry_after=0.60s
request=09 at=1.60s decision=limited tokens_before=0.60 tokens_after=0.60 retry_after=0.40s
request=10 at=1.80s decision=limited tokens_before=0.80 tokens_after=0.80 retry_after=0.20s
summary allowed=6 limited=4 final_tokens=0.80
```

What this proves:

- the first requests are allowed because the bucket starts full;
- tokens refill between requests;
- once the bucket cannot pay the request cost, decisions become `limited`;
- `retry_after` shrinks as the next token refills.

Small floating-point formatting differences are acceptable if the behavior is
the same.

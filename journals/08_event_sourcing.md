# Event Sourcing Audit Trail

Date: 2026-06-03
Mood/Energy: Careful and methodical
Estimated reading time: 7 minutes

## The "Why"
I wanted to understand why financial systems are so obsessed with append-only history. The answer kept showing up in different forms: if you preserve the events, you preserve the truth.

## The Exploration
Event sourcing felt strange at first because I was used to storing the latest state directly. With event sourcing, the current state is not the source of truth. The event log is. That means a deposit, withdrawal, or transfer is stored as a record, and the account balance is rebuilt by replaying those records.

My sketch for it was:

```text
event stream: deposit -> withdraw -> deposit -> ...
replay events -> current balance
```

That made the audit trail feel much stronger. If someone asks, "how did we get here?" I do not need to guess. I can replay the path.

## The Code (Crucial)
The longer Python example lives in [code/08_event_sourcing-example.py](../code/08_event_sourcing-example.py).

```python
events = [
    {"type": "deposit", "amount": 100},
    {"type": "withdraw", "amount": 30},
]

balance = 0
for event in events:
    if event["type"] == "deposit":
        balance += event["amount"]
    elif event["type"] == "withdraw":
        balance -= event["amount"]
```

## The "Aha!" Moment
The big click was that the history itself is the product. A snapshot is just a convenience for faster reads. The events are what make the system explainable.

## The Struggle
I kept wanting to mutate account objects directly because that is what feels natural in application code. That instinct made the design look simpler, but it also erased the audit trail. Once I forced myself to think in terms of immutable events, the model got stricter, but it also got much easier to reason about.

## Key Takeaways
- The event log is the source of truth.
- Current state is derived by replaying history.
- Snapshots are optimization, not truth.
- Event sourcing gives you a strong audit trail.
- Idempotency matters because duplicate events are always a possibility.

## Questions I still have
- How often should a system snapshot if replay starts getting expensive?
- What is the cleanest way to evolve event schemas without breaking old data?

# Consistent Hashing Sharding Simulator

Date: 2026-07-23
Mood/Energy: Clear-headed and satisfied
Estimated reading time: 7 minutes

## The "Why"
I wanted to see why distributed systems keep talking about consistent hashing instead of the simpler modulo approach. The promise sounded useful: if a node changes, only some keys should move.

## The Exploration
The easiest way to think about it is as a ring. Each node gets one or more points on the ring, and each key gets mapped to the next node clockwise. That means keys are not tied to a specific numeric partition count. They are tied to the shape of the ring.

My sketch looked like this:

```text
0 ---- node A ---- node B ---- node C ---- 0
key hashes land somewhere on the circle
```

Virtual nodes were the part that made the system feel practical instead of academic. Without them, a few real nodes can end up with uneven load. With them, the distribution looks much smoother.

## The Code (Crucial)
The longer Python example lives in [code/15_consistent_hashing-example.py](../code/15_consistent_hashing-example.py).

```python
ring.add_node("db-a")
ring.add_node("db-b")
print(ring.get_node("user:17"))
```

## The "Aha!" Moment
The big click was that consistency is about minimizing movement, not eliminating movement. The ring does not freeze the world. It just reduces the blast radius when membership changes.

## The Struggle
I kept comparing it to modulo hashing and expecting the same behavior with fewer partitions. That was the wrong mental model. Modulo works fine until the node count changes, and then almost everything shifts. Consistent hashing exists specifically to avoid that kind of mass reshuffle.

## Key Takeaways
- Keys map to a ring, not directly to a fixed node count.
- Virtual nodes help with balance.
- Consistent hashing reduces key movement during topology changes.
- It is about minimizing disruption, not making movement disappear.
- This is why it shows up everywhere in distributed storage.

## Questions I still have
- How do systems tune the number of virtual nodes in practice?
- What is the best way to visualize rebalancing pressure in a live cluster?

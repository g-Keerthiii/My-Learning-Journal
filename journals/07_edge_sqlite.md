# Edge Caching with SQLite and LiteFS

Date: 2026-05-27
Mood/Energy: Optimistic and practical
Estimated reading time: 7 minutes

## The "Why"
I kept hearing that edge infrastructure does not always need a giant database cluster. That sounded suspiciously elegant, so I wanted to see how far I could get with a small SQLite-backed cache and a replication layer that handled the boring distributed parts for me.

## The Exploration
What I like about SQLite here is that it is boring in a good way. The query model is familiar, the file format is stable, and the data is local. The interesting part is not the SQL itself. It is the replication and leadership behavior around it.

My mental model became:

```text
app -> local sqlite file -> replicated to other nodes
                |
                +-> writes only on leader
                +-> reads on every edge node
```

That separation made the architecture feel much more approachable. I do not need every region to be a full database primary. I need reads to be local and writes to be controlled.

## The Code (Crucial)
The longer example is in [code/07_edge_sqlite-example.py](../code/07_edge_sqlite-example.py).

```python
import sqlite3


def get_value(db_path, key):
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute("select value from cache where key = ?", (key,)).fetchone()
        return row[0] if row else None
    finally:
        conn.close()
```

## The "Aha!" Moment
The biggest realization was that edge caching is not only about speed. It is about placing state closer to users without giving up a sane write path. SQLite makes that feel surprisingly lightweight.

## The Struggle
I got tangled up in the difference between a local cache and a replicated database. My first mental model assumed every node could just write whenever it wanted, which obviously breaks down. Once I accepted that one node has to own writes and the others mostly serve reads, the design became much more coherent.

## Key Takeaways
- SQLite is attractive at the edge because it is compact and predictable.
- Reads can be local even when writes are centralized.
- Replication is the real distributed-systems problem here.
- Simplicity at the storage layer can still support a serious deployment model.
- Edge infrastructure is about latency as much as it is about fault tolerance.

## Questions I still have
- How do systems handle failover cleanly when the leader disappears?
- What is the operational cost of replication lag in real edge deployments?

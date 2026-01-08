# Building a Minimal LSM-Tree Key-Value Store

Date: 2026-03-17
Mood/Energy: Focused and slightly overconfident
Estimated reading time: 7 minutes

## The "Why"
I wanted to stop treating databases like mysterious black boxes. I kept hearing about LSM trees, SSTables, and write amplification, and I finally decided to build a tiny version so I could see how the pieces fit together.

## The Exploration
My simplified version of an LSM tree felt like a notebook that gets copied into cleaner notebooks over time. New writes land in memory first, because memory is fast. When the memtable gets big enough, I flush it to disk as an immutable sorted file. Later, reads check the newest data first and fall back to older files if needed.

My mental sketch was basically this:

```text
writes -> memtable -> flush -> sstable_001
                           -> sstable_002
                           -> sstable_003
```

That ordering matters. I had to remind myself that newer data wins, even if the older SSTable still exists on disk. The system is really saying, "keep the history, but read the latest version first."

Once I thought about it that way, the weird terms became easier:

- memtable = the fast, mutable layer
- SSTable = a frozen, sorted snapshot
- compaction = cleaning up older snapshots so reads do less work

## The Code (Crucial)
The longer example lives in [code/02_lsm_tree_kv-example.py](../code/02_lsm_tree_kv-example.py).

```python
class MiniLSM:
    def __init__(self, flush_limit=3):
        self.memtable = {}
        self.sstables = []
        self.flush_limit = flush_limit

    def put(self, key, value):
        self.memtable[key] = value
        if len(self.memtable) >= self.flush_limit:
            self.flush()

    def flush(self):
        self.sstables.insert(0, dict(sorted(self.memtable.items())))
        self.memtable.clear()

    def get(self, key):
        if key in self.memtable:
            return self.memtable[key]
        for table in self.sstables:
            if key in table:
                return table[key]
        return None
```

## The "Aha!" Moment
The thing that finally clicked was that LSM trees trade expensive writes for cheaper reads and batched disk work. The database is not avoiding work. It is just choosing *when* to do it.

## The Struggle
I first made the mistake of thinking I could just append everything to one file and call it a day. That version was easy to write, but it missed the whole point of sorted, immutable storage. The bug that forced me to rethink it was embarrassingly simple: older values kept winning because my lookup order was wrong. Once I searched the newest in-memory state first and then walked the SSTables in reverse age, the behavior finally matched the model.

## Key Takeaways
- Writes go to memory first so they stay cheap.
- SSTables are immutable and sorted, which makes them easy to scan.
- Lookup order matters as much as storage format.
- Compaction is the cleanup step that keeps the system healthy.
- LSM trees are a deliberate tradeoff, not a free performance trick.

## Questions I still have
- How do production systems choose compaction strategy without hurting latency?
- Where is the exact tipping point where an LSM design beats a B-tree for a workload?

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
        frozen = dict(sorted(self.memtable.items()))
        self.sstables.insert(0, frozen)
        self.memtable.clear()

    def get(self, key):
        if key in self.memtable:
            return self.memtable[key]
        for table in self.sstables:
            if key in table:
                return table[key]
        return None

    def compact(self):
        merged = {}
        for table in reversed(self.sstables):
            merged.update(table)
        self.sstables = [dict(sorted(merged.items()))]


if __name__ == "__main__":
    db = MiniLSM(flush_limit=2)
    db.put("alice", "v1")
    db.put("bob", "v1")
    db.put("alice", "v2")
    db.flush()
    print(db.get("alice"))
    print(db.sstables)

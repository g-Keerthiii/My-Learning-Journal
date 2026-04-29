import bisect
import hashlib


class ConsistentHashRing:
    def __init__(self, replicas=3):
        self.replicas = replicas
        self.ring = []
        self.nodes = {}

    def _hash(self, value):
        digest = hashlib.sha1(value.encode()).hexdigest()
        return int(digest, 16)

    def add_node(self, node):
        for replica in range(self.replicas):
            key = self._hash(f"{node}:{replica}")
            bisect.insort(self.ring, key)
            self.nodes[key] = node

    def get_node(self, item):
        if not self.ring:
            return None
        key = self._hash(item)
        index = bisect.bisect(self.ring, key) % len(self.ring)
        return self.nodes[self.ring[index]]


if __name__ == "__main__":
    ring = ConsistentHashRing(replicas=5)
    ring.add_node("db-a")
    ring.add_node("db-b")
    ring.add_node("db-c")
    for key in ["user:17", "user:42", "invoice:9"]:
        print(key, "->", ring.get_node(key))

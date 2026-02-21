import sqlite3


class EdgeCache:
    def __init__(self, db_path, leader=False):
        self.db_path = db_path
        self.leader = leader

    def get(self, key):
        conn = sqlite3.connect(self.db_path)
        try:
            row = conn.execute("select value from cache where key = ?", (key,)).fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    def set(self, key, value):
        if not self.leader:
            raise PermissionError("writes are only allowed on the leader")
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("create table if not exists cache (key text primary key, value text)")
            conn.execute("insert into cache(key, value) values(?, ?) on conflict(key) do update set value = excluded.value", (key, value))
            conn.commit()
        finally:
            conn.close()


if __name__ == "__main__":
    cache = EdgeCache("edge.db", leader=True)
    cache.set("home_page", "fresh html")
    print(cache.get("home_page"))

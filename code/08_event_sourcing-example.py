events = [
    {"type": "deposit", "amount": 100, "id": "evt-1"},
    {"type": "withdraw", "amount": 30, "id": "evt-2"},
    {"type": "deposit", "amount": 25, "id": "evt-3"},
]

seen_ids = set()
balance = 0
projection = []

for event in events:
    if event["id"] in seen_ids:
        continue
    seen_ids.add(event["id"])
    if event["type"] == "deposit":
        balance += event["amount"]
    elif event["type"] == "withdraw":
        balance -= event["amount"]
    projection.append((event["id"], balance))

print("balance:", balance)
print("projection:", projection)

# Redis Clone via the RESP Protocol

Date: 2026-07-08
Mood/Energy: Playful and stubborn
Estimated reading time: 7 minutes

## The "Why"
I wanted to understand why Redis feels so fast even though, at the core, it is still just handling network requests and in-memory data. Building a tiny clone sounded like the best way to stop treating the protocol as magic.

## The Exploration
RESP is much more mechanical than I expected. Once I saw the framing, it felt like a very strict little language for talking over TCP. The server does not care that a command came from `redis-cli` or from my own program. It just reads bytes, parses the structure, and returns a structured response.

My mental picture was:

```text
redis-cli -> TCP socket -> RESP parser -> in-memory store -> RESP reply
```

That was the real lesson for me: a lot of the elegance comes from the protocol being simple enough that the server can stay focused on the data structure and command handling.

## The Code (Crucial)
The longer JavaScript example lives in [code/13_redis_clone-example.js](../code/13_redis_clone-example.js).

```javascript
const command = parseRESP(input)
if (command[0] === 'ECHO') {
  return encodeSimpleString(command[1])
}
```

## The "Aha!" Moment
The click happened when I realized the protocol is just a small grammar. Once the parser works, every command becomes a normal application function instead of a network mystery.

## The Struggle
I kept messing up bulk string lengths because I was thinking about characters instead of bytes. That bug was annoying but useful. It forced me to remember that TCP and RESP care about raw byte counts, not the visual length of a string on screen.

## Key Takeaways
- RESP is compact and easy to parse once the framing clicks.
- Redis feels fast because the execution path is intentionally simple.
- Byte counts matter more than visual string length.
- A tiny protocol parser unlocks a lot of server behavior.
- In-memory data structures make the command path straightforward.

## Questions I still have
- How does Redis keep its event loop responsive under heavy mixed workloads?
- What is the best next command to implement after `ECHO` and `SET`?

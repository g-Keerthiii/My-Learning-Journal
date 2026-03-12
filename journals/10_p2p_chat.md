# Decentralized P2P Chat using libp2p

Date: 2026-06-17
Mood/Energy: Excited and slightly lost
Estimated reading time: 7 minutes

## The "Why"
I wanted to feel what it is like to build a networked app without hiding behind a server I fully control. A peer-to-peer chat app seemed like a nice way to see how discovery, routing, and transport all fit together.

## The Exploration
The part that surprised me most was how many separate problems a P2P stack has to solve before a message can even be sent. Peers need identities, they need a way to discover each other, they need a transport, and they need a secure session once the connection is formed.

My sketch looked like this:

```text
peer A <-> DHT discovery <-> peer B
   |                             |
   +-- noise encryption ---------+
   +-- multiplexed streams -------+
```

I used to imagine P2P as just "socket to socket," but it is really a whole coordination layer on top of raw connections.

## The Code (Crucial)
The longer JavaScript example lives in [code/10_p2p_chat-example.js](../code/10_p2p_chat-example.js).

```javascript
const node = await createLibp2p({
  transports: [tcp()],
  connectionEncryption: [noise()],
  streamMuxers: [yamux()],
  peerDiscovery: [kadDHT()],
})

await node.start()
await node.dial(peerId)
```

## The "Aha!" Moment
The real click was that peer identity is built into the system. A peer ID is not just a label. It is tied to a public key, which makes the network feel much more self-authenticating than a normal client-server app.

## The Struggle
I kept mixing up routing and transport. Discovery is about finding peers, transport is about moving bytes, and encryption is about making the bytes private. I was trying to treat them like one feature, which made the design seem messier than it really is. Once I separated those layers, the stack made more sense.

## Key Takeaways
- P2P apps still need discovery, transport, and security.
- libp2p bundles a lot of that coordination for me.
- Peer IDs are part of the trust model.
- NAT traversal is not a side problem; it is central.
- Decentralized chat is more about networking architecture than UI.

## Questions I still have
- How do peer networks stay healthy when most peers are behind NAT?
- What is the best way to persist chat history without reintroducing central control?

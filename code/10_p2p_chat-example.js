async function createLibp2p(config) {
  return {
    async start() {
      console.log("node started with", config.transports.length, "transport(s)")
    },
    async dial(peerId) {
      console.log("dialing peer", peerId)
    },
    async stop() {
      console.log("node stopped")
    },
  }
}

function tcp() {
  return { name: "tcp" }
}

function noise() {
  return { name: "noise" }
}

function yamux() {
  return { name: "yamux" }
}

function kadDHT() {
  return { name: "kad-dht" }
}

async function main() {
  const node = await createLibp2p({
    transports: [tcp()],
    connectionEncryption: [noise()],
    streamMuxers: [yamux()],
    peerDiscovery: [kadDHT()],
  })

  await node.start()
  await node.dial("12D3KooWPeerIdHere")
}

main()

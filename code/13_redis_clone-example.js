const net = require('net')

const store = new Map()

function encodeSimpleString(value) {
  return `+${value}\r\n`
}

function encodeBulkString(value) {
  return `$${Buffer.byteLength(value)}\r\n${value}\r\n`
}

function parseRESP(buffer) {
  const text = buffer.toString('utf8').trim()
  const parts = text.split('\r\n')
  const command = []
  for (let index = 2; index < parts.length; index += 2) {
    command.push(parts[index])
  }
  return command
}

const server = net.createServer((socket) => {
  socket.on('data', (buffer) => {
    const command = parseRESP(buffer)
    const name = (command[0] || '').toUpperCase()

    if (name === 'ECHO') {
      socket.write(encodeBulkString(command[1] || ''))
      return
    }

    if (name === 'SET') {
      store.set(command[1], command[2])
      socket.write(encodeSimpleString('OK'))
      return
    }

    if (name === 'GET') {
      const value = store.get(command[1])
      socket.write(value === undefined ? '$-1\r\n' : encodeBulkString(value))
      return
    }

    socket.write('-ERR unknown command\r\n')
  })
})

server.listen(6379, () => console.log('mini redis clone listening on 6379'))

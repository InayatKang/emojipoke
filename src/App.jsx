import React, { useState, useEffect } from 'react'
import Room from './Room.jsx'
import Home from './Home.jsx'

function randomRoomId() {
  return Math.random().toString(36).slice(2, 8).toUpperCase()
}

export default function App() {
  const [roomId, setRoomId] = useState(null)

  useEffect(() => {
    const match = window.location.pathname.match(/^\/room\/([A-Z0-9]{4,10})$/i)
    if (match) setRoomId(match[1].toUpperCase())
  }, [])

  function createRoom() {
    const id = randomRoomId()
    window.history.pushState({}, '', `/room/${id}`)
    setRoomId(id)
  }

  function joinRoom(id) {
    const clean = id.trim().toUpperCase()
    window.history.pushState({}, '', `/room/${clean}`)
    setRoomId(clean)
  }

  if (roomId) return <Room roomId={roomId} />
  return <Home onCreate={createRoom} onJoin={joinRoom} />
}

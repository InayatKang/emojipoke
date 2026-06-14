import React, { useState, useEffect, useRef } from 'react'
import Pusher from 'pusher-js'

const EMOJIS = [
  { emoji: '🏠', label: 'home', id: 'house' },
  { emoji: '🚗', label: 'car', id: 'car' },
  { emoji: '🥡', label: 'lunch', id: 'lunch' },
]

const PUSHER_KEY = import.meta.env.VITE_PUSHER_KEY
const PUSHER_CLUSTER = import.meta.env.VITE_PUSHER_CLUSTER || 'us3'

export default function Room({ roomId }) {
  const [received, setReceived] = useState(null)
  const [sending, setSending] = useState(null)
  const [connected, setConnected] = useState(false)
  const [copied, setCopied] = useState(false)
  const [notifPerm, setNotifPerm] = useState(
    typeof Notification !== 'undefined' ? Notification.permission : 'denied'
  )
  const [receivedKey, setReceivedKey] = useState(0)
  const sendingTimer = useRef(null)

  useEffect(() => {
    if (!PUSHER_KEY) return

    const pusher = new Pusher(PUSHER_KEY, { cluster: PUSHER_CLUSTER })
    const channel = pusher.subscribe(`room-${roomId}`)

    channel.bind('pusher:subscription_succeeded', () => setConnected(true))
    channel.bind('emoji-sent', (data) => {
      setReceived(data)
      setReceivedKey(k => k + 1)
      if (document.visibilityState !== 'visible' && notifPerm === 'granted') {
        navigator.serviceWorker?.ready.then(reg => {
          reg.showNotification('Poke!', {
            body: `${data.emoji} — ${data.label}`,
            vibrate: [80, 40, 80],
          })
        })
      }
    })

    pusher.connection.bind('connected', () => setConnected(true))
    pusher.connection.bind('disconnected', () => setConnected(false))

    return () => {
      channel.unbind_all()
      pusher.unsubscribe(`room-${roomId}`)
      pusher.disconnect()
    }
  }, [roomId])

  async function sendEmoji(item) {
    if (sending) return
    setSending(item.id)
    try {
      await fetch('/api/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ roomId, ...item }),
      })
    } catch (e) {}
    if (sendingTimer.current) clearTimeout(sendingTimer.current)
    sendingTimer.current = setTimeout(() => setSending(null), 600)
  }

  function shareRoom() {
    const url = `${window.location.origin}/room/${roomId}`
    if (navigator.share) {
      navigator.share({ title: 'Join my Poke room', url })
    } else {
      navigator.clipboard.writeText(url).then(() => {
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      })
    }
  }

  async function requestNotifs() {
    const perm = await Notification.requestPermission()
    setNotifPerm(perm)
  }

  return (
    <div style={styles.container}>
      {/* Received emoji display */}
      <div style={styles.receivedArea}>
        {received ? (
          <div key={receivedKey} style={styles.receivedEmoji}>
            {received.emoji}
          </div>
        ) : (
          <div style={styles.placeholder}>
            <div style={styles.placeholderBox} />
            <span style={styles.placeholderText}>
              {connected ? 'Waiting for a poke…' : 'Connecting…'}
            </span>
          </div>
        )}
      </div>

      {/* Room strip */}
      <div style={styles.strip}>
        <div style={styles.roomInfo}>
          <div style={{ ...styles.dot, background: connected ? 'var(--accent)' : 'var(--text-dim)', boxShadow: connected ? '0 0 6px var(--accent)' : 'none' }} />
          <span style={styles.roomCode}>{roomId}</span>
        </div>
        <button style={styles.shareBtn} onClick={shareRoom}>
          {copied ? '✓ Copied' : 'Invite'}
        </button>
        {notifPerm === 'default' && (
          <button style={styles.notifBtn} onClick={requestNotifs}>🔔</button>
        )}
      </div>

      {/* Emoji buttons */}
      <div style={styles.emojiBar}>
        {EMOJIS.map(item => (
          <button
            key={item.id}
            style={{
              ...styles.emojiBtn,
              ...(sending === item.id ? styles.emojiBtnActive : {}),
            }}
            onClick={() => sendEmoji(item)}
            aria-label={`Send ${item.label}`}
          >
            <span style={styles.emojiGlyph}>{item.emoji}</span>
            <span style={styles.emojiLabel}>{item.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

const styles = {
  container: {
    height: '100dvh',
    display: 'flex',
    flexDirection: 'column',
    paddingTop: 'env(safe-area-inset-top, 16px)',
    paddingBottom: 'env(safe-area-inset-bottom, 16px)',
  },
  receivedArea: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  receivedEmoji: {
    fontSize: '120px',
    lineHeight: 1,
    animation: 'none',
    filter: 'drop-shadow(0 0 40px rgba(200,240,122,0.3))',
  },
  placeholder: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '16px',
  },
  placeholderBox: {
    width: '120px',
    height: '120px',
    borderRadius: '28px',
    border: '2px dashed var(--border)',
  },
  placeholderText: {
    fontSize: '14px',
    color: 'var(--text-dim)',
  },
  strip: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '10px 20px',
    borderTop: '1px solid var(--border)',
    borderBottom: '1px solid var(--border)',
    background: 'var(--surface)',
  },
  roomInfo: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  dot: {
    width: '7px',
    height: '7px',
    borderRadius: '50%',
    flexShrink: 0,
    transition: 'background 0.3s',
  },
  roomCode: {
    fontSize: '13px',
    fontWeight: '600',
    letterSpacing: '1.5px',
    color: 'var(--text-dim)',
    fontFamily: 'monospace',
  },
  shareBtn: {
    padding: '6px 14px',
    background: 'transparent',
    border: '1px solid var(--border)',
    borderRadius: '100px',
    color: 'var(--text)',
    fontSize: '13px',
    cursor: 'pointer',
  },
  notifBtn: {
    padding: '6px 10px',
    background: 'transparent',
    border: '1px solid var(--border)',
    borderRadius: '100px',
    fontSize: '14px',
    cursor: 'pointer',
  },
  emojiBar: {
    display: 'flex',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: '20px 16px 16px',
    gap: '12px',
  },
  emojiBtn: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '6px',
    padding: '18px 8px',
    background: 'var(--surface)',
    border: '1px solid var(--border)',
    borderRadius: '20px',
    cursor: 'pointer',
    transition: 'transform 0.12s, border-color 0.12s',
  },
  emojiBtnActive: {
    transform: 'scale(0.92)',
    borderColor: 'var(--accent)',
    background: '#1a1f10',
  },
  emojiGlyph: {
    fontSize: '36px',
    lineHeight: 1,
  },
  emojiLabel: {
    fontSize: '11px',
    color: 'var(--text-dim)',
    letterSpacing: '0.04em',
  },
}

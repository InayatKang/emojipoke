import React, { useState, useEffect, useRef } from 'react'
import Pusher from 'pusher-js'

const EMOJIS = [
  { emoji: '📍', label: 'Uni', id: 'Uni' },
  //{ emoji: '🚗', label: 'leaving', id: 'leaving' },
  { emoji: '🥐', label: 'lunch', id: 'lunch' },
]

const PUSHER_KEY = import.meta.env.VITE_PUSHER_KEY
const PUSHER_CLUSTER = import.meta.env.VITE_PUSHER_CLUSTER || 'us3'

export default function Room({ roomId }) {
  const [received, setReceived] = useState(null)
  const [sent, setSent] = useState(null)
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
    setSent(item)
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

      <div style={styles.receivedArea}>
        <div style={styles.displayBox}>
          <span style={styles.boxLabel}>them</span>
          {received
            ? <div key={receivedKey} style={styles.bigEmoji}>{received.emoji}</div>
            : <div style={styles.placeholderBox} />}
        </div>
        <div style={styles.divider} />
        <div style={styles.displayBox}>
          <span style={styles.boxLabel}>you</span>
          {sent
            ? <div style={styles.bigEmoji}>{sent.emoji}</div>
            : <div style={styles.placeholderBox} />}
        </div>
      </div>

      <div style={styles.strip}>
        <div style={styles.roomInfo}>
          <div style={{
            ...styles.dot,
            background: connected ? 'var(--accent)' : 'var(--text-dim)',
            boxShadow: connected ? '0 0 6px var(--accent)' : 'none'
          }} />
          <span style={styles.roomCode}>{roomId}</span>
        </div>
        <button style={styles.shareBtn} onClick={shareRoom}>
          {copied ? '✓ Copied' : 'Invite'}
        </button>
        {notifPerm === 'default' && (
          <button style={styles.notifBtn} onClick={requestNotifs}>🔔</button>
        )}
      </div>

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
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    padding: '0 24px',
    gap: '16px',
  },
  displayBox: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px',
  },
  boxLabel: {
    fontSize: '12px',
    color: 'var(--text-dim)',
    letterSpacing: '0.1em',
    textTransform: 'uppercase',
    fontWeight: '600',
  },
  bigEmoji: {
    fontSize: '80px',
    lineHeight: 1,
    filter: 'drop-shadow(0 0 30px rgba(200,240,122,0.25))',
  },
  placeholderBox: {
    width: '90px',
    height: '90px',
    borderRadius: '24px',
    border: '2px dashed var(--border)',
  },
  divider: {
    width: '1px',
    height: '80px',
    background: 'var(--border)',
    flexShrink: 0,
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

import React, { useState } from 'react'

const s = {
  container: {
    height: '100dvh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '32px 24px',
    gap: '48px',
  },
  hero: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px',
  },
  heroEmojis: {
    fontSize: '36px',
    display: 'flex',
    gap: '16px',
    marginBottom: '8px',
  },
  title: {
    fontSize: '48px',
    fontWeight: '700',
    letterSpacing: '-1px',
    color: 'var(--accent)',
  },
  subtitle: {
    fontSize: '15px',
    color: 'var(--text-dim)',
    textAlign: 'center',
    lineHeight: '1.5',
  },
  actions: {
    width: '100%',
    maxWidth: '320px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  primary: {
    width: '100%',
    padding: '16px',
    background: 'var(--accent)',
    color: '#0a0a0a',
    border: 'none',
    borderRadius: 'var(--radius)',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  secondary: {
    width: '100%',
    padding: '16px',
    background: 'var(--surface)',
    color: 'var(--text)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    fontSize: '16px',
    fontWeight: '500',
    cursor: 'pointer',
  },
  divider: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    color: 'var(--text-dim)',
    fontSize: '13px',
  },
  joinRow: {
    display: 'flex',
    gap: '8px',
  },
  input: {
    flex: 1,
    padding: '14px 16px',
    background: 'var(--surface)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    color: 'var(--text)',
    fontSize: '16px',
    letterSpacing: '2px',
    fontWeight: '600',
    outline: 'none',
  },
  joinBtn: {
    padding: '14px 20px',
    background: 'var(--accent)',
    color: '#0a0a0a',
    border: 'none',
    borderRadius: 'var(--radius)',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
  },
}

export default function Home({ onCreate, onJoin }) {
  const [code, setCode] = useState('')
  const [joining, setJoining] = useState(false)

  return (
    <div style={s.container}>
      <div style={s.hero}>
        <div style={s.heroEmojis}>
          <span>📍</span><span>🚗</span><span>🥐</span>
        </div>
        <h1 style={s.title}>Poke</h1>
        <p style={s.subtitle}>poking emojis bc why not</p>
      </div>

      <div style={s.actions}>
        <button style={s.primary} onClick={onCreate}>Create a room</button>

        <div style={s.divider}>
          <span style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
          <span>or</span>
          <span style={{ flex: 1, height: '1px', background: 'var(--border)' }} />
        </div>

        {joining ? (
          <div style={s.joinRow}>
            <input
              style={s.input}
              placeholder="Room code"
              value={code}
              onChange={e => setCode(e.target.value.toUpperCase())}
              maxLength={8}
              autoFocus
              autoCapitalize="characters"
            />
            <button
              style={{ ...s.joinBtn, opacity: code.trim() ? 1 : 0.4 }}
              onClick={() => code.trim() && onJoin(code)}
            >
              Join
            </button>
          </div>
        ) : (
          <button style={s.secondary} onClick={() => setJoining(true)}>
            Join a room
          </button>
        )}
      </div>
    </div>
  )
}

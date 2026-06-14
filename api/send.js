import Pusher from 'pusher'

const pusher = new Pusher({
  appId: process.env.PUSHER_APP_ID,
  key: process.env.PUSHER_KEY,
  secret: process.env.PUSHER_SECRET,
  cluster: process.env.PUSHER_CLUSTER || 'us3',
  useTLS: true,
})

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { roomId, emoji, label, id } = req.body

  if (!roomId || !emoji) {
    return res.status(400).json({ error: 'Missing roomId or emoji' })
  }

  try {
    await pusher.trigger(`room-${roomId}`, 'emoji-sent', { emoji, label, id, ts: Date.now() })
    res.status(200).json({ ok: true })
  } catch (err) {
    console.error(err)
    res.status(500).json({ error: 'Failed to send' })
  }
}

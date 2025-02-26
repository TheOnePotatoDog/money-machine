import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Chat() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [agent, setAgent] = useState('money')     // selected agent type
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState([])    // chat history in current session

  useEffect(() => {
    // Fetch current user profile (to get email and credits)
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }
    fetch(`${API_URL}/user/me`, {
      headers: { 'Authorization': 'Bearer ' + token }
    })
      .then(res => res.ok ? res.json() : Promise.reject(res))
      .then(data => setUser(data))
      .catch(err => {
        console.error('Failed to fetch user info', err)
        // If token is invalid/expired, force logout
        localStorage.removeItem('token')
        navigate('/login')
      })
  }, [navigate])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!prompt.trim()) return
    const token = localStorage.getItem('token')
    if (!token) {
      alert('Session expired. Please log in again.')
      navigate('/login')
      return
    }
    // Append the user's message to the chat
    const userMessage = { role: 'user', content: prompt }
    setMessages(prev => [...prev, userMessage])
    const query = prompt  // store current prompt
    setPrompt('')         // clear input

    try {
      const res = await fetch(`${API_URL}/ai/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ prompt: query, agent: agent })
      })
      if (!res.ok) {
        const errData = await res.json()
        alert(errData.detail || 'Error: failed to get AI response.')
        // If it's a credits issue, user can buy more credits
        return
      }
      const data = await res.json()
      if (data.answer) {
        const aiMessage = { role: 'assistant', content: data.answer }
        setMessages(prev => [...prev, aiMessage])
      }
    } catch (err) {
      console.error('Error sending query:', err)
      alert('Failed to communicate with the AI agent. Please try again.')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  const startCheckout = async () => {
    // Initiate Stripe checkout by calling backend
    const token = localStorage.getItem('token')
    if (!token) return navigate('/login')
    try {
      const res = await fetch(`${API_URL}/payments/checkout`, {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token }
      })
      if (res.ok) {
        const data = await res.json()
        // Redirect user to Stripe's checkout page
        window.location.href = data.checkout_url
      } else {
        alert('Failed to initiate checkout session.')
      }
    } catch (err) {
      console.error('Checkout error:', err)
      alert('Unable to start checkout. Please try again.')
    }
  }

  return (
    <div>
      {/* Top bar with user info and actions */}
      <div style={{ marginBottom: '1em' }}>
        {user && <span>Logged in as <strong>{user.email}</strong> — Credits: <strong>{user.credits}</strong></span>}
        <button onClick={handleLogout} style={{ marginLeft: '1em' }}>Logout</button>
        <button onClick={startCheckout} style={{ marginLeft: '1em' }}>Buy Credits</button>
      </div>

      {/* Agent selector */}
      <div>
        <label>
          Agent: 
          <select value={agent} onChange={e => setAgent(e.target.value)} style={{ marginLeft: '0.5em' }}>
            <option value="money">Money Machine</option>
            <option value="safety">Safety Machine</option>
          </select>
        </label>
      </div>

      {/* Chat message display */}
      <div style={{ border: '1px solid #ccc', padding: '1em', margin: '1em 0', height: '300px', overflowY: 'auto' }}>
        {messages.map((msg, idx) => (
          <p key={idx}>
            <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong> {msg.content}
          </p>
        ))}
      </div>

      {/* Input form for new prompt */}
      <form onSubmit={handleSend}>
        <input 
          type="text" 
          value={prompt} 
          onChange={e => setPrompt(e.target.value)} 
          placeholder="Type your question..." 
          style={{ width: '80%' }}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

export default Chat

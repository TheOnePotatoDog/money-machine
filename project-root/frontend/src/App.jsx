import { Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './components/Login'
import Register from './components/Register'
import Chat from './components/Chat'
import PaymentSuccess from './components/PaymentSuccess'
import PaymentCancel from './components/PaymentCancel'
import { API_URL } from './config'

function App() {
  const token = localStorage.getItem('token')
  const [credits, setCredits] = useState(0)

  useEffect(() => {
    // Fetch user info if logged in
    if (token) {
      fetchUserInfo()
    }
  }, [token])

  const fetchUserInfo = async () => {
    try {
      const response = await fetch(`${API_URL}/user/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setCredits(data.credits)
      }
    } catch (error) {
      console.error('Error fetching user info:', error)
    }
  }

  const addFreeCredits = async () => {
    try {
      const response = await fetch(`${API_URL}/ai/free-credits`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      if (response.ok) {
        const data = await response.json()
        setCredits(data.current_credits)
        alert('Added 10 free credits!')
      }
    } catch (error) {
      console.error('Error adding free credits:', error)
    }
  }

  return (
    <div className="app-container">
      {token && (
        <div className="app-header" style={{ padding: '10px', background: '#f0f0f0', display: 'flex', justifyContent: 'space-between' }}>
          <div>Credits: {credits}</div>
          <button onClick={addFreeCredits} style={{ padding: '5px 10px' }}>
            Get Free Credits
          </button>
        </div>
      )}
      <Routes>
        {/* Protected main route: if no token, redirect to login */}
        <Route path="/" element={token ? <Chat /> : <Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/payment/success" element={<PaymentSuccess />} />
        <Route path="/payment/cancel" element={<PaymentCancel />} />
      </Routes>
    </div>
  )
}

export default App

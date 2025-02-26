import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function PaymentSuccess() {
  const [credits, setCredits] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      // Fetch updated user credits after purchase
      fetch(`${API_URL}/user/me`, {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data) setCredits(data.credits)
        })
        .catch(err => console.error('Failed to fetch updated credits:', err))
    }
  }, [])

  return (
    <div>
      <h2>Payment Successful</h2>
      <p>Thank you for your purchase!</p>
      {credits !== null && (
        <p>Your new balance is <strong>{credits}</strong> credits.</p>
      )}
      <p><Link to="/">Back to App</Link></p>
    </div>
  )
}

export default PaymentSuccess

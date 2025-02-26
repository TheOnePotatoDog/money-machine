import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Register() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleRegister = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      if (!res.ok) {
        const data = await res.json()
        alert(data.detail || 'Registration failed')
        return
      }
      alert('Registration successful! Please log in.')
      navigate('/login')
    } catch (err) {
      console.error('Register error:', err)
      alert('Unable to register. Please try again.')
    }
  }

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>
            Email: 
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          </label>
        </div>
        <div>
          <label>
            Password: 
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </label>
        </div>
        <button type="submit">Register</button>
      </form>
      <p>Have an account? <Link to="/login">Log in</Link>.</p>
    </div>
  )
}

export default Register

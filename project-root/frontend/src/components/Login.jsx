import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      if (!res.ok) {
        const data = await res.json()
        alert(data.detail || 'Login failed')
        return
      }
      const data = await res.json()
      localStorage.setItem('token', data.access_token)
      // Redirect to main app after successful login
      navigate('/')
    } catch (err) {
      console.error('Login error:', err)
      alert('Unable to login. Please try again.')
    }
  }

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
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
        <button type="submit">Login</button>
      </form>
      <p>No account? <Link to="/register">Register here</Link>.</p>
    </div>
  )
}

export default Login

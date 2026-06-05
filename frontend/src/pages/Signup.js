import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import API_BASE from '../config';

function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    try {
      await axios.post(`${API_BASE}/signup`, form);
      const loginRes = await axios.post(`${API_BASE}/login`, { email: form.email, password: form.password });
      localStorage.setItem('token', loginRes.data.token);
      localStorage.setItem('username', loginRes.data.username);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Signup failed');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h1 style={styles.logo}>SERIALSENSE</h1>
        <h3 style={styles.title}>CREATE YOUR ACCOUNT</h3>
        {error && <p style={styles.error}>{error}</p>}
        <input style={styles.input} name="username" placeholder="Username" onChange={handleChange} autoComplete="off" />
        <input style={styles.input} name="email" placeholder="Email" onChange={handleChange} autoComplete="off" />
        <input style={styles.input} name="password" placeholder="Password" type="password" onChange={handleChange} autoComplete="new-password" />
        <button style={styles.btn} onClick={handleSubmit}>Sign Up</button>
        <p style={styles.link} onClick={() => navigate('/login')}>Already have an account? Log in</p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: "'Orbitron', sans-serif",
  },
  box: {
    backgroundColor: 'rgba(10, 20, 30, 0.85)',
    padding: '50px 40px',
    borderRadius: '16px',
    width: '400px',
    border: '1px solid rgba(0, 200, 150, 0.3)',
    backdropFilter: 'blur(10px)',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
    boxShadow: '0 8px 40px rgba(0, 200, 150, 0.15)',
  },
  logo: {
    background: 'linear-gradient(135deg, #00d4aa, #00ff88)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    fontSize: '28px',
    fontWeight: '900',
    letterSpacing: '4px',
    textAlign: 'center',
    margin: '0 0 8px',
  },
  title: {
    color: '#a0d8c8',
    fontSize: '13px',
    letterSpacing: '3px',
    textAlign: 'center',
    margin: '0 0 16px',
    fontWeight: 'normal',
  },
  input: {
    width: '100%',
    padding: '14px',
    borderRadius: '8px',
    border: '1px solid rgba(0, 200, 150, 0.3)',
    backgroundColor: 'rgba(0, 20, 15, 0.6)',
    color: '#fff',
    fontSize: '13px',
    fontFamily: "'Orbitron', sans-serif",
    letterSpacing: '1px',
    boxSizing: 'border-box',
    outline: 'none',
  },
  btn: {
    width: '100%',
    padding: '14px',
    background: 'linear-gradient(135deg, #00b894, #00d4aa)',
    border: 'none',
    borderRadius: '8px',
    color: '#000',
    fontWeight: 'bold',
    cursor: 'pointer',
    fontSize: '14px',
    letterSpacing: '2px',
    fontFamily: "'Orbitron', sans-serif",
    marginTop: '8px',
  },
  error: {
    color: '#ff4d4d',
    textAlign: 'center',
    fontSize: '11px',
    letterSpacing: '1px',
  },
  link: {
    color: '#7ab8a8',
    textAlign: 'center',
    cursor: 'pointer',
    fontSize: '10px',
    letterSpacing: '2px',
    marginTop: '8px',
  },
};

export default Signup;
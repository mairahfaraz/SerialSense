import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

function Dashboard() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const token = localStorage.getItem('token');

  const [robotType, setRobotType] = useState('Line Follower');
  const [arduinoType, setArduinoType] = useState('Arduino Uno');
  const [motorDriver, setMotorDriver] = useState('L298N');
  const [goal, setGoal] = useState('');
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [inoFile, setInoFile] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [loading, setLoading] = useState('');

  const headers = { Authorization: `Bearer ${token}` };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/');
  };

  const startSession = async () => {
    setLoading('Starting session...');
    try {
      const res = await axios.post('http://127.0.0.1:5000/start_session', {
        robot_type: robotType,
        arduino_type: arduinoType,
        motor_driver: motorDriver,
        goal
      }, { headers });
      setMessages([{ role: 'assistant', content: res.data.message }]);
    } catch (err) {
      if (err.response?.status === 429) {
        setMessages([{ role: 'assistant', content: "You've reached today's free message limit. Please try again tomorrow!" }]);
      } else {
        alert('Failed to start session');
      }
    }
    setLoading('');
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;
    const newMessages = [...messages, { role: 'user', content: userInput }];
    setMessages(newMessages);
    setUserInput('');
    setLoading('Thinking...');
    try {
      const res = await axios.post('http://127.0.0.1:5000/chat', { message: userInput }, { headers });
      setMessages([...newMessages, { role: 'assistant', content: res.data.reply }]);
    } catch (err) {
      if (err.response?.status === 429) {
        setMessages(prev => [...prev, { role: 'assistant', content: "You've reached today's free message limit. Please try again tomorrow!" }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Something went wrong. Please try again.' }]);
      }
    }
    setLoading('');
  };

  const analyzeCode = async () => {
    if (!inoFile) return alert('Please select a .ino file first');
    setLoading('Analyzing code...');
    const formData = new FormData();
    formData.append('file', inoFile);
    try {
      const res = await axios.post('http://127.0.0.1:5000/analyze_code', formData, { headers });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.analysis }]);
    } catch (err) {
      if (err.response?.status === 429) {
        setMessages(prev => [...prev, { role: 'assistant', content: "You've reached today's free message limit. Please try again tomorrow!" }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Analysis failed. Please try again.' }]);
      }
    }
    setLoading('');
  };

  const analyzeVideo = async () => {
    if (!videoFile) return alert('Please select a video file first');
    setLoading('Analyzing video... this may take a moment');
    const formData = new FormData();
    formData.append('video', videoFile);
    try {
      const res = await axios.post('http://127.0.0.1:5000/analyze_video', formData, { headers });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.diagnosis }]);
    } catch (err) {
      if (err.response?.status === 429) {
        setMessages(prev => [...prev, { role: 'assistant', content: "You've reached today's free message limit. Please try again tomorrow!" }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Analysis failed. Please try again.' }]);
      }
    }
    setLoading('');
  };

  return (
    <div style={styles.container}>
      {/* NAVBAR */}
      <nav style={styles.navbar}>
        <h1 style={styles.logo}>SERIALSENSE</h1>
        <div style={styles.navRight}>
          <span style={styles.welcome}>HEY, {username?.toUpperCase()}!</span>
          <button style={styles.logoutBtn} onClick={handleLogout}>LOG OUT</button>
        </div>
      </nav>

      <div style={styles.main}>
        {/* LEFT PANEL */}
        <div style={styles.leftPanel}>
          <h3 style={styles.sectionTitle}>PROJECT SETUP</h3>

          <label style={styles.label}>ROBOT TYPE</label>
          <select style={styles.select} onChange={e => setRobotType(e.target.value)}>
            <option>Line Follower</option>
            <option>Obstacle Avoider</option>
            <option>Bluetooth Controlled</option>
            <option>IR Remote Controlled</option>
            <option>Sumo Robot</option>
          </select>

          <label style={styles.label}>ARDUINO BOARD</label>
          <select style={styles.select} onChange={e => setArduinoType(e.target.value)}>
            <option>Arduino Uno</option>
            <option>Arduino Nano</option>
            <option>Arduino Mega</option>
            <option>Arduino Leonardo</option>
            <option>Arduino Pro Mini</option>
          </select>

          <label style={styles.label}>MOTOR DRIVER</label>
          <select style={styles.select} onChange={e => setMotorDriver(e.target.value)}>
            <option>L298N</option>
            <option>L293D</option>
            <option>TB6612FNG</option>
            <option>L9110S</option>
            <option>DRV8833</option>
          </select>

          <label style={styles.label}>WHAT SHOULD YOUR ROBOT DO?</label>
          <textarea style={styles.textarea} placeholder="Describe your goal..." onChange={e => setGoal(e.target.value)} />

          <button style={styles.primaryBtn} onClick={startSession}>START SESSION</button>

          <div style={styles.divider} />

          <h3 style={styles.sectionTitle}>CODE ANALYSIS</h3>
          <input type="file" accept=".ino" style={styles.fileInput} onChange={e => setInoFile(e.target.files[0])} />
          <button style={styles.secondaryBtn} onClick={analyzeCode}>ANALYZE CODE</button>

          <div style={styles.divider} />

          <h3 style={styles.sectionTitle}>VIDEO DIAGNOSIS</h3>
          <input type="file" accept="video/*" style={styles.fileInput} onChange={e => setVideoFile(e.target.files[0])} />
          <button style={styles.secondaryBtn} onClick={analyzeVideo}>ANALYZE VIDEO</button>
        </div>

        {/* RIGHT PANEL - CHAT */}
        <div style={styles.rightPanel}>
          <h3 style={styles.sectionTitle}>CHAT WITH SERIALSENSE</h3>
          <div style={styles.chatBox}>
            {messages.length === 0 && (
              <p style={styles.placeholder}>Start a session to begin chatting...</p>
            )}
            {messages.map((msg, i) => (
              <div key={i} style={msg.role === 'user' ? styles.userMsg : styles.assistantMsg}>
                <strong style={styles.msgLabel}>{msg.role === 'user' ? 'YOU' : 'SERIALSENSE'}:</strong>
                <ReactMarkdown style={{ margin: '6px 0 0', lineHeight: '1.7', fontSize: '13px' }}>{msg.content}</ReactMarkdown>
              </div>
            ))}
            {loading && <p style={styles.loading}>{loading}</p>}
          </div>
          <div style={styles.inputRow}>
            <input
              style={styles.chatInput}
              placeholder="Ask about your project..."
              value={userInput}
              onChange={e => setUserInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
            />
            <button style={styles.primaryBtn} onClick={sendMessage}>SEND</button>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    color: '#fff',
    fontFamily: "'Orbitron', sans-serif",
  },
  navbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px 40px',
    borderBottom: '1px solid rgba(0, 200, 150, 0.2)',
    backgroundColor: 'rgba(5, 15, 20, 0.7)',
    backdropFilter: 'blur(10px)',
  },
  logo: {
    background: 'linear-gradient(135deg, #00d4aa, #00ff88)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    fontSize: '22px',
    fontWeight: '900',
    letterSpacing: '4px',
    margin: 0,
  },
  navRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
  },
  welcome: {
    color: '#7ab8a8',
    fontSize: '11px',
    letterSpacing: '2px',
  },
  logoutBtn: {
    backgroundColor: 'transparent',
    color: '#00d4aa',
    border: '1px solid rgba(0, 200, 150, 0.4)',
    padding: '8px 20px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontFamily: "'Orbitron', sans-serif",
    fontSize: '11px',
    letterSpacing: '2px',
  },
  main: {
    display: 'flex',
    gap: '24px',
    padding: '24px 40px',
    height: 'calc(100vh - 70px)',
    boxSizing: 'border-box',
  },
  leftPanel: {
    width: '300px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    backgroundColor: 'rgba(5, 15, 20, 0.6)',
    backdropFilter: 'blur(10px)',
    borderRadius: '16px',
    padding: '24px',
    border: '1px solid rgba(0, 200, 150, 0.15)',
  },
  rightPanel: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  sectionTitle: {
    color: '#00d4aa',
    margin: '8px 0 4px',
    fontSize: '12px',
    letterSpacing: '3px',
    fontWeight: 'bold',
  },
  label: {
    color: '#7ab8a8',
    fontSize: '10px',
    letterSpacing: '2px',
    marginTop: '6px',
  },
  select: {
    backgroundColor: 'rgba(0, 20, 15, 0.8)',
    color: '#fff',
    border: '1px solid rgba(0, 200, 150, 0.3)',
    borderRadius: '8px',
    padding: '10px',
    width: '100%',
    fontFamily: "'Orbitron', sans-serif",
    fontSize: '11px',
    letterSpacing: '1px',
  },
  textarea: {
    backgroundColor: 'rgba(0, 20, 15, 0.8)',
    color: '#fff',
    border: '1px solid rgba(0, 200, 150, 0.3)',
    borderRadius: '8px',
    padding: '10px',
    width: '100%',
    minHeight: '80px',
    resize: 'vertical',
    boxSizing: 'border-box',
    fontFamily: "'Orbitron', sans-serif",
    fontSize: '11px',
    letterSpacing: '1px',
  },
  primaryBtn: {
    background: 'linear-gradient(135deg, #00b894, #00d4aa)',
    color: '#000',
    border: 'none',
    padding: '12px 20px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontFamily: "'Orbitron', sans-serif",
    fontSize: '11px',
    letterSpacing: '2px',
    width: '100%',
  },
  secondaryBtn: {
    backgroundColor: 'rgba(0, 200, 150, 0.1)',
    color: '#00d4aa',
    border: '1px solid rgba(0, 200, 150, 0.3)',
    padding: '12px 20px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontFamily: "'Orbitron', sans-serif",
    fontSize: '11px',
    letterSpacing: '2px',
    width: '100%',
  },
  fileInput: {
    color: '#7ab8a8',
    fontSize: '11px',
    width: '100%',
    letterSpacing: '1px',
  },
  divider: {
    borderTop: '1px solid rgba(0, 200, 150, 0.15)',
    margin: '8px 0',
  },
  chatBox: {
    flex: 1,
    backgroundColor: 'rgba(5, 15, 20, 0.6)',
    backdropFilter: 'blur(10px)',
    borderRadius: '16px',
    padding: '20px',
    overflowY: 'auto',
    border: '1px solid rgba(0, 200, 150, 0.15)',
    display: 'flex',
    flexDirection: 'column',
    gap: '14px',
  },
  placeholder: {
    color: '#3a6a5a',
    textAlign: 'center',
    marginTop: '40px',
    fontSize: '12px',
    letterSpacing: '2px',
  },
  userMsg: {
    backgroundColor: 'rgba(0, 200, 150, 0.08)',
    border: '1px solid rgba(0, 200, 150, 0.15)',
    borderRadius: '10px',
    padding: '12px 16px',
    alignSelf: 'flex-end',
    maxWidth: '80%',
  },
  assistantMsg: {
    backgroundColor: 'rgba(0, 40, 30, 0.6)',
    border: '1px solid rgba(0, 200, 150, 0.2)',
    borderRadius: '10px',
    padding: '12px 16px',
    maxWidth: '85%',
  },
  msgLabel: {
    color: '#00d4aa',
    fontSize: '10px',
    letterSpacing: '2px',
  },
  loading: {
    color: '#00d4aa',
    fontSize: '11px',
    fontStyle: 'italic',
    letterSpacing: '2px',
  },
  inputRow: {
    display: 'flex',
    gap: '10px',
  },
  chatInput: {
    flex: 1,
    backgroundColor: 'rgba(5, 15, 20, 0.7)',
    color: '#fff',
    border: '1px solid rgba(0, 200, 150, 0.3)',
    borderRadius: '8px',
    padding: '14px',
    fontSize: '12px',
    fontFamily: "'Orbitron', sans-serif",
    letterSpacing: '1px',
    backdropFilter: 'blur(10px)',
  },
};

export default Dashboard;
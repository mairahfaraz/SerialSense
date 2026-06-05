import React from 'react';
import { useNavigate } from 'react-router-dom';
import bg from '../bg.png';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{
      backgroundImage: `url(${bg})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundAttachment: 'fixed',
      minHeight: '100vh',
      fontFamily: "'Orbitron', sans-serif",
    }}>

      {/* HERO SECTION */}
      <div style={styles.heroSection}>
        <div style={styles.leftPanel}>
          <button style={styles.btnPrimary} onClick={() => navigate('/login')}>Login</button>
          <p style={styles.dontHave}>DON'T HAVE AN ACCOUNT?</p>
          <button style={styles.btnPrimary} onClick={() => navigate('/signup')}>Sign Up</button>
        </div>

        <div style={styles.centerPanel}>
          <h1 style={styles.title}>SERIALSENSE</h1>
          <p style={styles.subtitle}>DEBUG YOUR ARDUINO ROBOT WITH AI</p>
          <p style={styles.description}>
            SERIALSENSE READS YOUR CODE,<br />
            WATCHES YOUR ROBOT MOVE,<br />
            AND TELLS YOU EXACTLY WHAT'S WRONG<br />
            AND HOW TO FIX IT
          </p>
        </div>
      </div>

      {/* FEATURES SECTION */}
      <div style={styles.featuresSection}>
        <div style={styles.topCards}>
          <div className="feature-card">
            <h3 style={styles.cardTitle}>CODE ANALYSIS</h3>
            <p style={styles.cardText}>UPLOAD YOUR .INO FILE AND GET CONTEXT-AWARE FEEDBACK SPECIFIC TO YOUR ROBOT AND HARDWARE SETUP.</p>
          </div>
          <div className="feature-card">
            <h3 style={styles.cardTitle}>AI CHAT</h3>
            <p style={styles.cardText}>ASK ANYTHING ABOUT YOUR PROJECT. SERIALSENSE KNOWS YOUR ROBOT TYPE, BOARD, AND GOAL.</p>
          </div>
        </div>
        <div style={styles.bottomCard}>
          <div className="feature-card">
            <h3 style={styles.cardTitle}>VIDEO DIAGNOSIS</h3>
            <p style={styles.cardText}>UPLOAD A VIDEO OF YOUR ROBOT MOVING. OUR ML MODEL CLASSIFIES EVERY FRAME AND DIAGNOSES FAULTS.</p>
          </div>
        </div>
      </div>

    </div>
  );
}

const styles = {
  heroSection: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '0 60px',
    gap: '200px',
  },
  leftPanel: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    gap: '20px',
    minWidth: '200px',
  },
  centerPanel: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
  },
  title: {
    fontSize: '80px',
    fontWeight: '900',
    margin: '0 0 16px',
    letterSpacing: '6px',
    background: 'linear-gradient(135deg, #00d4aa, #00ff88)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    textShadow: 'none',
  },
  subtitle: {
    fontSize: '14px',
    color: '#a0d8c8',
    letterSpacing: '4px',
    margin: '0 0 24px',
  },
  description: {
    fontSize: '12px',
    color: '#7ab8a8',
    letterSpacing: '2px',
    lineHeight: '2.2',
    margin: '0',
  },
  btnPrimary: {
    background: 'linear-gradient(135deg, #00b894, #00d4aa)',
    color: '#000',
    border: 'none',
    padding: '14px 40px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: '15px',
    letterSpacing: '1px',
    fontFamily: "'Orbitron', sans-serif",
    boxShadow: '0 4px 20px rgba(0, 200, 150, 0.3)',
    width: '100%',
  },
  dontHave: {
    color: '#7ab8a8',
    fontSize: '10px',
    letterSpacing: '2px',
    margin: '0',
  },
  featuresSection: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '30px',
    padding: '60px 40px',
  },
  topCards: {
    display: 'flex',
    gap: '40px',
    justifyContent: 'center',
  },
  bottomCard: {
    display: 'flex',
    justifyContent: 'center',
  },
  card: {
    backgroundColor: 'rgba(0, 200, 150, 0.82)',
    borderRadius: '16px',
    padding: '36px 28px',
    maxWidth: '280px',
    textAlign: 'center',
    boxShadow: '0 8px 32px rgba(0, 200, 150, 0.15)',
    backdropFilter: 'blur(4px)',
  },
  cardTitle: {
    color: '#000',
    fontSize: '14px',
    fontWeight: 'bold',
    letterSpacing: '3px',
    marginBottom: '16px',
  },
  cardText: {
    color: '#002a1a',
    fontSize: '11px',
    letterSpacing: '1px',
    lineHeight: '1.9',
  },
};

export default LandingPage;
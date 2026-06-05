# SerialSense

An AI-powered Arduino robot debugging assistant that reads your code, analyzes your robot's movement, and tells you exactly what's wrong — and how to fix it.

Built by Syeda Maira Faraz — Mechatronics Engineering, NUST.

---

## What it does

- **Project Onboarding** — tell SerialSense your robot type, Arduino board, motor driver, and goal
- **Context-Aware Code Analysis** — upload your `.ino` file and get specific feedback for your exact hardware setup
- **AI Chat** — ask anything about your project mid-session
- **ML-Powered Video Diagnosis** — upload a video of your robot moving; a fine-tuned MobileNetV2 model classifies every frame and diagnoses faults like detracking, stalling, or unexpected spinning

---

## Tech Stack

**Frontend:** React, React Router, Axios

**Backend:** Python, Flask, Flask-JWT-Extended, Flask-SQLAlchemy, bcrypt

**AI:** Google Gemini API (gemini-2.5-flash)

**Machine Learning:** PyTorch, MobileNetV2 (fine-tuned on custom robot movement dataset)

**Computer Vision:** OpenCV

**Database:** SQLite

---

## Features

- Sign up / Log in with JWT authentication
- Daily message limit per user (20 free messages/day)
- Friendly error handling — no raw API errors shown to users
- Responsive dark-themed UI with Orbitron font
- ML model trained on 4 labeled classes: on_line, left, right, stopped, spin

---

## ML Model

The movement classifier was trained on real footage of a line following robot with the following classes:

- `on_line` — robot correctly following the line
- `left` — robot detracking to the left
- `right` — robot detracking to the right
- `stopped` — robot stalled
- `spin` — unexpected 360 degree rotation

**Model:** MobileNetV2 fine-tuned with PyTorch

**Validation Accuracy:** 99%

---

## Installation

**Requirements:** Python 3.10+, Node.js, a Google Gemini API key

```bash
# Clone the repo
git clone https://github.com/mairahfaraz/SerialSense.git
cd SerialSense

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors flask-jwt-extended flask-sqlalchemy bcrypt python-dotenv google-genai opencv-python torch torchvision watchdog

# Add your API key
echo GEMINI_API_KEY=your_key_here > ../.env

# Run backend
python app.py

# Frontend setup (new terminal)
cd ../frontend
npm install
npm start
```

---

## Author

**Syeda Maira Faraz**
Mechatronics Engineering, NUST Islamabad
[LinkedIn](https://www.linkedin.com/in/syedamairafaraz) · [GitHub](https://github.com/mairahfaraz)

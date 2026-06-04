# SerialSense

An AI-powered Arduino coding assistant that reads your `.ino` files in real time, detects hardware-software bugs, and delivers context-aware feedback based on your specific robot type and goal.

Built by Syeda Maira Faraz — Mechatronics Engineering, NUST.

---

## What it does

Most Arduino debugging means uploading broken code to hardware, watching it fail, and guessing why. SerialSense sits alongside Arduino IDE and catches bugs before they reach your robot.

- Tell SerialSense what you're building and what you want it to do
- Select your `.ino` file — SerialSense watches it
- Save your code in Arduino IDE
- Click Analyze Now — SerialSense reads your latest code and gives feedback specific to your robot, not generic advice
- Chat with the AI about anything in your project

---

## Screenshots

### Onboarding + live bug detection alongside Arduino IDE
![SerialSense in action]
<img width="934" height="434" alt="image" src="https://github.com/user-attachments/assets/01323ffc-65d6-462d-83b9-b4d4ac24e7d3" />



### Context-aware analysis in the chat
![SerialSense chat]
<img width="959" height="434" alt="image" src="https://github.com/user-attachments/assets/6685c3c1-7859-4e79-ae37-0aac68ae20a4" />



---

## Features

- **Project onboarding** — tell the AI your robot type, Arduino board, and goal before you start
- **Live file watching** — select your `.ino` file once, SerialSense tracks every save
- **Context-aware analysis** — feedback is specific to your robot, not generic code review
- **Real bug detection** — catches logic errors, missing pinMode declarations, incorrect motor driver usage, unused libraries, and more
- **Chat interface** — ask anything about your project mid-session
- **Code rewriting** — ask the AI to fix the bugs and it rewrites the corrected code

---

## Tech stack

- Python 3.14
- React — front-end
- Google Gemini API — AI analysis
- Watchdog — file system monitoring
- python-dotenv — environment variable management
- Flask - backend
---

## Installation

**Requirements:** Python 3.10+, a Google Gemini API key (free at aistudio.google.com)

```bash
# Clone the repo
git clone https://github.com/mairahfaraz/SerialSense.git
cd SerialSense

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install gradio google-genai python-dotenv watchdog

# Add your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run
python3 app.py
```

Then open `http://127.0.0.1:7860` in your browser.

---

## How to use

1. Open SerialSense in your browser
2. Select your robot type, Arduino board, and describe your goal
3. Click **Start Session**, the AI greets you and confirms your project
4. Open your `.ino` file in Arduino IDE as usual
5. In SerialSense, click **Select your .ino file** and choose the same file
6. Write code in Arduino IDE, save with `Command+S` (Mac) or `Ctrl+S` (Windows)
7. Click **Analyze Now** — feedback appears in the chat
8. Ask follow-up questions or request a rewrite in the chat

---

## Roadmap

- [x] Project onboarding and context engine
- [x] Live `.ino` file reading and watching
- [x] Context-aware AI code analysis
- [ ] Serial monitor integration — stream live Arduino output into the app
- [ ] Camera-based robot behavior analysis — watch the physical robot move and diagnose issues from video

---

## Author

**Syeda Maira Faraz**  
Mechatronics Engineering, NUST Islamabad  
[LinkedIn](https://www.linkedin.com/in/syedamairafaraz) · [GitHub](https://github.com/mairahfaraz)

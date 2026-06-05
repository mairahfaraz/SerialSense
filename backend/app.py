from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import os
import sys
from datetime import date
from werkzeug.utils import secure_filename
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
if not os.getenv('GEMINI_API_KEY'):
    os.environ['GEMINI_API_KEY'] = 'AQ.Ab8RN6J59oD83AYjqdaY8fqMqb5-q27Xr-5S87t1_mYmZaJ_mg'

from google import genai
from google.genai import types
import cv2
from camera import analyze_video

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serialsense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'serialsense-secret-key-change-in-production'
app.config['JWT_ALGORITHM'] = 'HS256'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ---------- MODELS ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    count = db.Column(db.Integer, default=0)

# ---------- HELPERS ----------
DAILY_LIMIT = 20
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)
session_store = {}

def check_and_increment_limit(user_id):
    today = str(date.today())
    log = MessageLog.query.filter_by(user_id=user_id, date=today).first()
    if not log:
        log = MessageLog(user_id=user_id, date=today, count=0)
        db.session.add(log)
    if log.count >= DAILY_LIMIT:
        return False
    log.count += 1
    db.session.commit()
    return True


def handle_gemini_error(e):
    print(f"GEMINI ERROR: {str(e)}")  # add this line
    error_str = str(e).lower()
    if '429' in error_str or 'quota' in error_str or 'resource_exhausted' in error_str or 'rate limit' in error_str:
        return jsonify({'error': 'DAILY_LIMIT_REACHED'}), 429
    return jsonify({'error': 'AI service unavailable. Please try again later.'}), 500

# ---------- ROUTES ----------
@app.route('/test_token', methods=['GET'])
@jwt_required()
def test_token():
    user = get_jwt_identity()
    return jsonify({'user': user}), 200

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, email=email, password=hashed.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'username': user.username}), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f"Hello {current_user}!"}), 200

@app.route('/start_session', methods=['POST'])
@jwt_required()
def start_session():
    print("start_session called")
    user = get_jwt_identity()
    data = request.get_json()
    robot_type = data.get('robot_type')
    arduino_type = data.get('arduino_type')
    motor_driver = data.get('motor_driver')
    goal = data.get('goal')

    context = f"Robot type: {robot_type}, Arduino: {arduino_type}, Motor Driver: {motor_driver}, Goal: {goal}"
    session_store[user] = {'context': context, 'history': []}

    prompt = f"""You are SerialSense, an AI assistant helping a student build an Arduino based robot.
Here is what they told you about their project:
- Robot type: {robot_type}
- Arduino type: {arduino_type}
- Motor driver: {motor_driver}
- Goal: {goal}
Greet them, confirm you understand their project. Keep it friendly, specific, and under 100 words."""

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return jsonify({'message': response.text}), 200
    except Exception as e:
        return handle_gemini_error(e)

@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    print("start_session called")
    user = get_jwt_identity()
    if not check_and_increment_limit(int(user)):
        return jsonify({'error': 'DAILY_LIMIT_REACHED'}), 429

    data = request.get_json()
    user_message = data.get('message')
    session = session_store.get(user, {'context': '', 'history': []})

    history_text = ""
    for msg in session['history']:
        role = "User" if msg['role'] == 'user' else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are SerialSense, an AI assistant helping a student build an Arduino based robot.
Project context: {session['context']}
Conversation so far:
{history_text}
User: {user_message}"""

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        reply = response.text
        session['history'].append({'role': 'user', 'content': user_message})
        session['history'].append({'role': 'assistant', 'content': reply})
        session_store[user] = session
        return jsonify({'reply': reply}), 200
    except Exception as e:
        return handle_gemini_error(e)

@app.route('/analyze_code', methods=['POST'])
@jwt_required()
def analyze_code():
    user = get_jwt_identity()
    if not check_and_increment_limit(int(user)):
        return jsonify({'error': 'DAILY_LIMIT_REACHED'}), 429

    session = session_store.get(user, {'context': ''})
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    code = file.read().decode('utf-8')

    prompt = f"""You are SerialSense analyzing Arduino code.
Project context: {session['context']}
Give specific feedback relevant to their exact robot type and goal.
Point out bugs, improvements, and upload readiness.
Under 150 words. Code: {code}"""

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return jsonify({'analysis': response.text}), 200
    except Exception as e:
        return handle_gemini_error(e)

@app.route('/analyze_video', methods=['POST'])
@jwt_required()
def analyze_video_route():
    user = get_jwt_identity()
    if not check_and_increment_limit(int(user)):
        return jsonify({'error': 'DAILY_LIMIT_REACHED'}), 429

    session = session_store.get(user, {'context': ''})
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400

    video_file = request.files['video']
    suffix = os.path.splitext(video_file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        video_file.save(tmp.name)
        tmp_path = tmp.name

    summary, snapshot = analyze_video(tmp_path)
    os.unlink(tmp_path)

    try:
        if snapshot is not None:
            _, buffer = cv2.imencode('.jpg', snapshot)
            image_bytes = buffer.tobytes()
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    f"""You are SerialSense analyzing a robot's physical behavior through a video file.
Project context: {session['context']}

IMPORTANT - Frame by frame ML classification results from the video:
{summary}

FIRST, look at the image carefully. If you do not see a robot or any robotic hardware (wheels, motors, Arduino, sensors, tracks), immediately respond with: "This doesn't appear to be a robot. Please upload a video of your actual Arduino robot moving on a track." Do not give any diagnosis if no robot is visible.
If robot is visible, use the frame by frame classification summary below as your primary source of truth for diagnosing the robot's behavior. Ignore any motion summary statements that contradict the classification data.
These classifications were made by a trained MobileNetV2 model on every frame of the video.

Based on the classification percentages:
- If 'spin' is detected, flag it as a fault unless the user mentioned spinning as a requirement
- If 'left' or 'right' is high, the robot is detracking
- If 'stopped' is high, the robot is stalling
- If 'on_line' is dominant, the robot is performing correctly

Give a specific diagnosis and actionable fixes based on the classification data. Under 150 words."""
                ]
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Motion summary: {summary}\nContext: {session['context']}"
            )
        return jsonify({'diagnosis': response.text}), 200
    except Exception as e:
        return handle_gemini_error(e)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
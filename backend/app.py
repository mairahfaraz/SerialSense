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
    user = get_jwt_identity()
    data = request.get_json()
    robot_type = data.get('robot_type')
    arduino_type = data.get('arduino_type')
    motor_driver = data.get('motor_driver')
    goal = data.get('goal')
    context = f"Robot type: {robot_type}, Arduino: {arduino_type}, Motor Driver: {motor_driver}, Goal: {goal}"
    session_store[user] = {'context': context, 'history': [], 'current_code': ''}
    return jsonify({'message': f"Hey! I'm SerialSense, your Arduino debugging assistant. I can see you're building a **{robot_type}** using an **{arduino_type}** with an **{motor_driver}** motor driver. Your goal: *{goal}*. I've got full context of your project — upload your `.ino` file anytime for a code review, or ask me anything. Let's get your robot working perfectly!"}), 200


@app.route('/start_session', methods=['POST'])
@jwt_required()
def start_session():
    user = get_jwt_identity()
    data = request.get_json()
    robot_type = data.get('robot_type')
    arduino_type = data.get('arduino_type')
    motor_driver = data.get('motor_driver')
    goal = data.get('goal')

    context = f"Robot type: {robot_type}, Arduino: {arduino_type}, Motor Driver: {motor_driver}, Goal: {goal}"
    session_store[user] = {'context': context, 'history': [], 'current_code': ''}

    prompt = f"""You are SerialSense, an AI assistant helping a student build an Arduino based robot.
Here is what they told you about their project:
- Robot type: {robot_type}
- Arduino type: {arduino_type}
- Motor driver: {motor_driver}
- Goal: {goal}
Greet them, confirm you understand their project. Keep it friendly, specific, and under 100 words."""

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return jsonify({'message': response.text}), 200
    except Exception as e:
        return handle_gemini_error(e)
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
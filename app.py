import gradio as gr
from google import genai
from dotenv import load_dotenv
import os
os.environ["OPENCV_AVFOUNDATION_SKIP_AUTH"] = "1"
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from templates import get_template
from camera import run_camera_session, analyze_video
import cv2 

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

current_file_path = None
session_context = ""
latest_analysis = ""
observer = None

class ArduinoFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global latest_analysis
        if current_file_path and event.src_path == current_file_path:
            time.sleep(0.5)
            with open(current_file_path, 'r') as f:
                code = f.read()
            prompt = f"""You are SerialSense analyzing Arduino code in real time.
Give short specific feedback about bugs, improvements, upload readiness.
Under 100 words. Code: {code}"""
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt)
            latest_analysis = response.text

def start_watching(file):
    global current_file_path, observer
    if file is None:
        return "No file selected"
    if observer:
        observer.stop()
    current_file_path = file.name
    observer = Observer()
    handler = ArduinoFileHandler()
    observer.schedule(handler,
                      path=os.path.dirname(current_file_path),
                      recursive=False)
    observer.start()
    return f"Watching: {os.path.basename(current_file_path)}"

def get_analysis():
    return latest_analysis

def start_session(robot_type, arduino_type, motor_driver, goal):
    global session_context
    templaye = get_template(robot_type, motor_driver)
    session_context = f"Robot type: {robot_type}, Arduino: {arduino_type}, Motor Driver: {motor_driver}, Goal: {goal}"
    prompt = f"""You are SerialSense, an AI assistant helping a student build an Arduino based robot.
Here is what they told you about their project:
- Robot type: {robot_type}
- Arduino type: {arduino_type}
- Motor driver: {motor_driver}
- Goal: {goal}
Greet them, confirm you understand their project.
Keep it friendly, specific, and under 100 words."""
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt)
    greeting = response.text
    return [{"role": "assistant", "content": greeting}]

def chat(user_message, history):
    messages = ""
    for msg in history:
        if msg["role"] == "user":
            messages += f"User: {msg['content']}\n"
        else:
            messages += f"Assistant: {msg['content']}\n"
    prompt = f"""You are SerialSense, an AI assistant helping a student build an Arduino based robot.
Keep responses friendly, helpful, and focused on their Arduino project.
Conversation so far:
{messages}
User: {user_message}"""
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt)
    reply = response.text
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    return "", history

def analyze_and_chat(history):
    if current_file_path is None:
        history.append({"role": "assistant", "content": "No file selected. Please select your .ino file first."})
        return history
    with open(current_file_path, 'r') as f:
        code = f.read()
    prompt = f"""You are SerialSense analyzing Arduino code.
The user's project context: {session_context}
Give specific feedback relevant to their exact robot type and goal.
Point out bugs, improvements, and upload readiness.
Under 150 words. Code: {code}"""
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt)
    history.append({"role": "assistant", "content": response.text})
    return history

def start_analysis(duration, history):
    global camera_stop_flag
    camera_stop_flag = False
    summary, snapshot = run_camera_session(duration, lambda: camera_stop_flag)
    
    from google.genai import types
    
    if snapshot is not None:
        _, buffer = cv2.imencode('.jpg', snapshot)
        image_bytes = buffer.tobytes()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                f"""You are SerialSense analyzing a robot's physical behavior.
Project context: {session_context}
Motion summary: {summary}
Look at this image carefully. If this is not a robot, say so and ask the user to point the camera at their bot.
If it is a robot, analyze its position, the track if visible, and cross reference with the motion summary and code context.
Give specific diagnosis and fixes. Under 150 words."""
            ]
        )
    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Motion summary: {summary}\nContext: {session_context}"
        )
    
    if history is None:
        history = []
    history.append({"role": "assistant", "content": response.text})
    return history

camera_stop_flag = False

def stop_analysis(history):
    global camera_stop_flag
    camera_stop_flag = True
    if history is None: 
        history = []
    history.append({"role": "assistant", "content": "Camera analysis stopped."})
    return history

def analyze_video_chat(video_input, history):
    if history is None:
        history = []
    
    if video_input is None:
        history.append({"role": "assistant", "content": "No video uploaded. Please upload a video first."})
        return history
    
    video_path = video_input.name
    summary, snapshot = analyze_video(video_path)
    
    from google.genai import types
    
    if snapshot is not None:
        _, buffer = cv2.imencode('.jpg', snapshot)
        image_bytes = buffer.tobytes()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                f"""You are SerialSense analyzing a robot's physical behavior through a video file.
Project context: {session_context}
Motion summary: {summary}
Look at this image carefully. If this is not a robot, say so and ask the user to insert a video of their bot.
If it is a robot, analyze its position, the track if visible, and cross reference with the motion summary and code context.
Give specific diagnosis and fixes. Under 150 words."""
            ]
        )
    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Motion summary: {summary}\nContext: {session_context}"
        )
    
    history.append({"role": "assistant", "content": response.text})
    return history


with gr.Blocks(title="SerialSense") as app:
    gr.Markdown("# SerialSense")
    gr.Markdown("Tell us about your robot before we begin.")

    with gr.Row():
        robot_type = gr.Dropdown(
            label="What type of robot are you building?",
            choices=["Line Follower", "Obstacle Avoider", "Bluetooth Controlled",
                     "IR Remote Controlled", "Sumo Robot"],
            value="Line Follower")
        arduino_type = gr.Dropdown(
            label="What Arduino are you using?",
            choices=["Arduino Uno", "Arduino Nano", "Arduino Mega",
                     "Arduino Leonardo", "Arduino Pro Mini"],
            value="Arduino Uno")
        motor_driver = gr.Dropdown(
            label="What Motor Driver are you using?",
            choices=["L298N", "L293D", "TB6612FNG", "L9110S", "DRV8833"],
            value="L298N")
        
    goal = gr.Textbox(label="What do you want your robot to do?",
                      placeholder="Describe in detail")
    submit = gr.Button("Start Session", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### Chat with SerialSense")
    chatbot = gr.Chatbot(height=400)
    user_input = gr.Textbox(placeholder="Ask anything about your project...",
                             show_label=False)
    send = gr.Button("Send", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### Live code analysis")
    file_input = gr.File(label="Select your .ino file", file_types=[".ino"])
    watch_status = gr.Textbox(label="Status", interactive=False)
    analyze_btn = gr.Button("Analyze Now", variant="secondary")
    
    gr.Markdown("---")
    gr.Markdown("### Camera Analysis")
    gr.Markdown("Point camera at your bot, set duration and click Analyze. OR upload a video of your robot")
    with gr.Row():
        duration = gr.Slider(minimum=5, maximum=30, value=10,
                         step=5, label="Recording duration (seconds)")
        camera_feed = gr.Image(sources=["webcam"],
                       streaming=True, label="Camera Feed")
        with gr.Row():
            camera_btn = gr.Button("Start Camera Analysis", variant="primary")
            stop_camera_btn = gr.Button("Stop Camera Analysis", variant="stop")
            
            video_input = gr.File(label= "Upload robot video", file_types = [".mp4", ".mov", ".avi"])
            analyze_video_btn = gr.Button("Analyze Video", variant = "primary")
            camera_running = gr.State(False)
            
            camera_btn.click(start_analysis,
                 inputs=[duration, chatbot],
                 outputs=[chatbot])
            stop_camera_btn.click(stop_analysis,
                      inputs=[chatbot],
                      outputs=[chatbot])
            analyze_video_btn.click(analyze_video_chat,
                        inputs=[video_input, chatbot],
                        outputs=[chatbot])

    
    submit.click(start_session,
                 inputs=[robot_type, arduino_type, motor_driver, goal],
                 outputs=[chatbot])
    send.click(chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    user_input.submit(chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    file_input.change(start_watching, inputs=[file_input], outputs=[watch_status])
    analyze_btn.click(analyze_and_chat, inputs = [chatbot], outputs=[chatbot])

app.launch(theme=gr.themes.Ocean())
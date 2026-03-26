import gradio as gr
from google import genai
from dotenv import load_dotenv
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

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
Give short specific feedback — bugs, improvements, upload readiness.
Under 100 words. Code: {code}"""
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", contents=prompt)
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

def start_session(robot_type, arduino_type, goal):
    global session_context
    session_context = f"Robot type: {robot_type}, Arduino: {arduino_type}, Goal: {goal}"
    prompt = f"""You are SerialSense, an AI assistant helping a student build an Arduino based robot.
Here is what they told you about their project:
- Robot type: {robot_type}
- Arduino type: {arduino_type}
- Goal: {goal}
Greet them, confirm you understand their project.
Keep it friendly, specific, and under 100 words."""
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=prompt)
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
        model="gemini-2.5-flash-lite", contents=prompt)
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
        model="gemini-2.5-flash-lite", contents=prompt)
    history.append({"role": "assistant", "content": response.text})
    return history

with gr.Blocks(title="SerialSense", theme=gr.themes.Ocean()) as app:
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

    goal = gr.Textbox(label="What do you want your robot to do?",
                      placeholder="Describe in detail")
    submit = gr.Button("Start Session", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### 💬 Chat with SerialSense")
    chatbot = gr.Chatbot(height=400)
    user_input = gr.Textbox(placeholder="Ask anything about your project...",
                             show_label=False)
    send = gr.Button("Send", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### 📂 Live code analysis")
    file_input = gr.File(label="Select your .ino file", file_types=[".ino"])
    watch_status = gr.Textbox(label="Status", interactive=False)
    analyze_btn = gr.Button("Analyze Now", variant="secondary")

    submit.click(start_session,
                 inputs=[robot_type, arduino_type, goal],
                 outputs=[chatbot])
    send.click(chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    user_input.submit(chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    file_input.change(start_watching, inputs=[file_input], outputs=[watch_status])
    analyze_btn.click(analyze_and_chat, inputs = [chatbot], outputs=[chatbot])

app.launch()
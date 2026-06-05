import cv2
import time
import os
import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
from PIL import Image

os.environ["OPENCV_AVFOUNDATION_SKIP_AUTH"] = "1"

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'robot_classifier.pth')
CLASS_NAMES = ['left', 'on_line', 'right', 'spin', 'stopped']

def load_model():
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, len(CLASS_NAMES))
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'), weights_only=True)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model

classifier = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def classify_frame(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = classifier(tensor)
        _, predicted = torch.max(output, 1)
    return CLASS_NAMES[predicted.item()]

def open_camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        return True, cap
    else:
        return False, None

def capture_frames(cap):
    ret1, frame1 = cap.read()
    time.sleep(0.1)
    ret2, frame2 = cap.read()
    if not ret1 or not ret2:
        return 0
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    motion = cv2.countNonZero(thresh)
    return motion

def analyze_motion(motion_values):
    if not motion_values:
        return "No data recorded."
    threshold = 500
    moving = [v for v in motion_values if v > threshold]
    stopped = [v for v in motion_values if v <= threshold]
    total = len(motion_values)
    moving_count = len(moving)
    stopped_count = len(stopped)
    if moving_count == 0:
        return "Robot did not move at all during the session."
    elif stopped_count == 0:
        return "Robot moved consistently throughout the session."
    elif moving_count > 0 and stopped_count > 0:
        if motion_values[-1] <= threshold:
            return f"Robot moved for {moving_count} intervals then stopped. Possible stall or end of run."
        else:
            return f"Robot showed intermittent movement — moved {moving_count} intervals, stopped {stopped_count} intervals."
    return "Motion pattern unclear."

def summarize_classifications(classifications):
    if not classifications:
        return "No classifications made."
    from collections import Counter
    counts = Counter(classifications)
    total = len(classifications)
    summary = ", ".join([f"{label}: {count/total*100:.1f}%" for label, count in counts.most_common()])
    dominant = counts.most_common(1)[0][0]
    dominant_pct = counts.most_common(1)[0][1] / total * 100
    if dominant_pct < 40:
        confidence = "LOW CONFIDENCE — subject may not be a robot or movement was unclear."
    else:
        confidence = f"HIGH CONFIDENCE — dominant behavior: {dominant}."
    return f"Frame classification summary — {summary}. {confidence}"
def run_camera_session(duration, stop_flag_func):
    success, cap = open_camera()
    if not success:
        return "Error: Camera permission denied or camera not found.", None
    motion_values = []
    classifications = []
    snapshot = None
    start_time = time.time()
    while time.time() - start_time < duration:
        if stop_flag_func():
            break
        motion = capture_frames(cap)
        motion_values.append(motion)
        ret, frame = cap.read()
        if ret:
            label = classify_frame(frame)
            classifications.append(label)
            if snapshot is None:
                snapshot = frame
    cap.release()
    cv2.destroyAllWindows()
    motion_summary = analyze_motion(motion_values)
    classification_summary = summarize_classifications(classifications)
    combined_summary = f"{motion_summary} | {classification_summary}"
    return combined_summary, snapshot

def analyze_video(video_path):
    print("DEBUG: analyze_video called with", video_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error: Could not open video file.", None
    motion_values = []
    classifications = []
    snapshot = None
    frame_count = 0
    ret, frame1 = cap.read()
    while ret:
        ret, frame2 = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 10 == 0:
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            motion = cv2.countNonZero(thresh)
            motion_values.append(motion)
            label = classify_frame(frame2)
            classifications.append(label)
            if snapshot is None:
                snapshot = frame2
        frame1 = frame2
    cap.release()
    motion_summary = analyze_motion(motion_values)
    classification_summary = summarize_classifications(classifications)
    combined_summary = f"{motion_summary} | {classification_summary}"
    return combined_summary, snapshot
import cv2
import time
import os
os.environ["OPENCV_AVFOUNDATION_SKIP_AUTH"] = "1"

def open_camera():
    cap= cv2.VideoCapture(0)
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

def run_camera_session(duration, stop_flag_func):
    success, cap = open_camera()
    if not success:
        return "Error: Camera permission denied or camera not found.", None
    
    motion_values = []
    snapshot = None
    start_time = time.time()
    
    while time.time() - start_time < duration:
        if stop_flag_func():
            break
        motion = capture_frames(cap)
        motion_values.append(motion)
        if snapshot is None:
            ret, snapshot = cap.read()
    
    cap.release()
    summary = analyze_motion(motion_values)
    return summary, snapshot
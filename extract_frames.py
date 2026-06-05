import cv2
import os

video_labels = {
    "3 seconds.mp4": [
        (0, 1, "left"),
        (2, 3, "left"),
    ],
    "4 seconds.mp4": [ 
        (0, 1, "right"),
        (2, 3, "right"),
    ],
    "11 seconds.mp4": [
        (0, 1, "on_line"),
        (1, 2, "stopped"),
        (2, 3, "on_line"),
        (3, 4, "stopped"),
        (4, 9, "on_line"),
        (10, 11, "stopped"),
    ],
    "16 seconds.mp4": [
        (0, 9, "on_line"),
        (10, 12, "spin"),
        (12, 13, "on_line"),
        (13, 14, "stopped" ),
    ],
}

output_dir = "dataset"
classes = ["on_line", "stopped", "left", "right", "spin"]
for c in classes:
    os.makedirs(f"{output_dir}/{c}", exist_ok=True)

for video_file, segments in video_labels.items():
    if not os.path.exists(video_file):
        print(f"File not found: {video_file}")
        continue

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Processing {video_file} at {fps:.1f} FPS...")

    for (start_sec, end_sec, label) in segments:
        start_frame = int(start_sec * fps)
        end_frame = int(end_sec * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        frame_count = 0
        existing = len(os.listdir(f"{output_dir}/{label}"))

        for i in range(start_frame, end_frame):
            ret, frame = cap.read()
            if not ret:
                break

            filename = f"{output_dir}/{label}/{existing + frame_count:04d}.jpg"
            cv2.imwrite(filename, frame)
            frame_count += 1

        print(f" {label}: extracted {frame_count} frames ({start_sec}s-{end_sec}s)")
    cap.release()

print("Done! Check your dataset folder.")
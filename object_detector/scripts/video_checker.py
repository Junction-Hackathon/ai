import cv2
from detect_udhiyah import detect_sacrifice_animal


def check_video_for_sacrifice_animal(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_number = 0
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_number % fps == 0:
            frames.append(frame)
        frame_number += 1
    cap.release()

    for frame in frames:
        animal = detect_sacrifice_animal(frame)
        if animal:
            return True
    return False

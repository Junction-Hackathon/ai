import cv2
import numpy as np
import os

def blur(video_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, video_path)
    output_path = os.path.join(script_dir, 'blurred_video.mp4')

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError("cannot open file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if fps == 0 or width == 0 or height == 0:
        cap.release()
        raise ValueError("error")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print("processing video...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 70, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        kernel = np.ones((25, 25), np.uint8)  
        dilated_mask = cv2.dilate(red_mask, kernel, iterations=1)
        blurred = cv2.GaussianBlur(frame, (71, 71), 0)
        frame[dilated_mask > 0] = blurred[dilated_mask > 0]


        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"output saved successfully to: {output_path}")


blur("slaughter.mp4")
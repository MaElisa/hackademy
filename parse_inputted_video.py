# run with         python3 -m flask run
from flask import Flask,render_template,Response
import mediapipe as mp
import cv2

app=Flask(__name__)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def parse_frames(path_to_video):
    if not isinstance(path_to_video, str):
        print("Invalid path format")
        return
    if path_to_video[-4:] != ".mp4":
        print("Invalid video type")
        return
    cap = cv2.VideoCapture(path_to_video)
    while True:
        # Read the camera frame
        success, frame = cap.read()
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for i in range(21):
                    print(f"{i}: {results.multi_hand_landmarks[0].landmark[i].x}")
                for handLms in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__=="__main__":
    app.run(debug=True)


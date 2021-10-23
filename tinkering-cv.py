# run with         python3 -m flask run
from flask import Flask,render_template,Response
import mediapipe as mp
import cv2

app=Flask(__name__)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

@app.route('/demo')
def demo():
    return Response(generate_frames(True),mimetype='multipart/x-mixed-replace; boundary=frame')

def chinese_calligraphy_demo():
        # Reading the image using imread() function
    cap = cv2.VideoCapture('chinese-calligraphy-demo.mp4')

    if (cap.isOpened() == False):
        print("Error opening video stream or file")
    
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def generate_frames(picture):
    cap = cv2.VideoCapture('chinese-calligraphy-demo.mp4')
    while True:
        # Read the camera frame
        success, frame = cap.read()
        if not success:
            break
        else:
          imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          results = hands.process(imgRGB)
          if results.multi_hand_landmarks:
            # print(results.multi_hand_landmarks)
            for handLms in results.multi_hand_landmarks:
              mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
              if not picture:
                  yield(mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS))
          ret,buffer=cv2.imencode('.jpg',frame)
          frame=buffer.tobytes()
        if picture :
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__=="__main__":
    app.run(debug=True)

    
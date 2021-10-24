# run with         python3 -m flask run

from flask import Flask,render_template,Response
import cv2
import mediapipe as mp
import chinese_calligraphy_demo

app=Flask(__name__)
cap=cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def generate_frames(picture):
  i = 0
  while i < 2:
      ## read the camera frame
      success,img=cap.read()
      if not success:
          break
      else:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
          print (len(results.multi_hand_landmarks))
          print(type(results.multi_hand_landmarks[0].landmark[0]))
          # for j in range(21):
          #   print(f"{j}: {results.multi_hand_landmarks[1].landmark[j].x}")
          # for j in range(21):
          #   print(f"{j}: {results.multi_hand_landmarks[0].landmark[j].x}")
          # i +=1
          for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            if not picture:
                yield(mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS))
        ret,buffer=cv2.imencode('.jpg',img)
        img=buffer.tobytes()
      if picture :
          yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/video')
def video():
    return Response(generate_frames(True),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/text')
def text():
    return Response(generate_frames(False),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tes')
def tes():

  is_working = True
  dev_port = 0
  working_ports = []
  available_ports = []
  while is_working:
      camera = cv2.VideoCapture(dev_port)
      if not camera.isOpened():
          is_working = False
          print("Port %s is not working." %dev_port)
      else:
          is_reading, img = camera.read()
          w = camera.get(3)
          h = camera.get(4)
          if is_reading:
              print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
              working_ports.append(dev_port)
          else:
              print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
              available_ports.append(dev_port)
      dev_port +=1
  print(available_ports)
  return "asdf"

@app.route('/demo')
def demo():
    return Response(chinese_calligraphy_demo.generate_frames(True),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
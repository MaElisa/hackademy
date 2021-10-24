# # run with         python3 -m flask run

# from flask import Flask,render_template,Response
# import cv2
# import mediapipe as mp
# import math
# import os
# import chinese_calligraphy_demo
# import parse_inputted_video
# import faces

# global started
# started = False
# app=Flask(__name__)
# cap=cv2.VideoCapture(0)

# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils

# folderPath = "Images"
# image = os.listdir(folderPath)
# pic = cv2.imread(f'{folderPath}/hands.png')

# def generate_frames(picture):
#   started = False
#   i = 0
#   while True:
#       ## read the camera frame
#       success,img=cap.read()
#       if not success:
#           break
#       else:
#         if not started:
#           cv2.putText(img, f'Please put your hands flat on the table!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = hands.process(imgRGB)
#         if results.multi_hand_landmarks:
#           # print (len(results.multi_hand_landmarks))
#           # print(type(results.multi_hand_landmarks[0].landmark[0]))
#           for j in range(10,13):
#             if len(results.multi_hand_landmarks) == 2:
#               print(f"{j}: {results.multi_hand_landmarks[0].landmark[j]} \n TWO : {results.multi_hand_landmarks[1].landmark[j]}")
#               left = results.multi_hand_landmarks[0]
#               print(f"first{math.dist([left.landmark[9].x, left.landmark[9].y],[left.landmark[10].x, left.landmark[10].y])}")
#               print(f"second{math.dist([left.landmark[10].x, left.landmark[10].y],[left.landmark[12].x, left.landmark[12].y])}")
#               if (math.dist([left.landmark[9].x, left.landmark[9].y],[left.landmark[10].x, left.landmark[10].y]) > math.dist([left.landmark[10].x, left.landmark[10].y],[left.landmark[12].x, left.landmark[12].y])):
#                 cv2.putText(img, f'Great job!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
#               else:
#                 cv2.putText(img, f'Bend your left finger!', (200, 200), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 3)
#               if checkHand(results.multi_hand_landmarks):
#                 started = True;
#               if started:
#                 checkProperTechnique(results.multi_hand_landmarks)
#             else:
#               cv2.putText(img, f'Please keep both hands in frame!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
#               print(f"{j}: {results.multi_hand_landmarks[0].landmark[j]}")
#             if not picture:
#                 yield(mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS))
#           # for j in range(21):
#           #   print(f"{j}: {results.multi_hand_landmarks[0].landmark[j].x}")
#           # i +=1
#           for handLms in results.multi_hand_landmarks:
#             mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
#         ret,buffer=cv2.imencode('.jpg',img)
#         img=buffer.tobytes()
#       if picture :
#           yield(b'--frame\r\n'
#                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

# def checkHand(hand):
#   return (hand[0].landmark[20].x > hand[0].landmark[4].x > hand[1].landmark[4].x > hand[1].landmark[20].x) or (hand[0].landmark[20].x < hand[0].landmark[4].x < hand[1].landmark[4].x < hand[1].landmark[20].x)

# def checkProperTechnique(hand):
#   return True

# @app.route('/')
# def index():
#     return render_template('home.html')

# @app.route('/video')
# def video():
#     return Response(generate_frames(True),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/text')
# def text():
#     return Response(generate_frames(False),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/tes')
# def tes():
#   is_working = True
#   dev_port = 0
#   working_ports = []
#   available_ports = []
#   while is_working:
#       camera = cv2.VideoCapture(dev_port)
#       if not camera.isOpened():
#           is_working = False
#           print("Port %s is not working." %dev_port)
#       else:
#           is_reading, img = camera.read()
#           w = camera.get(3)
#           h = camera.get(4)
#           if is_reading:
#               print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
#               working_ports.append(dev_port)
#           else:
#               print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
#               available_ports.append(dev_port)
#       dev_port +=1
#   print(available_ports)
#   return "asdf"

# @app.route('/demo')
# def demo():
#     return Response(chinese_calligraphy_demo.generate_frames(True),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/input')
# def user_input():
#     return Response(parse_inputted_video.parse_frames('chinese-calligraphy-demo.mp4'),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/faces')
# def face():
#     return Response(faces.parse_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__=="__main__":
#     app.run(host='0.0.0.0', port=8080, debug=True)
from flask import Flask,render_template,Response
import cv2
import mediapipe as mp
app = Flask(__name__)
import math
import os
import chinese_calligraphy_demo
import parse_inputted_video
import faces

global started
started = False
app=Flask(__name__)
cap=cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_drawing_styles = mp.solutions.drawing_styles
holistic =  mp_holistic.Holistic()
folderPath = "Images"
image = os.listdir(folderPath)
pic = cv2.imread(f'{folderPath}/hands.png')
grat = cv2.imread(f'{folderPath}/grats.png')

def generate_frames2(picture):
  cap = cv2.VideoCapture(0)
  i = 500
  with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
    while True:
      success, img = cap.read()
      if not success:
          break
      else:
        results = holistic.process(img)
        if results.pose_landmarks:

          # To improve performance, optionally mark the image as not writeable to
          # pass by reference.
          img.flags.writeable = False
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          if(i < 0):
            scale_percent = 200 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            congrats = cv2.resize(grat, dim, interpolation = cv2.INTER_AREA)
            img = congrats
          # print (results.pose_landmarks.landmark[16].y - results.pose_landmarks.landmark[15].y)
          elif (results.pose_landmarks.landmark[16].visibility < 0.8 or (results.pose_landmarks.landmark[15].visibility < 0.8 )):
            cv2.putText(img, f'Please put your arms in the frame!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
          else:
            val = (results.pose_landmarks.landmark[16].y - results.pose_landmarks.landmark[15].y);
            if val > 0.2:
              cv2.putText(img, f'Left too high!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
              i = 500
            elif val < -0.2:
              cv2.putText(img, f'Right too high!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
              i = 500
            else:
              cv2.putText(img, f'Good!! Hold for {round(i/50)} seconds', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
              i -= 3;
          # if results.pose_landmarks.landmark[16] and results.pose_landlandmarks.landmark[15]:
          #   print (abs(results.pose_landmarks.landmark[16] - results.pose_landlandmarks.landmark[15]))
          # Draw landmark annotation on the image.
          img.flags.writeable = True
          img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
          mpDraw.draw_landmarks(
            img,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
          mpDraw.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
          ret,buffer=cv2.imencode('.jpg',img)
          img=buffer.tobytes()
          yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
    # Flip the image horizontally for a selfie-view display.


def generate_frames(picture):
  started = False
  i = 250
  while True:
      ## read the camera frame
      success,img=cap.read()
      if not success:
          break
      else:
        if not started:
          cv2.putText(img, f'Please put your hands flat on the table!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if (i <= 0):
          # cv2.imshow(img, grat)
          scale_percent = 200 # percent of original size
          width = int(img.shape[1] * scale_percent / 100)
          height = int(img.shape[0] * scale_percent / 100)
          dim = (width, height)

          # resize image
          congrats = cv2.resize(grat, dim, interpolation = cv2.INTER_AREA)
          img = congrats

        if results.multi_hand_landmarks and i > 0:
          for j in range(10,13):
            if len(results.multi_hand_landmarks) == 2:
              # print(f"{j}: {results.multi_hand_landmarks[0].landmark[j]} \n TWO : {results.multi_hand_landmarks[1].landmark[j]}")
              left = results.multi_hand_landmarks[0]
              # print(f"first{math.dist([left.landmark[9].x, left.landmark[9].y],[left.landmark[10].x, left.landmark[10].y])}")
              # print(f"second{math.dist([left.landmark[10].x, left.landmark[10].y],[left.landmark[12].x, left.landmark[12].y])}")
              if ((math.dist([left.landmark[9].x, left.landmark[9].y],[left.landmark[10].x, left.landmark[10].y]) > math.dist([left.landmark[10].x, left.landmark[10].y],[left.landmark[12].x, left.landmark[12].y])) and started):
                cv2.putText(img, f'Great job! Continue for {round(i/50)} more seconds', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                if i >= 0:
                  i -= 1;
              else:
                if i > 0:
                  i = 250;
                if started:
                  cv2.putText(img, f'Bend your left finger!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
              if checkHand(results.multi_hand_landmarks):
                started = True;
              if started:
                checkProperTechnique(results.multi_hand_landmarks)
            else:
              if started:
                cv2.putText(img, f'Please keep both hands in frame!', (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
              # print(f"{j}: {results.multi_hand_landmarks[0].landmark[j]}")
            # if not picture:
            #     yield(mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS))
          for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        ret,buffer=cv2.imencode('.jpg',img)
        img=buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

def checkHand(hand):
  return (hand[0].landmark[20].x > hand[0].landmark[4].x > hand[1].landmark[4].x > hand[1].landmark[20].x) or (hand[0].landmark[20].x < hand[0].landmark[4].x < hand[1].landmark[4].x < hand[1].landmark[20].x)

def checkProperTechnique(hand):
  return True


@app.route('/yoga2')
def yoga2():
    return Response(generate_frames2(True),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/yoga-class.html')
def index234234():
  return render_template('yoga-class.html')

@app.route('/home.html')
def index5():
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

@app.route('/classes.html')
def classes():
  return render_template('classes.html')

@app.route('/cooking-class.html')
def classes2():
  return render_template('cooking-class.html')

@app.route('/asl-class.html')
def classes3():
  return render_template('asl-class.html')



if __name__=="__main__":
    app.debug = True
    app.run()
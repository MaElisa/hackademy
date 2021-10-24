# run with         python3 -m flask run
from flask import Flask,render_template,Response
import mediapipe as mp
import cv2

app = Flask(__name__)

def parse_frames():
    print("entered 1")
    mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        # refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    # cap = cv2.VideoCapture("C:\\Users\\elisa\\OneDrive\\Pictures\\Camera Roll\\2021\\07\\20210704_033756000_iOS.mp4")
    cap = cv2.VideoCapture('chinese-calligraphy-demo.mp4')
    while True:
        print("entered 2")
        success, image = cap.read()
        if not success:
            print("Not success")
            # If loading a video, use 'break' instead of 'continue'.
            break

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None)
                    # ,connection_drawing_spec=mp_drawing_styles
                    # .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None)
                    # ,connection_drawing_spec=mp_drawing_styles
                    # .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None)
                    # , connection_drawing_spec=mp_drawing_styles
                    # .get_default_face_mesh_iris_connections_style())
        ret, buffer = cv2.imencode('.jpg',image)
        image = buffer.tobytes()
        yield(b'--image\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
            # Flip the image horizontally for a selfie-view display.
            # cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break
    cap.release()

if __name__=="__main__":
    app.run(debug=True)

    
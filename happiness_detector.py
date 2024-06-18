import cv2
from deepface import DeepFace
import base64
import numpy as np
from models import flask_app, Reaction, db, Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def analyze_image(image_data):
    img_data = base64.b64decode(image_data.split(',')[1])
    nparr = np.fromstring(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
        face_roi = rgb_frame[y:y + h, x:x + w]

        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']

        reaction_value = 1 if dominant_emotion == 'happy' else 0

        return {"dominant_emotion": dominant_emotion, "reaction_value": reaction_value}
    else:
        return {"dominant_emotion": None, "reaction_value": 0}

import cv2
from deepface import DeepFace
import base64
import numpy as np
from models import flask_app, Reaction, db, Image
from flask import Flask, request, jsonify

# Inspired by https://github.com/manish-9245/Facial-Emotion-Recognition-using-OpenCV-and-Deepface

# Face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def analyze_image(image_data, user_id, current_image_index):
    img_data = base64.b64decode(image_data.split(',')[1])
    nparr = np.fromstring(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    reaction_value = 0

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale to RGB
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Select the largest face detected
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = largest_face
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Analyze the dominant emotion in the detected face
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']



        # Determine reaction_value based on emotion detected
        if dominant_emotion == 'happy':
            reaction_value = 1

        # Get image filename and extract the image_id
        image_id = current_image_index

        # Store the reaction in the database
        with flask_app.app_context():
            reaction = Reaction(user_id=user_id, image_id=image_id, reaction_value=reaction_value)
            db.session.add(reaction)
            db.session.commit()

        return {"dominant_emotion": dominant_emotion, "reaction_value": reaction_value}

    else:
        return {"error": "No face detected"}


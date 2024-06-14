import cv2
from deepface import DeepFace
import time
from models import flask_app, Reaction, db, Image
from flask import Flask

#  Inspired by https://github.com/manish-9245/Facial-Emotion-Recognition-using-OpenCV-and-Deepface

# Face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def handle_reactions(user_id, image_list):
    # Start video capture
    cap = cv2.VideoCapture(0)
    current_image_index = 0
    start_time = time.time()

    with flask_app.app_context():
        while current_image_index < len(image_list):
            # Capture each frame
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convert grayscale to RGB
            rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

            # Detect dominat face and emotion in the frame
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            largest_face = max(faces, key=lambda face: face[2] * face[3])
            x, y, w, h = largest_face
            face_roi = rgb_frame[y:y + h, x:x + w]
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            dominant_emotion = result[0]['dominant_emotion']

            # Check if the dominant emotion is 'happy' or not
            if dominant_emotion == 'happy':
                reaction_value = 1
            else:
                reaction_value = 0

            # Draw rectangle around the face and label with the emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"{dominant_emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Store the reaction in the database


            # Add text "image_i" on the frame
            cv2.putText(frame, f"image_{current_image_index + 1}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Display the resulting frame
            cv2.imshow('Real-time Emotion Detection', frame)

            # Check if 3 seconds have passed
            if time.time() - start_time > 2 or reaction_value == 1 :
                image_path = image_list[current_image_index]
                image = Image.query.filter_by(image_path=image_path).first()
                reaction = Reaction(user_id=user_id, image_id=image.id, reaction_value=reaction_value)
                db.session.add(reaction)
                    # Commit the reactions to the database
                db.session.commit()
                start_time = time.time()
                current_image_index += 1
                

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


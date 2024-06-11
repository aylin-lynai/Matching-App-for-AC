import cv2
from deepface import DeepFace
import time
import random
from models import flask_app, Reaction, db, Image

# Face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def handle_reactions(user_id, image_list):
    cap = cv2.VideoCapture(0)
    image_index = 0

    while image_index < len(image_list):
        image_id = image_list[image_index]
        start_time = time.time()
        happy_detected = False

        while time.time() - start_time < 3:
            # Capture each frame
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convert grayscale to RGB
            rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Extract the face ROI (Region of Interest)
                face_roi = rgb_frame[y:y + h, x:x + w]

                # Perform emotion analysis on the face ROI
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

                # Determine the dominant emotion
                dominant_emotion = result[0]['dominant_emotion']

                # Check if the dominant emotion is 'happy' or not
                if dominant_emotion == 'happy':
                    happy_detected = True
                    break

            if happy_detected:
                break

            # Press 'q' to exit manually (optional)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        # Store the reaction in the database
        with flask_app.app_context():
            reaction_value = 1 if happy_detected else 0
            reaction = Reaction(user_id=user_id, image_id=image_id, reaction_value=reaction_value)
            db.session.add(reaction)

        image_index += 1

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()



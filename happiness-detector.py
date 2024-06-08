import cv2
from deepface import DeepFace

# inspired by https://github.com/manish-9245/Facial-Emotion-Recognition-using-OpenCV-and-Deepface

# Face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video
cap = cv2.VideoCapture(0)

while True:
    # Capture each frame
    ret, frame = cap.read()

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
            emotion_label = 'happy'
        else:
            emotion_label = 'not happy'
 # TODO store emotion in database!!
 
        # Draw rectangle around the face and label with the emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        #TODO remove that in the frontend!!
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

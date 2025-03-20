import cv2
import numpy as np
from deepface import DeepFace
from threading import Thread

# Load the webcam
cap = cv2.VideoCapture(0)

# Function to recognize faces asynchronously
def recognize_faces(frame, faces):
    for face in faces:
        try:
            # Extract face ROI
            x, y, w, h = face['x'], face['y'], face['w'], face['h']
            face_img = frame[y:y+h, x:x+w]

            # Recognize face using FaceNet
            result = DeepFace.find(face_img, db_path="face_db", model_name="Facenet", detector_backend="retinaface", enforce_detection=False)

            # Get the recognized person's name
            if len(result) > 0 and not result[0].empty:
                identity = result[0]['identity'][0].split("/")[-1].split(".")[0]
                cv2.putText(frame, identity, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        except Exception as e:
            print(f"Error in recognition: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect multiple faces using RetinaFace
    faces = DeepFace.detectFace(frame, detector_backend='retinaface', enforce_detection=False)

    # Draw bounding boxes for detected faces
    for face in faces:
        x, y, w, h = face['x'], face['y'], face['w'], face['h']
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Run recognition in a separate thread for speed optimization
    recognition_thread = Thread(target=recognize_faces, args=(frame, faces))
    recognition_thread.start()

    cv2.imshow("Face Detection & Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

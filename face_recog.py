import cv2
import os
from arcface_recog import ArcFaceRecognizer

arcface = ArcFaceRecognizer()

def detect_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "Image could not be loaded.", ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return "No faces detected.", ""

    annotated_faces = []
    for i, (x, y, w, h) in enumerate(faces):
        face = img[y:y+h, x:x+w]
        embedding = arcface.get_embedding(face)
        annotated_faces.append((embedding, (x, y, w, h)))

    for i, (embedding, (x, y, w, h)) in enumerate(annotated_faces):
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(img, f"Face {i+1}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    output_path = os.path.splitext(image_path)[0] + "_output.jpg"
    cv2.imwrite(output_path, img)

    return f"{len(faces)} face(s) detected.", output_path

def safe_camera_test():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Camera is in use or unavailable."
        cap.release()
        return True, "Camera is available."
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    status, msg = safe_camera_test()
    print(msg)
    if status:
        result, output = detect_face("test.jpg")
        print(result)

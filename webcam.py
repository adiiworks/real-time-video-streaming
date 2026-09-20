import cv2
import time  # FPS calculate karne ke liye
from ultralytics import YOLO

# Models load kiye
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = YOLO("yolov8n.pt")

cam = cv2.VideoCapture(0)
photo_count = 0
prev_time = 0  # Purana time store karne ke liye (for FPS)

print("Polished AI Webcam Active hai!")

while True:
    ret, frame = cam.read()
    if not ret:
        break
        
    # --- FPS CALCULATION START ---
    current_time = time.time()
    # FPS = 1 / (current_time - previous_time)
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    # --- FPS CALCULATION END ---

    # AI Object Detection
    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()
    
    # Face Detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(annotated_frame, "Aditya", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Camera Tampering Detection
    avg_color = cv2.mean(frame)
    overall_average = (avg_color[0] + avg_color[1] + avg_color[2]) / 3
    
    if overall_average < 30:
        cv2.putText(annotated_frame, "WARNING: CAMERA TAMPERED!", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # --- SCREEN PAR FPS DISPLAY KARNA ---
    # Top-right corner ke paas FPS text print karenge cyan color me
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow('My AI & Face Webcam', annotated_frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        file_name = f'captured_photo_{photo_count}.jpg'
        cv2.imwrite(file_name, annotated_frame)
        print(f"Photo save ho gayi: {file_name}")
        photo_count += 1
    elif key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
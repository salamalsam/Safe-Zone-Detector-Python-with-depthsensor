import cv2
from distance_utils import calculate_focal_length, calculate_distance
from playsound import playsound
from machine_utils import Machine
import os
import time

# Known dimensions
KNOWN_DISTANCE = 35.0  # cm (distance at which focal length is calibrated)
KNOWN_WIDTH = 5.0      # cm (width of a reference object)

# Zone thresholds
DANGER_ZONE = 25.0  # cm
WARNING_ZONE = 50.0  # cm

# Initialize the machine
machine = Machine()

# Directories for saving images
os.makedirs("danger_zone", exist_ok=True)
os.makedirs("warning_zone", exist_ok=True)

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set frame height

# Load a pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize focal length
focal_length = None

# Focal length calibration
print("Place the reference object at", KNOWN_DISTANCE, "cm from the camera for calibration.")
while focal_length is None:
    ret, frame = cap.read()
    if not ret:
        continue

    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:  # Check if any face is detected
        x, y, w, h = faces[0]
        focal_length = calculate_focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, w)
        machine.turn_fast()
        print("Focal length calibrated:", focal_length)
    else:
        machine.turn_slow()
        print("No faces detected. Adjust lighting or camera angle.")

print("Focal length initialized. Starting real-time object detection...")

# Track last capture time
last_capture_time = time.time()

# Measure distance to detected objects in real-time
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Calculate distance
        distance = calculate_distance(focal_length, KNOWN_WIDTH, w)

        # Determine zone
        current_time = time.time()
        if distance <= DANGER_ZONE:
            zone_color = (0, 0, 255)  # Red for danger zone
            alert = "Danger"
            save_dir = "danger_zone"
            machine.turn_off()
            #playsound("siren.mp3", block=False)  # Uncomment and provide correct path
        elif distance <= WARNING_ZONE:
            zone_color = (0, 255, 255)  # Yellow for warning zone
            alert = "Warning"
            save_dir = "warning_zone"
            machine.turn_on()
            machine.turn_slow()
            #playsound("beep.mp3", block=False)  # Uncomment and provide correct path
        else:
            zone_color = (0, 255, 0)  # Green for safe zone
            alert = "Safe"
            machine.turn_fast()
            save_dir = None

        # Draw a rectangle around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), zone_color, 2)

        # Display distance and zone status
        cv2.putText(frame, f"{distance:.2f} cm - {alert}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, zone_color, 2)

        # Capture and save images if in danger or warning zone every 5 seconds
        if save_dir and (current_time - last_capture_time >= 5):
            filename = f"{save_dir}/{alert}_{int(current_time)}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captured and saved: {filename}")
            last_capture_time = current_time

    # Show the frame
    cv2.imshow("Object Detection with Zones", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

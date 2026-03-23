import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# import pigpio

# -----------------------------
# HAND CONNECTIONS (manual)
# -----------------------------
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

# -----------------------------
# MediaPipe Setup
# -----------------------------
BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions

model_path = "hand_landmarker.task"  # make sure this file exists

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    num_hands=2
)

hand_landmarker = HandLandmarker.create_from_options(options)

# -----------------------------
# SERVO (COMMENTED - FOR PI)
# -----------------------------
# pi = pigpio.pi()
# servo_pins = [17,18,27,22,23,24,25,4,5,6,12,13,16,20,21]

# def move_servo(pin, angle):
#     pulse_width = int((angle / 180) * 2000 + 500)
#     pi.set_servo_pulsewidth(pin, pulse_width)

# -----------------------------
# HAND → SERVO LOGIC
# -----------------------------
def control_robotic_hand(hand_landmarks):
    """
    Tracks all 5 fingers and converts them into angles (0–180)
    """

    finger_tips = [4, 8, 12, 16, 20]
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

    angles = []

    for i, tip in enumerate(finger_tips):
        landmark = hand_landmarks[tip]

        # Use Y-axis (better for open/close detection)
        angle = int((1 - landmark.y) * 180)
        angle = max(0, min(180, angle))

        angles.append(angle)

        print(f"{finger_names[i]}: {angle}")

        # Example for servo control (Raspberry Pi)
        # move_servo(servo_pins[i], angle)

    print("----------------------")


# -----------------------------
# WEBCAM START
# -----------------------------
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Detect hands
    result = hand_landmarker.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:

            control_robotic_hand(hand_landmarks)

            h, w, _ = frame.shape

            # Draw landmarks
            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Draw connections
            for start_idx, end_idx in HAND_CONNECTIONS:
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]

                cv2.line(
                    frame,
                    (int(start.x * w), int(start.y * h)),
                    (int(end.x * w), int(end.y * h)),
                    (255, 0, 0),
                    2
                )

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# -----------------------------
# CLEANUP (FOR PI)
# -----------------------------
# pi.stop()
import cv2
import mediapipe as mp
import pigpio
import time

# Initialize the PiGPIO library
pi = pigpio.pi()

if not pi.connected:
    print("Not connected to pigpio daemon")
    exit()

# Define the GPIO pins for the servos
servo_pins = [17, 18, 27, 22, 23, 24, 25, 4, 5, 6, 12, 13, 16, 20, 21]  # example GPIO pins for 15 servos

# Set up the servos on the corresponding GPIO pins
for pin in servo_pins:
    pi.set_mode(pin, pigpio.OUTPUT)

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Function to move servo
def move_servo(pin, angle):
    # Map angle (0 to 180 degrees) to pulse width (500 to 2500 microseconds)
    pulse_width = int((angle / 180) * (2500 - 500) + 500)
    pi.set_servo_pulsewidth(pin, pulse_width)

# Function to control the hand based on detected gestures
def control_robotic_hand(hand_landmarks):
    # Extract relevant landmarks for finger movements
    if hand_landmarks:
        # Example: Mapping landmarks to servo control
        thumb_finger_angle = hand_landmarks[0]  # Adjust based on the thumb position
        index_finger_angle = hand_landmarks[1]  # Adjust based on the index finger position
        
        # Here, you would implement the logic to extract angles from the landmarks
        # and map them to your servo control. This is a simplified placeholder.
        
        # For instance:
        move_servo(servo_pins[0], thumb_finger_angle)   # Thumb opening/closing
        move_servo(servo_pins[1], index_finger_angle)   # Index finger movement
        # Add more logic for other servos/fingers here

# Start the webcam feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = hands.process(rgb_frame)

    # Draw the hand landmarks and process gesture data
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Control the robotic hand based on detected landmarks
            control_robotic_hand(hand_landmarks.landmark)
            
            # Visualize the hand landmarks
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

# Clean up and stop servos
pi.stop()
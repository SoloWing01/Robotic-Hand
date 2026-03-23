# 🖐️ Robotic Hand (Hand Tracking + Servo Control)

This project uses **computer vision (MediaPipe)** to track real-time hand movements from a webcam and control a **robotic hand with 15 servos** using a Raspberry Pi.

---

## 🎥 Demo

Check out the working demo of the project:

👉 https://youtube.com/shorts/CTu5sQrJ89M

---

## 🧰 Hardware Used

* Raspberry Pi 4 Model B (8GB RAM)
* Raspberry Pi Camera Module
* 15x Servo Motors
* External 5V–6V Power Supply
* Connecting Wires

---

## 🚀 Features

* Real-time **hand tracking using MediaPipe**
* Maps **finger movements → servo angles**
* Supports up to **15 servo motors**
* Works with:

  * 🖥️ PC (for testing vision)
  * 🤖 Raspberry Pi (for controlling hardware)

---

## 🧠 How It Works

```
Webcam → MediaPipe → Landmark Detection → Angle Mapping → Servo Movement
```

* Camera captures your hand
* MediaPipe detects finger positions
* Positions are converted into angles
* Angles control servo motors via GPIO (pigpio)

---

## 📦 Requirements

```
opencv-python==4.9.0.80
mediapipe>=0.10.13
pigpio==1.78
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/roboticHand.git
cd roboticHand
```

---

### 2. Use Compatible Python Version

⚠️ MediaPipe works best with:

* Python ≤ 3.10
* OR use **pyenv** to manage multiple Python versions

---

### 3. (Optional) Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Run the Project

```bash
python arm.py
```

---

## 🖥️ Running on PC (Testing Only)

If you're testing on a PC:

* Comment out pigpio-related lines:

```python
# import pigpio
# pi = pigpio.pi()
```

Use only:

```
opencv-python
mediapipe
```

---

## 🤖 Running on Raspberry Pi (Full System)

### Start pigpio daemon:

```bash
sudo systemctl start pigpiod
```

### Wiring:

* Servo VCC → External 5V/6V supply
* Servo GND → Common GND (Pi + PSU)
* Servo Signal → GPIO pins

⚠️ Do NOT power servos from Raspberry Pi

---

## ⚠️ Known Issues

* Jitter with many servos (GPIO limitation)
* MediaPipe compatibility depends on Python version
* Requires good lighting for accurate tracking

---

## 🔥 Future Improvements

* Smooth servo movement (reduce jitter)
* Better finger angle calculation
* Gesture recognition (fist, open, pinch)
* Wireless control (LoRa / WiFi)

---

## 📁 Project Structure

```
roboticHand/
│── arm.py
│── requirements.txt
```

---

## 🙌 Contribution

Feel free to improve:

* Accuracy
* Performance
* Hardware integration

---

## 📌 Notes

This project is ideal for:

* Robotics beginners
* Hardware + vision integration
* Real-time control systems

---

## 💡 Author

Built for learning and experimentation in robotics systems 🚀

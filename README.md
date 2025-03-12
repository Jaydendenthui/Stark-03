# Stark-03
This AI-powered voice assistant integrates speech recognition, computer vision, and hand gesture control to perform various tasks, including opening websites, reading text, detecting objects, and retrieving calendar events.

🚀 Features
🎙️ Voice Interaction – Uses speech recognition to listen and respond.
📅 Google Calendar Integration – Retrieves daily events and schedules.
🌐 Smart Web Navigation – Opens websites based on voice commands.
📷 Object Detection – Detects objects in real-time using YOLOv5.
🔠 Text Recognition – Reads text from images using EasyOCR.
✋ Hand Gesture Control – Uses MediaPipe to recognize hand gestures for seamless interaction.
🛠️ Technologies Used
Python
Pyttsx3 (Text-to-Speech)
SpeechRecognition
OpenCV (Computer Vision)
YOLOv5 (Object Detection)
EasyOCR (Text Recognition)
Google Calendar API
MediaPipe (Hand Tracking)
📌 How It Works
The assistant greets the user and fetches daily events.
Using speech commands, you can ask it to open websites.
Using hand gestures, you can:
🖐️ Raise 1 finger to open a website (based on voice input).
✌️ Raise 2 fingers to start object detection.
🤟 Raise 3 fingers to read text from an image.
✋ Raise 5 fingers to reset actions.
📷 Demo

📦 Installation
Clone the repository

git clone https://github.com/your-username/ai-voice-assistant.git
cd ai-voice-assistant
Install dependencies:

pip install -r requirements.txt
Run the assistant:

python main.py
🔥 Future Improvements
Implementing NLP for better conversation handling.
Adding face recognition for personalized interactions.
Improving response speed and optimization for real-time processing.

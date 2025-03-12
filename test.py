import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import pyttsx3
import datetime
import time
import webbrowser
import cv2
import torch
import numpy as np
import requests
import easyocr
from googleapiclient.discovery import build
from google.oauth2 import service_account
import mediapipe as mp
import speech_recognition as sr

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', min(volume+0.25, 1.0))
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Which website would you like to open?")
        print("Listening for website name...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            speak("Could not request results. Please check your internet connection.")
            return None

def wishMe():
    hour = datetime.datetime.now().hour
    t = time.strftime("%I:%M %p")
    day = cal_day()
    speak(f"Sup Jayden, it's {day} and the time is {t}. Here's everything that happened today:")
    get_appointments()

def cal_day():
    day_dict = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    return day_dict.get(datetime.datetime.today().weekday(), "Unknown Day")
def get_appointments():
    try:
        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
        SERVICE_ACCOUNT_FILE = "credentials.json"
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=credentials)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        end_of_day = (datetime.datetime.utcnow().replace(hour=23, minute=59, second=59)).isoformat() + "Z"
        events_result = service.events().list(
            calendarId="primary", timeMin=now, timeMax=end_of_day, maxResults=50,
            singleEvents=True, orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        if not events:
            print("You had no events scheduled for today.")
        else:
            print("Here is what happened today:")
            for event in events:
                event_summary = event.get("summary", "No Title")
                start = event["start"].get("dateTime", event["start"].get("date"))
                if "T" in start:
                    start_time = datetime.datetime.fromisoformat(start[:-1]).strftime("%I:%M %p")
                else:
                    start_time = start
                print(f"{event_summary} at {start_time}")
    except Exception as e:
        print(f"I couldn't retrieve your calendar events. Error: {e}")
    
def open_website(command):
    if command is None:
        return
    website_dict = {
        "facebook": "facebook.com",
        "instagram": "instagram.com",
        "twitter": "twitter.com",
        "youtube": "youtube.com",
        "google": "google.com",
        "reddit": "reddit.com",
        "github": "github.com",
        "school": "calendar.google.com"
    }
    words = command.lower().split()
    for word in words:
        if word in website_dict:
            url = f"https://{website_dict[word]}"
            print(f"Opening {word}")
            webbrowser.open(url)
            return
        elif any(ext in word for ext in [".com", ".org", ".net", ".io"]):
            url = f"https://{word}" if not word.startswith("http") else word
            print(f"Opening {word}")
            webbrowser.open(url)
            return
    print("Please specify a valid website.")

def detect_objects():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        detected_objects = results.pandas().xyxy[0]['name'].unique()
        if len(detected_objects) > 0:
            speak(f"I see {', '.join(detected_objects)}")
        cv2.imshow('YOLOv5 Object Detection', np.squeeze(results.render()))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def read_text():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using EasyOCR on: {device}")
    reader = easyocr.Reader(['en'], gpu=(device == 'cuda'))  # Use GPU if available
    
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = reader.readtext(frame)
        for _, text, _ in results:
            print(f"Detected Text: {text}")
        
        cv2.imshow('Text Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def count_fingers():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture(0)
    action_performed = False
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks and not action_performed:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_tips = [4, 8, 12, 16, 20]
                finger_count = sum(
                    hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y
                    for i in finger_tips
                )
                print(f"Fingers up: {finger_count}")
                if finger_count == 1:
                    command = listen()
                    open_website(command)
                    action_performed = True
                elif finger_count == 2:
                    detect_objects()
                    action_performed = True
                elif finger_count == 3:
                    read_text()
                    action_performed = True
                elif finger_count == 5:
                    action_performed = False
        cv2.imshow('Finger Counting', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    wishMe()
    count_fingers()

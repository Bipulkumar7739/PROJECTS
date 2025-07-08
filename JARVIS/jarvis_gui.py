import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit
import tkinter as tk
from tkinter import messagebox

# Initialize voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 17:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def playMusic():
    music_dir = "music"
    songs = os.listdir(music_dir)
    if songs:
        os.startfile(os.path.join(music_dir, songs[0]))
        speak("Playing music")
    else:
        speak("No songs found in the music folder")

def openYouTube():
    webbrowser.open("https://www.youtube.com")
    speak("Opening YouTube")

def openGoogle():
    webbrowser.open("https://www.google.com")
    speak("Opening Google")

def openWhatsapp():
    webbrowser.open("https://web.whatsapp.com")
    speak("Opening WhatsApp Web")

def tellTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

def tellDate():
    today = datetime.date.today()
    speak(f"Today's date is {today.strftime('%B %d, %Y')}")

def searchWiki():
    speak("What should I search on Wikipedia?")
    query = takeCommand()
    if query != "None":
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)

def startListening():
    speak("Listening now...")
    query = takeCommand()

    if 'youtube' in query:
        openYouTube()
    elif 'google' in query:
        openGoogle()
    elif 'whatsapp' in query:
        openWhatsapp()
    elif 'play music' in query:
        playMusic()
    elif 'time' in query:
        tellTime()
    elif 'date' in query:
        tellDate()
    elif 'wikipedia' in query:
        searchWiki()
    elif 'exit' in query or 'close' in query:
        speak("Goodbye, take care!")
        root.destroy()
    else:
        speak("Sorry, I didn't understand. Please try again.")

# GUI Setup
root = tk.Tk()
root.title("Jarvis AI Assistant")
root.geometry("500x500")
root.configure(bg="#1a1a1a")

title = tk.Label(root, text="Jarvis AI Assistant", font=("Helvetica", 20, "bold"), fg="cyan", bg="#1a1a1a")
title.pack(pady=20)

btn_listen = tk.Button(root, text="🎙️ Speak Command", font=("Helvetica", 16), bg="green", fg="white", command=startListening)
btn_listen.pack(pady=20)

btn_music = tk.Button(root, text="🎵 Play Music", font=("Helvetica", 16), bg="blue", fg="white", command=playMusic)
btn_music.pack(pady=10)

btn_youtube = tk.Button(root, text="▶️ Open YouTube", font=("Helvetica", 16), bg="red", fg="white", command=openYouTube)
btn_youtube.pack(pady=10)

btn_whatsapp = tk.Button(root, text="💬 Open WhatsApp", font=("Helvetica", 16), bg="darkgreen", fg="white", command=openWhatsapp)
btn_whatsapp.pack(pady=10)

btn_exit = tk.Button(root, text="❌ Exit", font=("Helvetica", 16), bg="gray", fg="white", command=root.destroy)
btn_exit.pack(pady=30)

wishMe()

root.mainloop()
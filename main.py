import speech_recognition as sr # Used for speech-to-text conversion.

import webbrowser # Used to open URLs in a web browser.
import pyttsx3 # Used for text-to-speech conversion... # Works offline and allows control over speech speed and volume.
import requests # Used to send HTTP requests (GET, POST, etc.) to APIs and websites.  # Fetch data from an API.
import openai # Used to interact with OpenAI APIs (like ChatGPT, geminia) , Requires an API key for access.
from gtts import gTTS #gTTS (Google Text-to-Speech) is a Python library used for converting text to speech using Google's TTS API. 
                      # It generates natural-sounding speech and supports multiple languages and accents.
import pygame # pygame is a Python library used for game development and multimedia applications.
              # It provides functions for graphics, sound, input handling, and event management.
import os
from musicLibrary import musicLibrary  # Import the musicLibrary dictionary

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Your NewsAPI key
newsapi = "OPENAI_API_KEY" # news api key

# OpenAI API key
openai.api_key = "OPENAI_API_KEY" # openai api key


# Speak Function with Pygame
def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()  # Initialize Pygame mixer
    pygame.mixer.music.load("temp.mp3")  # Load the MP3 file
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # Keep running while music is playing
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


# AI Processing Function
def aiprocess(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses, please."},
                {"role": "user", "content": command}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error interacting with AI: {e}"


# Command Processing Function
def processCommand(c):
    c = c.lower().strip()  # Normalize and clean the command
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open github" in c:
        webbrowser.open("https://github.com")
    elif "open nextwave" in c:
        webbrowser.open("https://learning.ccbp.in/")
    elif c.startswith("play"):
        # Extract song name and play it
        song = c.split(" ", 1)[1]
        if song in musicLibrary:
            link = musicLibrary[song]
            webbrowser.open(link)
            speak(f"Playing {song} for you.")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                for article in articles[:5]:  # Limit to 5 articles for brevity
                    speak(article['title'])
            else:
                speak("No news articles found.")
        else:
            speak("Error fetching news.")
    else:
        output = aiprocess(c)
        speak(output)


# Main Function
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        recognizer = sr.Recognizer()
        print("Recognizing...")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusting for ambient noise
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio, language="en-IN")  # Set the language
                print(f"Recognized: {word}")

                if word.lower() == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)
                        command = recognizer.recognize_google(audio, language="en-IN")
                        print(f"Command: {command}")
                        processCommand(command)

            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand that. Please try again.")
            except sr.RequestError as e:
                speak(f"Speech service error: {e}")
            except Exception as e:
                speak(f"An error occurred: {e}")

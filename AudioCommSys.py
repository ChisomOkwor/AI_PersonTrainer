import speech_recognition as sr

from gtts import gTTS
import os
from io import BytesIO
from playsound import playsound

language = 'en'

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Please say something....")
        audio = recognizer.listen(source, timeout=2)
        try:
            print("You said: \n" + recognizer.recognize_google(audio))
            return (recognizer.recognize_google(audio))
        except Exception as e:
            print("Error: " + str(e))

def text_to_speech(text):
    output = gTTS(text=text, lang=language, slow=False)
    output.save("output.mp3")
    playsound("output.mp3")

def main():  
    text_to_speech("Testing, Testing, Testing")

if __name__ == "__main__":
    main()

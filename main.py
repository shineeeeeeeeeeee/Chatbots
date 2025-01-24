import speech_recognition as sr
import os
import webbrowser
import openai
import datetime

def say(text):
    """Speak the given text using the system's text-to-speech."""
    os.system(f"say {text}")

def takeCommand(recognizer, source):
    """Listen to the user's command and return the recognized text."""
    print("Listening...")
    try:
        audio = recognizer.listen(source)
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble reaching the service.")
        return None

def playMusic(musicPath):
    """Play music from the given file path."""
    if os.path.exists(musicPath):
        if os.name == 'nt':  # Windows
            os.startfile(musicPath)
        elif os.name == 'posix':  # macOS or Linux
            os.system(f"open {musicPath}")  # macOS
            # For Linux, replace with: os.system(f"xdg-open {musicPath}")
    else:
        say("Music file not found!")

if __name__ == '__main__':
    print("Hello World")
    say("Hello, I am Jarvis A.I")

    recognizer = sr.Recognizer()

    # List of websites and their URLs
    sites = [
        ("youtube", "https://youtube.com"),
        ("google", "https://google.com"),
        ("github", "https://github.com")
    ]

    # Adjust for ambient noise once at the start
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Adjustment complete.")

        while True:
            text = takeCommand(recognizer, source)
            if text is None:
                continue  # Skip processing if no command is recognized

            # Check for specific commands
            found_site = False
            for site in sites:
                if f"open {site[0]}" in text.lower():
                    say(f"Opening {site[0]}, sir...")
                    webbrowser.open(site[1])
                    found_site = True
                    break  # Exit the loop once a match is found

            # Check for music command
            if "open music" in text.lower():
                musicPath = "songs/romantic.mp3"
                playMusic(musicPath)
                found_site = True

            if "the time" in text.lower():
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir, the time is {strfTime}")

            if "open facetime" in text.lower():
                os.system("open /System/Applications/FaceTime.app")
                say("Opening FaceTime, sir.")
                found_command = True

            # If no specific command matches
            if not found_site:
                if "exit" in text.lower() or "stop" in text.lower():
                    say("Goodbye, sir!")
                    break
                else:
                    say(f"You said: {text}")

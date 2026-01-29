import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import smtplib
import wikipedia

# ---------------- SPEAK (FEMALE VOICE) ----------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)

    voices = engine.getProperty('voices')
    # Try to select female voice safely
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    else:
        # fallback if female not detected
        engine.setProperty('voice', voices[1].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ---------------- WISH USER ----------------
def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning Jafar boss")
    elif hour < 18:
        speak("Good Afternoon Jafar boss")
    else:
        speak("Good Evening Jafar boss")
    speak("I am your smiley. How can I help you?")

# ---------------- TAKE COMMAND ----------------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print("User said:", query)
        return query.lower()
    except:
        speak("Sorry, I did not understand")
        return ""

# ---------------- EMAIL FUNCTION ----------------
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("yourEmail@gmail.com", "yourPassword")
    server.sendmail("yourEmail@gmail.com", to, content)
    server.quit()

# -------------- MAIN PROGRAM ------------
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        # -------- WIKIPEDIA --------
        if "wikipedia" in query:
            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)

        # -------- YOUTUBE SEARCH --------
        elif "search" in query and "youtube" in query:
            speak("What should I search on YouTube boss?")
            search_query = takeCommand()

            if search_query != "":
                speak(f"Searching {search_query} on YouTube")
                search_query = search_query.replace(" ", "+")
                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={search_query}"
                )

        # -------- OPEN YOUTUBE --------
        elif "open youtube" in query:
            speak("Opening YouTube boss")
            webbrowser.open("https://www.youtube.com")

        # -------- OPEN GOOGLE --------
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # -------- PLAY MUSIC --------
        elif "play music" in query:
            speak("Playing music")
            music_dir = "C:\\Users\\YourName\\Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        # -------- TIME --------
        elif "time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time}")

        # -------- OPEN VS CODE --------
        elif "open code" in query:
            speak("Opening Visual Studio Code")
            os.startfile(
                "C:\\Users\\YourName\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            )

        # -------- SEND EMAIL --------
        elif "send email" in query:
            speak("What should I say?")
            content = takeCommand()
            sendEmail("friend@example.com", content)
            speak("Email has been sent")

        # -------- EXIT --------
        elif "sleep" in query or "bye" in query:
            speak("Goodbye Jafar boss")
            break

        # -------- FALLBACK --------
        else:
            if query != "":
                speak("You said " + query)
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
from deep_translator import GoogleTranslator

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Female voice

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Speak text using TTS
def talk(text):
    engine.say(text)
    engine.runAndWait()
    result_label.config(text=text)

# Handle command (typed or spoken)
def process_command(command):
    command = command.lower().strip()

    # Play song
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)

    # Time request
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')

    # Info or Wikipedia queries
    elif any(keyword in command for keyword in ['who is', 'tell me about', 'what is', 'info']):
        for keyword in ['who is', 'tell me about', 'what is', 'info']:
            if keyword in command:
                topic = command.split(keyword, 1)[-1].strip()
                break
        try:
            info = wikipedia.summary(topic, 1)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"There are many results for {topic}. Try being more specific.")
        except wikipedia.exceptions.PageError:
            talk(f"Sorry, I couldn't find any info on {topic}.")
        except Exception as e:
            talk(f"Something went wrong while looking up {topic}.")

    # Joke
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    # Search web
    elif 'search' in command or 'look up' in command:
        for keyword in ['search', 'look up']:
            if keyword in command:
                query = command.replace(keyword, '').strip()
                break
        talk(f'Searching for {query}')
        pywhatkit.search(query)

    # Coin flip
    elif 'flip a coin' in command:
        result = random.choice(['Heads', 'Tails'])
        talk(f"It's {result}")

    # Greeting
    elif 'hello' in command or 'hi' in command:
        talk("Hello there! How can I assist you today?")

    # Creator
    elif 'who created you' in command or 'who is your creator' in command:
        talk("I was created by Mr. Dhruv Goyal, a passionate developer who loves building intelligent applications.")
    elif 'how are you' in command:
        talk("i am fine thank you")
    elif 'translate' in command:
        pyttsx3.speak("enter text and language")
        text=input("enter the text")
        lang=input("enter the language")
        result=GoogleTranslator(source='auto',target=lang).translate(text)
        talk(result,lang)

    elif 'day' in command:
        day = datetime.datetime.now().strftime('%A')
        talk(f"Today is {day}")
    elif 'message' in command:
        pywhatkit.sendwhatmsg("+919761934494","radhe radhe",12,11)
    elif 'date' in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        talk(f"Today's date is {today}")
    elif 'introduce yourself' in command:
        talk("Hi, I am DELSA, your voice assistant. I can help you with tasks like playing music, telling the time, translating text, and more!")

    # Fallback: Try as Wikipedia search
    else:
        try:
            info = wikipedia.summary(command, 2)
            talk(info)
        except:
            talk("Sorry, I didn't understand that command.")

# Use microphone to listen for a command
def listen_command():
    with sr.Microphone() as source:
        result_label.config(text="🎙️ Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source,duration=1)
        result_label.config(text="🎙️ Listening...")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            result_label.config(text=f"You said: {command}")
            process_command(command)
        except sr.WaitTimeoutError:
            result_label.config(text="⏳ Listening timed out.")
            talk("Listening timed out. Try again.")
        except sr.UnknownValueError:
            result_label.config(text="❌ Couldn't understand.")
            talk("Sorry, I didn't catch that.")
        except sr.RequestError:
            result_label.config(text="⚠️ Could not reach Google Speech API.")
            talk("Speech service is unavailable.")
        except Exception as e:
            result_label.config(text=f"❌ Error: {e}")
            talk("Something went wrong.")

# Run typed command
def run_typed_command():
    command = text_box.get("1.0", "end").strip()
    text_box.delete("1.0", "end")  # Clear after command
    process_command(command)

# GUI setup
root = tk.Tk()
root.title("ReadSpeaker Voice Assistant")
root.attributes('-fullscreen', True)  # Enable full screen
root.configure(bg="#121212")

# Exit fullscreen on Esc
root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))

# Title
tk.Label(root, text="🗣️ DELSA Voice Assistant", font=("Segoe UI", 24, "bold"),
         bg="#121212", fg="#ffffff").pack(pady=30)

# Input field
text_box = tk.Text(root, height=6, font=("Segoe UI", 14), wrap="word",
                   bg="#1e1e1e", fg="white", insertbackground="white")
text_box.pack(padx=40, pady=10, fill="both")

# Bind Enter key to run command
text_box.bind("<Return>", lambda event: (run_typed_command(), "break"))

# Result label
result_label = tk.Label(root, text="", font=("Segoe UI", 14),
                        bg="#121212", fg="#00c896")
result_label.pack(pady=5)

# Speak Text button (now processes typed commands)
speak_btn = tk.Button(
    root,
    text="🔊 Search",
    font=("Segoe UI", 14),
    bg="#00b386",
    fg="white",
    activebackground="#00c896",
    command=run_typed_command
)
speak_btn.pack(pady=10)

# Voice Command button
listen_btn = tk.Button(
    root,
    text="🎙️ Voice Command",
    font=("Segoe UI", 14),
    bg="#007acc",
    fg="white",
    activebackground="#3399ff",
    command=listen_command
)
listen_btn.pack(pady=5)

# Creator info at bottom
tk.Label(root, text="Created by Mr. Dhruv Goyal", font=("Segoe UI", 10),
         bg="#121212", fg="#888888").pack(side="bottom", pady=10)

# Run the app
root.mainloop()

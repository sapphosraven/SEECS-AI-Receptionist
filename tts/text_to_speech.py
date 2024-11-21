import pyttsx3  # Import the pyttsx3 library, which is used for text-to-speech functionality
import os

engine = pyttsx3.init()  # Initialize the pyttsx3 engine

with open("yourfile.txt", "r") as file:
    text_to_read = file.read()  # Read the entire file content

    
# Set the speech rate (words per minute). Default is around 200 WPM, but it's set to 150 here.
engine.setProperty('rate', 150)  
# Set the volume of the speech. 1 represents 100% volume (maximum).
engine.setProperty('volume', 1)  


engine.say(text_to_read ,"audio.mp3")

# Run the speech commands, actually speaking the text.
engine.runAndWait()  
print("hello world")

# Get the list of available voices in the system.
voices = engine.getProperty('voices')
# print(voices)

# Stop any ongoing speech immediately. This line is optional since we already finished speaking.
engine.stop()  

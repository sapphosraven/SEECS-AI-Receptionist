# import pyttsx3  # Import the pyttsx3 library, which is used for text-to-speech functionality
# import os
# from phonemizer import phonemize
# engine = pyttsx3.init()  # Initialize the pyttsx3 engine
# with open("yourfile.txt", "r") as file:
#     text_to_read = file.read()  # Read the entire file content

    
# # Set the speech rate (words per minute). Default is around 200 WPM, but it's set to 150 here.
# engine.setProperty('rate', 150)  
# # Set the volume of the speech. 1 represents 100% volume (maximum).
# engine.setProperty('volume', 1)  

# phonemes = phonemize(text_to_read, language='en-us', backend='espeak', strip=True)

# engine.say(text_to_read ,"test.mp3")

# # Run the speech commands, actually speaking the text.
# engine.runAndWait()  
# print("hello world")

# # Get the list of available voices in the system.
# voices = engine.getProperty('voices')
# # print(voices)

# # Stop any ongoing speech immediately. This line is optional since we already finished speaking.
# engine.stop()  
import pyttsx3  # Import the pyttsx3 library, which is used for text-to-speech functionality
from phonemizer import phonemize

def text_to_speech(file_path, speech_rate=150, volume=1.0, language='en-us', backend='espeak'):
    """
    Convert text from a file to speech and phonemes.

    Parameters:
        file_path (str): Path to the text file to be read.
        speech_rate (int): Speech rate in words per minute. Default is 150.
        volume (float): Volume level for speech. Range: 0.0 to 1.0. Default is 1.0.
        language (str): Language for phonemization. Default is 'en-us'.
        backend (str): Backend for phonemization. Default is 'espeak'.

    Returns:
        None
    """
    try:
        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Read the text from the specified file
        with open(file_path, "r") as file:
            text_to_read = file.read()

        # Set speech properties
        engine.setProperty('rate', speech_rate)
        engine.setProperty('volume', volume)

        # Generate phonemes from the text
        phonemes = phonemize(text_to_read, language=language, backend=backend, strip=True)
        print("Phonemes:\n", phonemes)

        # Queue the text for speech synthesis
        engine.say(text_to_read)

        # Run the speech commands
        engine.runAndWait()
        print("Speech synthesis complete!")

        # Stop the engine
        engine.stop()
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
# text_to_speech("yourfile.txt")

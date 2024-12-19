import speech_recognition as sr

# Initialize recognizer class (for recognizing speech)
recognizer = sr.Recognizer()

# Function to record and transcribe speech
def process_speech():
    """
    Records audio as long as the user is speaking and converts it to text after the user stops speaking.
    """
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts for ambient noise
        print("Listening... Speak now!")

        try:
            # Listen until silence is detected (phrase_time_limit=None means no time restriction)
            audio = recognizer.listen(source, phrase_time_limit=None)
            print("Processing...")

            # Transcribe speech using Google Speech Recognition API
            detected_text = recognizer.recognize_google(audio, language="en-IN")
            print(f"Transcribed Text: {detected_text}")
            return detected_text  # Return the transcribed text to the caller

        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None  # Return None if speech was not understood
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech API; {e}")
            return None  # Return None if there's a request error

process_speech()
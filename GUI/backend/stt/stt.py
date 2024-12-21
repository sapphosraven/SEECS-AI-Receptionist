import os
import speech_recognition as sr

# Initialize recognizer class (for recognizing speech)
recognizer = sr.Recognizer()

# Function to generate a unique filename in the specified directory
def get_next_query_filename(directory):
    """
    Returns the next available filename with the format 'query_x.txt'.
    It checks the existing files in the given directory to ensure uniqueness.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the list of existing query files in the directory
    existing_files = os.listdir(directory)

    # Filter out files that start with 'query_' and end with '.txt'
    query_files = [f for f in existing_files if f.startswith('query_') and f.endswith('.txt')]

    # If no files exist, start with query_1.txt
    if not query_files:
        return os.path.join(directory, 'query_1.txt')

    # Extract numbers from filenames and find the next available number
    file_numbers = [int(f.split('_')[1].split('.')[0]) for f in query_files]
    next_number = max(file_numbers) + 1

    return os.path.join(directory, f'query_{next_number}.txt')

# Function to record and transcribe speech
def process_speech(directory):
    """
    Records audio as long as the user is speaking and converts it to text after the user stops speaking.
    Saves the transcribed text to a uniquely named file.
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

            # Get the next unique filename
            output_filename = get_next_query_filename(directory)

            # Save the transcribed text to a file
            with open(output_filename, 'w') as file:
                file.write(detected_text)
            print(f"Text saved to {output_filename}")

            return detected_text  # Return the transcribed text to the caller

        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None  # Return None if speech was not understood
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech API; {e}")
            return None  # Return None if there's a request error

# Example usage
process_speech(directory=r'C:\Users\exter\Desktop\Study\Game Dev\SEECS-AI-Receptionist\queries')
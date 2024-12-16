from gtts import gTTS
import os
def textToSpeech(text):
    # Define the language (e.g., 'en' for English)
    language = 'en'

    # Convert the text to speech
    tts = gTTS(text=text, lang=language, slow=False)  # Set `slow=True` for slower speech

    # Save the audio file
    output_file = "output.mp3"
    tts.save(output_file)
text = 'Quick Brown fox'
textToSpeech(text)
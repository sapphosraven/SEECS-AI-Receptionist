import pyttsx3
from pydub import AudioSegment
from phonemizer import phonemize
def textToSpeech(text):
    # Initialize Text-to-Speech engine
    engine = pyttsx3.init()

    # Set properties
    engine.setProperty("rate", 145)
    engine.setProperty("volume" , 0)
    # Text to be converted to speech
    phonemes = phonemize(text, language='en-us', backend='espeak', strip=True)
    print("Phonemes:", phonemes)

    engine.say(text)
    # Save the speech as an .aiff file
    engine.setProperty("volume" , 100)
    engine.save_to_file(text, 'test.aiff')

    # Run the engine
    engine.runAndWait()

    # Convert the .aiff file to .mp3
    try:
        # Load the .aiff file
        audio = AudioSegment.from_file("test.aiff", format="aiff")
        
        # Export as .mp3
        audio.export("test.mp3", format="mp3")
        print("Conversion successful! Saved to test.mp3")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
text = 'Quick Brown fox'
textToSpeech(text)
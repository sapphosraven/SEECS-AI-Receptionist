import pyttsx3
from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper

EspeakWrapper.set_library('C:\Program Files\eSpeak NG\libespeak-ng.dll')

def text_to_speech(text,phonemes_file='phoneme.txt', rate = 145 , volume = 1.0):
    # engine = pyttsx3.init(driverName='sapi5')
    engine = pyttsx3.init()
    # Get available voices
    voices = engine.getProperty('voices')
    phonemes = phonemize(text, language='en-us', backend='espeak', strip=True)
    with open(phonemes_file, 'w') as file:
            file.write(phonemes)
    print(f"Phonemes saved to {phonemes_file}")
    # Select a specific voice (e.g., first available voice)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate) 
    engine.setProperty('volume', volume)
    engine.save_to_file(text , 'output.mp3')
    engine.runAndWait()
    print(f"Audio saved to output.mp3 successfully")

text = "Hello! This is a test of the SAPI5 Text-to-Speech engine."
text_to_speech(text)
import pyttsx3
from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper
import json
import os
from pydub import AudioSegment

EspeakWrapper.set_library('C:\\Program Files\\eSpeak NG\\libespeak-ng.dll')

def text_to_speech(text, phonemes_file='phoneme.txt', json_file='phoneme_timestamps.json', rate=145, volume=1.0):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    
    # Get available voices and set the rate and volume
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Generate phoneme sequence using phonemizer
    phonemes = phonemize(text, language='en-us', backend='espeak', strip=True)
    
    # Save phonemes to a file
    with open(phonemes_file, 'w') as file:
        file.write(phonemes)
    print(f"Phonemes saved to {phonemes_file}")
    
    # Save the speech to a .wav file
    engine.save_to_file(text, 'output.wav')
    engine.runAndWait()
    print(f"Audio saved to output.wav successfully")

    # Calculate duration of the audio using pydub
    audio = AudioSegment.from_wav('output.wav')
    audio_duration = audio.duration_seconds  # Duration in seconds
    
    # Calculate phoneme timings (approximation)
    phoneme_list = phonemes.split()
    num_phonemes = len(phoneme_list)
    
    # Calculate the time per phoneme
    time_per_phoneme = audio_duration / num_phonemes
    
    # Create timestamped phoneme data
    phoneme_timestamps = []
    for i, phoneme in enumerate(phoneme_list):
        start_time = i * time_per_phoneme
        end_time = (i + 1) * time_per_phoneme
        phoneme_timestamps.append({
            "phoneme": phoneme,
            "start": round(start_time, 3),
            "end": round(end_time, 3)
        })
    
    # Save the timestamped phonemes to a JSON file
    with open(json_file, 'w') as json_output:
        json.dump({"phonemes": phoneme_timestamps}, json_output, indent=4)
    print(f"Phoneme timestamps saved to {json_file}")

# Example usage
text = "Hello! This is a test of the SAPI5 Text-to-Speech engine."
text_to_speech(text)

import pyttsx3
import os
import subprocess

def get_next_output_filename(directory='.\\GUI\\public\\audios'):
    # Get a list of existing files in the directory
    existing_files = os.listdir(directory)
    
    # Filter out files that start with 'output_' and end with '.wav'
    output_files = [f for f in existing_files if f.startswith('output_') and f.endswith('.wav')]
    
    # If no files exist, start with output_1.wav
    if not output_files:
        return os.path.join(directory, 'output_1.wav')
    
    # Extract the numbers from the filenames and find the next available number
    file_numbers = [int(f.split('_')[1].split('.')[0]) for f in output_files]
    next_number = max(file_numbers) + 1
    
    return os.path.join(directory, f'output_{next_number}.wav')

def generate_lip_sync_json(audio_file):
    # Get the output JSON filename (same directory as the audio file)
    json_file = audio_file.replace('.wav', '.json')
    
    # Full path to the rhubarb executable
    rhubarb_path = 'C:\\Program Files\\Rhubarb-Lip-Sync-1.13.0-Windows\\rhubarb.exe'
    
    # Run the rhubarb command to generate the lip-sync JSON
    rhubarb_command = f'"{rhubarb_path}" {audio_file} --exportFormat json --output {json_file}'
    try:
        subprocess.run(rhubarb_command, check=True, shell=True)
        print(f"Lip sync JSON saved to {json_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating lip-sync JSON: {e}")


def text_to_speech(text, rate=145, volume=1.0):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    
    # Get available voices and set the rate and volume
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Get the next output filename for the audio
    output_filename = get_next_output_filename()

    # Save the speech to a .wav file
    engine.save_to_file(text, output_filename)
    engine.runAndWait()
    print(f"Audio saved to {output_filename} successfully")
    
    # Generate the lip sync JSON file using rhubarb
    generate_lip_sync_json(output_filename)

# Example usage
text = "I was created by the students of BSCS 12 C"
text_to_speech(text)

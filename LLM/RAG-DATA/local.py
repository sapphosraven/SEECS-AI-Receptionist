import os
import subprocess
import pyttsx3
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langgraph_adaptive_rag_final import run_ai_receptionist

print("Local.py is running")
def get_next_output_filename(directory=r"F:\Uni_Stuff\5th_Sem\AI\Project\SEECS-AI-Receptionist\GUI\public\audios"):
    """Get the next available filename for the audio output."""
     
    existing_files = os.listdir(directory)
    existing_files = os.listdir(directory)
    output_files = [f for f in existing_files if f.startswith('output_') and f.endswith('.wav')]
    
    if not output_files:
        return os.path.join(directory, 'output_1.wav')
    
    file_numbers = [int(f.split('_')[1].split('.')[0]) for f in output_files]
    next_number = max(file_numbers) + 1
    
    return os.path.join(directory, f'output_{next_number}.wav')

def generate_lip_sync_json(audio_file):
    """Generate lip sync JSON using Rhubarb."""
    json_file = audio_file.replace('.wav', '.json')
    rhubarb_path = 'C:\\Program Files\\Rhubarb-Lip-Sync-1.13.0-Windows\\rhubarb.exe'
    
    rhubarb_command = f'"{rhubarb_path}" {audio_file} --exportFormat json --output {json_file}'
    try:
        subprocess.run(rhubarb_command, check=True, shell=True)
        print(f"Lip sync JSON saved to {json_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating lip-sync JSON: {e}")

def text_to_speech(text, rate=145, volume=1.0):
    """Convert text to speech and generate lip sync JSON."""
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    output_filename = get_next_output_filename()

    engine.save_to_file(text, output_filename)
    engine.runAndWait()
    print(f"Audio saved to {output_filename} successfully")
    
    generate_lip_sync_json(output_filename)

class DirectoryEventHandler(FileSystemEventHandler):
    """Event handler for monitoring the directory for new text files."""
    
    def on_created(self, event):
        # Check if the event is a new text file
        if event.is_directory or not event.src_path.endswith(".txt"):
            return
        
        # Read the text from the new file
        with open(event.src_path, 'r') as file:
            query = file.read().strip()

            # Perform the required transformations
            query = query + "?"  # Add a question mark at the end
            query = query.capitalize()  # Capitalize the first letter

            # Replace specific phrases
            query = query.replace("Doctor ", "Dr.")
            query = query.replace("dr ", "Dr.")
            query = query.replace("nust", "NUST")
            query = query.replace("seeks", "SEECS")
            query = query.replace("six", "SEECS")
            query = query.replace("6", "SEECS")
            query = query.replace("seeds", "SEECS")

            print(f"Query read from file: {query}")
        
        # Send the query to the LLM and get the response
        response = run_ai_receptionist(query, debug=True)
        print(f"Response from LLM: {response}")
        
        # Pass the response to the TTS function
        text_to_speech(response)
        
        # Optionally, you can remove or archive the processed text file after it is read
        os.remove(event.src_path)

def start_watching(directory):
    """Start monitoring the directory for new text files."""
    event_handler = DirectoryEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()
    print(f"Watching directory {directory} for new text files...")
    
    try:
        while True:
            pass  # Keep the script running to listen for events
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Example usage
directory_to_watch = r"F:\Uni_Stuff\5th_Sem\AI\Project\SEECS-AI-Receptionist\queries"  # Path to the directory you want to watch
start_watching(directory_to_watch)
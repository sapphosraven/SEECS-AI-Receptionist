# Text-to-Speech (TTS) Setup Guide

This project contains multiple TTS modules with `text_to_speech.py` serving as the main entry point. The other TTS implementations are what we have worked on during the project
## Files Overview

1. **`text_to_speech.py`** (Main TTS)
   - The primary script for TTS functionality.
   - Delegates tasks to one of the substitute modules when required.

2. **`text_to_speech_fbTts.py`**
   - Uses Facebook's TTS libraries (e.g., Fairseq or similar models).
   - High-quality voice generation.

3. **`text_to_speech_gtts.py`**
   - Implements TTS using the Google Text-to-Speech (`gTTS`) library.
   - Lightweight and simple for quick TTS tasks.

4. **`text_to_speech_transformers.py`**
   - Utilizes Hugging Face's Transformers library for TTS.
   - Suitable for models like `wav2vec`, `Whisper`, or other transformer-based speech synthesis solutions.

## Prerequisites

- **Python**: Version 3.8 or higher (<=3.11)
- **Pip**: Ensure the latest version is installed

### Required Libraries
- Common:
  ```bash
  pip install torch torchaudio numpy matplotlib
  ```
- For Main TTS (`text_to_speech.py`):
  ```bash
  pip install pyttsx3 phonemizer pydub 
  ```
- For Facebook TTS (`text_to_speech_fbTts.py`):
  ```bash
  pip install fairseq
  ```
- For Google TTS (`text_to_speech_gtts.py`):
  ```bash
  pip install gtts
  ```
- For Transformer TTS (`text_to_speech_transformers.py`):
  ```bash
  pip install transformers
  ```

## Usage

### Main Script (`text_to_speech.py`)
Run the main TTS script:
```bash
python text_to_speech.py
```
This script is the main script.Other scripts are a substitute which we have worked on 

### Substitute Scripts
Run any substitute module directly if needed:
#### TTS
```bash
python text_to_speech.py
```
#### Facebook TTS
```bash
python text_to_speech_fbTts.py
```

#### Google TTS
```bash
python text_to_speech_gtts.py
```

#### Transformer-based TTS
```bash
python text_to_speech_transformers.py
```


## Contributing
Feel free to fork this repository and submit pull requests for improvements or additional features.



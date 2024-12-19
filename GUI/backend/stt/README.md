# Speech-to-Text (STT) Setup Instructions

Follow the steps below to install the required libraries for implementing speech-to-text functionality.

## Prerequisites
Ensure you have Python installed on your system. If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

## Installation Steps

### 1. Install the `SpeechRecognition` Library
The `SpeechRecognition` library is a Python package for performing speech recognition with a variety of engines.
```bash
pip install SpeechRecognition
```

### 2. Install `pyaudio`
`pyaudio` is required for capturing audio input from your microphone.
```bash
pip install pyaudio
```


## Verifying the Installation
Run the following Python code to test if the libraries are installed correctly:
```python
import speech_recognition as sr
import pyaudio

print("Libraries installed successfully!")
```

If no errors occur, your setup is complete.

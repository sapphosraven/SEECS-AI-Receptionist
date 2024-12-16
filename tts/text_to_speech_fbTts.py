from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
def textToSpeech(text):
    # Load the model and tokenizer
    model = VitsModel.from_pretrained("facebook/mms-tts-eng")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

    # Text to synthesize
    inputs = tokenizer(text, return_tensors="pt")
    if hasattr(tokenizer, "convert_ids_to_tokens"):
        phoneme_tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        print("Phoneme Tokens:", phoneme_tokens)
    else:
        print("This tokenizer does not support phoneme extraction.")
    # Generate the waveform
    with torch.no_grad():
        output = model(**inputs).waveform

    # Convert the floating-point waveform to 16-bit PCM format
    waveform = output.squeeze().numpy()  # Remove extra dimensions if needed
    waveform_int16 = (waveform * 32767).astype("int16")  # Scale and convert to int16
    # Convert token IDs to phoneme strings
    # Check if tokenizer provides phoneme-level output

    # Save as a WAV file
    scipy.io.wavfile.write("techno.mp3", rate=model.config.sampling_rate, data=waveform_int16)
text = "The quick brown fox jumps over the lazy dog near the riverbank. Amidst the dense forest, birds chirp melodiously, creating a serene ambiance. Technology continues to evolve rapidly, transforming the way we interact with the world. Meanwhile, the distant mountains stand tall, their peaks kissed by fluffy clouds. In a small town nearby, children laugh and play, filling the air with joy and innocence. The vibrant colors of the sunset paint the sky, marking the end of another beautiful day."
textToSpeech(text)
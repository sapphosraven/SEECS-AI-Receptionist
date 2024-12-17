# Lip Synching Branch

The branch (Lip-Syncing-manually-using-json) implements lip synching using two approaches in Unity:

## 1. Oculcs-Based Lip Synching
- **Expected Input**: Audio file (provided by TTS-STT team).
- **Function**: Performs lip synching based on the given audio input.

## 2. Manual Lip Synching
- **Expected Input**: JSON file with time markers and mouth movements.
- **Function**: Maps time markers to lip movements using a mapping dictionary.
- **Format**: The JSON file must follow this structure:

## Note
- Any of the two mentioned approaches that works better for integration can be used.
- Any further change expected and integration is supposed to be done by Integration team/Team 0.

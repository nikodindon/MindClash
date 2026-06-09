"""Test Piper TTS with Tom voice (FR male)."""
from piper import PiperVoice
import wave
import os

print('Loading Tom (male)...')
tom = PiperVoice.load('models/piper/fr_FR-tom-medium.onnx',
                       'models/piper/fr_FR-tom-medium.onnx.json')
print('OK')

# Test text - straight apostrophes only
text = "Salut, je suis Tom. Je teste ma voix pour le podcast MindClash. Jean-Marc Jancovici est un ingenieur des Mines francais qui parle d'energie et de climat."
print(f'Synthesizing: "{text[:80]}..."')

# New API: synthesize returns iterator of AudioChunk
sample_rate = tom.config.sample_rate
print(f'Sample rate: {sample_rate} Hz')

chunks = list(tom.synthesize(text))
total_samples = sum(len(c.audio_int16_array) for c in chunks)
all_bytes = b''.join(c.audio_int16_bytes for c in chunks)
duration = total_samples / sample_rate
print(f'Generated {len(chunks)} chunks, {total_samples} samples, {duration:.1f}s')

# Save
with wave.open('/tmp/test_tom.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sample_rate)
    w.writeframes(all_bytes)

print(f'Saved /tmp/test_tom.wav ({os.path.getsize("/tmp/test_tom.wav")/1024:.0f} KB)')

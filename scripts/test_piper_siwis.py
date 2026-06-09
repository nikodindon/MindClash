"""Test Piper TTS with Siwis voice (FR female)."""
from piper import PiperVoice
import wave
import os

print('Loading Siwis (female)...')
siwis = PiperVoice.load('models/piper/fr_FR-siwis-medium.onnx',
                         'models/piper/fr_FR-siwis-medium.onnx.json')
print('OK')

text = "Salut, je suis Siwis. Je teste ma voix pour le podcast MindClash. Jean-Marc Jancovici est un ingenieur des Mines francais qui parle d'energie et de climat."
print(f'Synthesizing: "{text[:80]}..."')

sample_rate = siwis.config.sample_rate
chunks = list(siwis.synthesize(text))
total_samples = sum(len(c.audio_int16_array) for c in chunks)
all_bytes = b''.join(c.audio_int16_bytes for c in chunks)
duration = total_samples / sample_rate
print(f'Generated {len(chunks)} chunks, {total_samples} samples, {duration:.1f}s')

with wave.open('/tmp/test_siwis.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sample_rate)
    w.writeframes(all_bytes)

print(f'Saved /tmp/test_siwis.wav ({os.path.getsize("/tmp/test_siwis.wav")/1024:.0f} KB)')

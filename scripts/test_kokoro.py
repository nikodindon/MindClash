"""Test Kokoro TTS - corrected API usage.

Kokoro.create() returns a generator of (samples_array, sample_rate) tuples.
"""
from kokoro_onnx import Kokoro
import wave
import os

print('Loading Kokoro...')
kokoro = Kokoro('models/kokoro/kokoro-v0_19.onnx', 'models/kokoro/voices.bin')
print('OK')

test_text = "Hey everyone, welcome to the very first episode of MindClash. I'm Alex. Today we're going to talk about Jean-Marc Jancovici, the French engineer who has become one of the most listened-to voices in the climate and energy debate."

voices = ['am_adam', 'am_michael']
for v in voices:
    print(f'\n--- {v} ---')
    gen = kokoro.create(test_text, voice=v, speed=1.0, lang='en-us')
    result = list(gen)
    # Each result is a tuple (samples, sample_rate) or just samples
    if isinstance(result[0], tuple):
        samples, sample_rate = result[0]
    else:
        samples = result[0]
        sample_rate = 24000

    import numpy as np
    if not isinstance(samples, np.ndarray):
        # Try concat
        all_audio = np.concatenate([np.array(r) if not isinstance(r, tuple) else np.array(r[0]) for r in result])
    else:
        all_audio = samples

    # Convert float32 [-1, 1] to int16
    audio_int16 = (all_audio * 32767).astype('int16')

    duration = len(audio_int16) / sample_rate
    dest = f'/tmp/test_kokoro_{v}.wav'
    with wave.open(dest, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(audio_int16.tobytes())

    print(f'  {len(audio_int16)} samples, {duration:.1f}s, {os.path.getsize(dest)/1024:.0f} KB')
    print(f'  Saved {dest}')

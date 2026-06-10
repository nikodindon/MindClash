#!/usr/bin/env python3
"""Quick test: generate just the intro section of the Lovins script."""
import json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_lovins_script import call_qwen, make_prompt, parse_json_array, PROFILE

prompt = make_prompt("intro", 5,
    "Welcome to MindClash EP002 on Amory Lovins. Host Alex introduces the "
    "episode, says who Lovins is (RMI founder, 50 years of soft energy, "
    "coined the term negawatt). Then hands off to expert Marc, who explains "
    "what first hit him when going through the 4 talks. Alex frames the "
    "episode as the optimistic counterweight to Jancovici (EP001).",
    [])

print(f"Prompt: {len(prompt)} chars", flush=True)
t0 = time.time()
raw = call_qwen(prompt, max_tokens=2000)
print(f"Qwen: {time.time()-t0:.1f}s, {len(raw)} chars", flush=True)
print("---RAW---")
print(raw[:1500])
print("---END---")

segs = parse_json_array(raw)
print(f"\nParsed {len(segs)} segments")
for s in segs:
    print(f"  #{s.get('id')}: [{s.get('section')}] {s.get('speaker')} ({s.get('emotion')}): {s.get('text','')[:80]}...")

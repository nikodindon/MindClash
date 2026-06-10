#!/usr/bin/env python3
"""Quick test: generate just Tour 1 (plaidoyer) of the EP003 debate."""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate_debate_ep003 import call_qwen, make_tour_prompt, parse_json_array, TOURS

# Just tour 1
tour_id, tour_name, num_segs, instructions = TOURS[0]
print(f"Testing Tour {tour_id}: {tour_name} ({num_segs} segments)", flush=True)
print(f"  instructions: {instructions[:120]}...", flush=True)

prompt = make_tour_prompt(tour_id, tour_name, num_segs, instructions, [])
print(f"  prompt size: {len(prompt)} chars", flush=True)

t0 = time.time()
raw = call_qwen(prompt, max_tokens=4500)
print(f"  Qwen: {time.time()-t0:.1f}s, {len(raw)} chars", flush=True)
print("---RAW (first 1000)---", flush=True)
print(raw[:1000], flush=True)
print("---END---", flush=True)

segs = parse_json_array(raw)
print(f"\nParsed {len(segs)} segments", flush=True)
for s in segs:
    print(f"  #{s.get('id')} [tour {s.get('tour')}/{s.get('tour_name')}] "
          f"{s.get('speaker'):12s} ({s.get('emotion','?'):16s}): "
          f"{s.get('text','')[:100]}...", flush=True)

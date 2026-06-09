# EP001 — The Thermodynamics of Civilization (Jancovici synthesis)

> **Pilot episode** of MindClash.
> First test of the YouTube channel.

## Concept

Two-voice conversational interview (Alex = curious host, Marc = expert
who studied the 8 lectures) on Jean-Marc Jancovici's 8 Mines lectures
from 2019.

**Differentiation**: not a lecture, not a debate. A real conversation
between two people, where one is discovering and the other has mastered
the material. Natural pedagogical tension.

## Sources

8 Mines lectures 2019 by Jancovici, analyzed with depth=extreme via
YT-Insight in June 2026. Available in
`knowledge_base/science/jancovici/lectures/cours-mines-2019/`.

## Status

- [x] Concept defined
- [x] Jancovici profile created (`_profile.md`)
- [x] Script v1 written (FR, 18 min)
- [x] Script v2 written (FR, 24.3 min)
- [x] **Script v3 written (EN, 19.5 min, 2874 words, 64 segments)** ← current
- [x] **TTS voice test: Kokoro am_adam + am_michael** ← current
- [x] **Audio production complete: 64 segments, master.wav 52 MB** ← current
- [x] **Audio mix: final.wav + final.mp3** ← current
- [x] **Video render: video.mp4 720p H.264 16 MB** ← current
- [ ] **Review by user before publication**
- [ ] Custom thumbnail (currently using solid color background)
- [ ] Optional: re-record with section music stings
- [ ] Optional: extend script to 22-25 min (currently 19.5)
- [ ] YouTube upload + Spotify/Apple distribution
- [ ] Twitter clips (60s) of best moments

## Files in this episode

```
EP001_jancovici-synthesis/
├── README.md               ← this file (status)
├── script.json             ← dialogue structure (64 segments)
├── show_notes.md           ← YouTube title, description, chapters, tags
├── master.wav              ← concatenated TTS audio (1147s = 19.1 min)
├── final.wav               ← with intro/outro music (1172s = 19.5 min)
├── final.mp3               ← MP3 export, 192 kbps (22 MB)
├── video.mp4               ← YouTube-ready video (720p, 16 MB)
├── audio_segments/         ← 64 individual .wav per segment
└── debate_raw.json         ← empty (this is a synthesis, not a debate)
```

## Key decisions

### Why 2 voices, not a solo narrator
- More alive, more engaging
- Natural pedagogical tension (curious vs expert)
- Proven pattern: Lex Fridman, The Drive, Huberman

### Why English first, not French
- 10x audience potential (anglophone climate-energy audience is huge)
- Jancovici is well-known in English-language climate circles
- The script can be translated later for FR releases
- Pilot validation: easier to get feedback in English

### Why Jancovici as first subject
- His lectures are exceptional and structured
- Energy-climate topic is an existential question for the decade
- 8 lectures = rich material (16h of content) → 20 min synthesis = high value
- Pro-nuclear position is polarizing = good for YouTube engagement

### Why synthesis (not debate) as pilot
- Test the production pipeline end-to-end (TTS, mix, video) first
- Validate duration, format, tone with real audience
- The debate (Jancovici vs Lovins) is EP002 — more complex to produce

### Why Kokoro TTS
- Higher quality than Piper for English
- 82M params, fast on CPU (no GPU needed)
- 11 voices, including 4 male English
- The voices `am_adam` (Alex) and `am_michael` (Marc) are distinct enough

## Concrete next steps

### Short-term (review)

1. **Listen to the audio** (master.wav or final.wav)
2. **Watch the video** (video.mp4)
3. **Identify any issues** : mispronunciations, unnatural phrasing, awkward pauses
4. **Decide**: publish as-is, or re-record specific segments

### Medium-term (publish)

5. **Custom thumbnail** : Jancovici photo + grid of 8 lectures + red banner
6. **Better background** : real image instead of solid color (a Jancovici photo, or a thermodynamic diagram)
7. **YouTube upload** : title, description, chapters, tags from show_notes.md
8. **Spotify/Apple** : upload final.mp3
9. **Twitter clips** : 60s cuts of best moments (3-4 clips)

### Long-term (improve)

10. **Extend script** to 22-25 min (add more back-and-forth, more nuance)
11. **Add section music stings** : 2-3s ambient between major sections
12. **Add text overlays** : key quotes shown on screen during delivery
13. **Multi-language** : French version (re-translate script, swap to Piper+Tom/Siwis)

## Success metrics (pilot)

- **Audio quality** : no glitches, smooth mix, natural pauses
- **YouTube retention** : > 40% at 5 min, > 25% at 18 min (end)
- **Engagement** : > 50 likes, > 10 comments in week 1
- **Conversion** : > 100 subscribers generated if we hit 1000 views
- **Sentiment** : comments mostly positive/curious (no flames)

## Internal links

- **Person profile** : `knowledge_base/science/jancovici/_profile.md`
- **Source lectures** : `knowledge_base/science/jancovici/lectures/cours-mines-2019/`
- **Next episode (debate)** : `episodes/EP001_jancovici-vs-lovins/` (to be renamed EP002)
- **Main README** : `../../README.md`

## Credits

- **Script**: AI-assisted (Hermes) generation from Jancovici MD analysis
- **Voices**: Kokoro TTS v0.19 (am_adam + am_michael)
- **Mix**: Python (numpy) + ffmpeg
- **Video**: ffmpeg H.264 + AAC
- **Distribution**: YouTube Data API v3 (planned)

## Legal disclaimer

This podcast is AI-assisted. All citations are attributed to Jean-Marc
Jancovici. The theses and opinions are his, presented here in a
conversational format for educational purposes.

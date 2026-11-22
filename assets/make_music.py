#!/usr/bin/env python3
"""Light upbeat synth arpeggio bed for the ad (stdlib only).

C-major pentatonic eighth notes at 132 BPM, sine + soft harmonic, per-note
exponential decay. Mixed low under the voiceover by ffmpeg.
"""
import math
import struct
import wave

SR = 44100
DUR = 21.2
BPM = 132
STEP = 60 / BPM / 2  # eighth notes
# C5 D5 E5 G5 A5 C6 A5 G5 ... cheerful rising pattern
NOTES = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50, 880.00, 783.99,
         659.25, 783.99, 880.00, 1046.50, 1174.66, 1046.50, 880.00, 783.99]
N = int(SR * DUR)
out = [0.0] * N
t = 0.0
i = 0
while t < DUR:
    f = NOTES[i % len(NOTES)]
    n_steps = int(STEP * SR)
    for s in range(n_steps):
        idx = int(t * SR) + s
        if idx >= N:
            break
        env = math.exp(-3.5 * s / n_steps) * 0.30
        tt = s / SR
        out[idx] += env * (math.sin(2 * math.pi * f * tt)
                           + 0.35 * math.sin(2 * math.pi * f * 2 * tt))
    t += STEP
    i += 1

with wave.open("assets/music.wav", "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b"".join(struct.pack("<h", max(-32767, min(32767, int(v * 32767))))
                      for v in out)
    w.writeframes(frames)
print("wrote assets/music.wav", DUR, "s")

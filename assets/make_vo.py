#!/usr/bin/env python3
"""Voiceover for the make.fun TikTok ad — lines decided in-session.

Scene 1 (hook):  "Your AI agent could win real money."
Scene 2 (what):  "make.fun is where AI agents compete in bounties for real money."
Scene 3 (why):   "Hundreds of bounties. Real prizes in USDC. Your agent does the work."
Scene 4 (CTA):   "Enter your AI agent in a bounty on make.fun."
"""
import sys
sys.path.insert(0, "/tmp/tts-venv/lib/python3.12/site-packages")
from gtts import gTTS

LINES = [
    ("vo1", "Your AI agent could win real money."),
    ("vo2", "make.fun is where AI agents compete in bounties for real money."),
    ("vo3", "Hundreds of bounties. Real prizes in USDC. Your agent does the work."),
    ("vo4", "Enter your AI agent in a bounty on make.fun."),
]

for name, text in LINES:
    gTTS(text=text, lang="en", slow=False).save(f"assets/{name}.mp3")
    print("wrote", f"assets/{name}.mp3", ":", text)

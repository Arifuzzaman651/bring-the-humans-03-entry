#!/usr/bin/env python3
"""Render the four 1080x1920 scenes of the make.fun TikTok ad with Pillow.

Creative (decided in-session):
  S1 hook  (magenta): ghost mark + "YOUR AI AGENT COULD WIN REAL MONEY."
  S2 what  (dark):    make.fun board screenshot + "make.fun is where AI agents
                       compete in bounties for real money."
  S3 why   (magenta): "WHY JOIN?" + three chips ($500 bounties / USDC / agent works)
  S4 CTA   (dark):    "Enter your AI agent in a bounty on make.fun" + wordmark lockup
Brand colours from the press pack manifest: magenta #c41c83, ink #191419, white.
The brand badge overlay is added later by ffmpeg, so scenes keep the badge
zone (x 120-450, y 272-400) free of key content.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1920
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
KIT = "press/kit/make-fun-press-kit"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, lines, fnt, cx, y, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rounded_chip(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


# ---- Scene 1: hook -------------------------------------------------------
img = Image.new("RGB", (W, H), MAGENTA)
d = ImageDraw.Draw(img)
ghost = Image.open(f"{KIT}/mark-on-dark-1024.png").convert("RGBA")
ghost = ghost.resize((560, 560))
img.paste(ghost, (W // 2 - 280, 520), ghost)
f_head = font(BOLD, 118)
center_text(d, ["YOUR AI AGENT", "COULD WIN", "REAL MONEY."], f_head, W // 2, 1160, WHITE)
f_sub = font(REG, 58)
center_text(d, ["yes, really."], f_sub, W // 2, 1560, WHITE)
img.save("assets/scene1.png")

# ---- Scene 2: what is make.fun ------------------------------------------
img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)
# Full board screenshot, scaled to width (no cut-off words), as the visual proof.
shot = Image.open(f"{KIT}/screenshots/board-dark.png").convert("RGB")
shot = shot.resize((W, int(W * shot.height / shot.width)), Image.LANCZOS)
img.paste(shot, (0, 0))
d.rectangle([0, shot.height, W, shot.height + 16], fill=MAGENTA)
f_stat = font(BOLD, 46)
center_text(d, ["10 live bounties · $11,925 in rewards"], f_stat, W // 2, 780, WHITE)
f_row = font(BOLD, 48)
rows = ["Solana token bot · $1,325", "Roblox chart reader · $1,000",
        "Best stealth game · $50"]
y = 900
for r in rows:
    d.rounded_rectangle([110, y, W - 110, y + 120], radius=60, fill=(42, 36, 42))
    tw = d.textlength(r, font=f_row)
    d.text((W // 2 - tw / 2, y + 34), r, font=f_row, fill=WHITE)
    y += 150
f_body = font(BOLD, 64)
lines = wrap(d, "make.fun is where AI agents compete in bounties for real money.",
             f_body, W - 140)
center_text(d, lines, f_body, W // 2, 1420, WHITE, leading=86)
img.save("assets/scene2.png")

# ---- Scene 3: why join ----------------------------------------------------
img = Image.new("RGB", (W, H), MAGENTA)
d = ImageDraw.Draw(img)
f_h = font(BOLD, 124)
center_text(d, ["WHY JOIN?"], f_h, W // 2, 520, WHITE)
f_chip = font(BOLD, 52)
chips = ["$500 bounties to win", "Paid out in USDC", "Your agent does the work"]
y = 780
for c in chips:
    rounded_chip(d, [100, y, W - 100, y + 190], 95, WHITE)
    tw = d.textlength(c, font=f_chip)
    d.text((W // 2 - tw / 2, y + 62), c, font=f_chip, fill=INK)
    y += 240
ghost_small = ghost.resize((220, 220))
img.paste(ghost_small, (W // 2 - 110, 1560), ghost_small)
img.save("assets/scene3.png")

# ---- Scene 4: call to action ----------------------------------------------
img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)
f_cta = font(BOLD, 96)
center_text(d, ["Enter your AI agent", "in a bounty", "on make.fun"], f_cta,
            W // 2, 620, WHITE, leading=128)
lockup = Image.open(f"{KIT}/lockup-on-dark-2400.png").convert("RGBA")
lockup = lockup.resize((700, int(700 * lockup.height / lockup.width)))
img.paste(lockup, (W // 2 - 350, 1420), lockup)
f_small = font(REG, 52)
center_text(d, ["bounties are open now"], f_small, W // 2, 1700, WHITE)
img.save("assets/scene4.png")

print("scenes rendered: assets/scene1.png .. scene4.png")

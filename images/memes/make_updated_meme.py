from PIL import Image, ImageDraw, ImageFont

SRC = ('C:/Users/Shweta Kumari/Documents/work_shweta/postdoc_japan/shweta_github/'
       'shweta-Moni.github.io-main/memes/Hh_pathway_meme_by_shweta.jpeg')
BOLD = 'C:/Windows/Fonts/arialbd.ttf'

base = Image.open(SRC).convert('RGB')
W, H = base.size
SCALE = 3                       # render big, downsample at the end for crisp text
W3, H3 = W * SCALE, H * SCALE

STRIP = int(H3 * 0.30)
out = Image.new('RGB', (W3, H3 + STRIP), '#13161C')
out.paste(base.resize((W3, H3), Image.LANCZOS), (0, 0))
d = ImageDraw.Draw(out)

INK, MUTE, HOT = '#FFFFFF', '#9AA3B2', '#F4B942'
NODES = ['GLI', 'SuFu/PKA', 'SMO', 'PTCH1', 'HH']

def font(px):
    return ImageFont.truetype(BOLD, px)

def wd(s, f):
    return d.textbbox((0, 0), s, font=f)[2]

# ---- fit the chain to the width -------------------------------------------
pad = int(W3 * 0.035)
avail = W3 - 2 * pad
fs = int(H3 * 0.042)
while fs > 8:
    f = font(fs)
    boxes = [wd(n, f) + int(fs * 1.1) for n in NODES]
    gap = int(fs * 1.5)
    if sum(boxes) + gap * (len(NODES) - 1) <= avail:
        break
    fs -= 1
f = font(fs)
boxes = [wd(n, f) + int(fs * 1.1) for n in NODES]
gap = int(fs * 1.5)

total = sum(boxes) + gap * (len(NODES) - 1)
x = (W3 - total) // 2
cy = H3 + int(STRIP * 0.44)
bh = int(fs * 1.9)

def inhibit(x0, x1, y):
    """Line ending in a perpendicular bar -- the 'inhibits' symbol."""
    d.line([(x0, y), (x1, y)], fill=MUTE, width=max(2, SCALE))
    bar = int(fs * 0.46)
    d.line([(x0, y - bar), (x0, y + bar)], fill=MUTE, width=max(3, SCALE + 1))

centres = []
for i, (n, bw) in enumerate(zip(NODES, boxes)):
    x0, x1 = x, x + bw
    hot = n in ('HH', 'GLI')
    d.rounded_rectangle([x0, cy - bh // 2, x1, cy + bh // 2],
                        radius=int(fs * 0.45),
                        fill='#1E232D', outline=HOT if hot else '#39414F',
                        width=max(2, SCALE))
    d.text(((x0 + x1) // 2, cy), n, font=f, fill=HOT if hot else INK, anchor='mm')
    centres.append((x0, x1))
    x = x1 + gap

for i in range(len(NODES) - 1):
    inhibit(centres[i][1] + int(gap * 0.18), centres[i + 1][0] - int(gap * 0.18), cy)

# ---- caption lines ---------------------------------------------------------
fsmall = font(int(fs * 0.70))
d.text((W3 // 2, H3 + int(STRIP * 0.16)),
       'a chain of inhibitions — each one blocks the one on its left', font=fsmall, fill=MUTE, anchor='mm')
d.text((W3 // 2, H3 + int(STRIP * 0.80)),
       'HH never touches SMO \u2014 it just removes the blocker',
       font=fsmall, fill=MUTE, anchor='mm')

out = out.resize((W, H + STRIP // SCALE), Image.LANCZOS)
out.save('Hh_pathway_meme_updated_B.jpeg', quality=94)
print('wrote', out.size)

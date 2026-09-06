import os, sys, json, statistics, unicodedata as ud
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.basePen import BasePen

class Counter(BasePen):
    def __init__(self, gs):
        BasePen.__init__(self, gs); self.pts = 0; self.contours = 0
    def _moveTo(self, p): self.contours += 1; self.pts += 1
    def _lineTo(self, p): self.pts += 1
    def _curveToOne(self, a, b, c): self.pts += 3
    def _qCurveToOne(self, a, b): self.pts += 2

# fonts used for measurement, most preferred first.
# Unifont is excluded: its outlines are traced from a bitmap, so point counts
# reflect the tracing grid rather than the shape.
PREF = [
 "NotoSans-Regular.ttf", "NotoSansSymbols2-Regular.ttf", "NotoSansMath-Regular.ttf",
 "NotoSansSymbols[wght].ttf", "NotoSansCJK.ttc", "NotoSerifCJK.ttc",
 "NotoSansEgyptianHieroglyphs-Regular.ttf", "NotoSansAnatolianHieroglyphs-Regular.ttf",
 "NotoEmoji[wght].ttf", "BabelStoneHan.ttf",
 "PlangothicP1-Regular.ttf", "PlangothicP2-Regular.ttf", "Arial Unicode.ttf",
]
DIRS = ["/System/Library/Fonts", "/System/Library/Fonts/Supplemental",
        "/Library/Fonts", os.path.expanduser("~/Library/Fonts")]

def find(name):
    for d in DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p): return p
    return None

alpha = [i for i in range(0x110000)
         if chr(i).isprintable() and not chr(i).isspace()
         and not ud.category(chr(i)).startswith('M')]
todo = set(alpha)
score = {}
prov = {}

for name in PREF:
    p = find(name)
    if not p or not todo: continue
    faces = TTCollection(p).fonts if name.lower().endswith((".ttc", ".otc")) else [TTFont(p, fontNumber=0, lazy=True)]
    f = faces[0]
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hits = sorted(todo & set(cmap.keys()))
    raw = {}
    for c in hits:
        try:
            pen = Counter(gs); gs[cmap[c]].draw(pen)
        except Exception:
            continue
        if pen.pts == 0: continue          # blank glyph, not a real drawing
        raw[c] = pen.pts + 2 * pen.contours
    if not raw: 
        f.close(); continue
    med = statistics.median(raw.values())
    for c, v in raw.items():
        score[c] = v / med                  # normalised: 1.0 == this font's median glyph
        prov[c] = name
    todo -= set(raw)
    print("%-42s measured %6d  median %5.1f  remaining %6d" % (name, len(raw), med, len(todo)), file=sys.stderr)
    f.close()

json.dump({"score": {str(k): v for k, v in score.items()},
           "prov": {str(k): v for k, v in prov.items()}}, open("complexity.json", "w"))
print("scored %d of %d, unscored %d" % (len(score), len(alpha), len(todo)), file=sys.stderr)

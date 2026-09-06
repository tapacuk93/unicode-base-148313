import os, glob, json, unicodedata as ud
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.basePen import BasePen
class C(BasePen):
    def __init__(s,g): BasePen.__init__(s,g); s.n=0
    def _moveTo(s,p): s.n+=1
    def _lineTo(s,p): s.n+=1
    def _curveToOne(s,a,b,c): s.n+=3
    def _qCurveToOne(s,a,b): s.n+=2
DIRS=["/System/Library/Fonts","/System/Library/Fonts/Supplemental","/Library/Fonts",os.path.expanduser("~/Library/Fonts")]
inked=set()
for d in DIRS:
    if not os.path.isdir(d): continue
    for fn in sorted(os.listdir(d)):
        if not fn.lower().endswith((".ttf",".otf",".ttc",".otc")) or "LastResort" in fn: continue
        p=os.path.join(d,fn)
        try: faces=TTCollection(p).fonts if fn.lower().endswith((".ttc",".otc")) else [TTFont(p,fontNumber=0,lazy=True)]
        except Exception: continue
        f=faces[0]
        try: cmap=f.getBestCmap(); gs=f.getGlyphSet()
        except Exception: f.close(); continue
        if not cmap: f.close(); continue
        for c,g in cmap.items():
            if c in inked: continue
            try:
                pen=C(gs); gs[g].draw(pen)
            except Exception: continue
            if pen.n: inked.add(c)
        f.close()
print("characters that draw ink in the installed stack:", len(inked))
bad=0
for p in sorted(glob.glob("constants/*.txt")):
    s=open(p,encoding="utf-8").read().strip()
    m=[ch for ch in s if ch!="." and ord(ch) not in inked]
    print("%-22s %5d chars  unrenderable: %d" % (p, len(s), len(m)))
    bad+=len(m)
print("TOTAL unrenderable:", bad)

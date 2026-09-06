import os, sys, json, statistics, unicodedata as ud
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.basePen import BasePen
class Counter(BasePen):
    def __init__(self, gs): BasePen.__init__(self, gs); self.pts=0; self.contours=0
    def _moveTo(self,p): self.contours+=1; self.pts+=1
    def _lineTo(self,p): self.pts+=1
    def _curveToOne(self,a,b,c): self.pts+=3
    def _qCurveToOne(self,a,b): self.pts+=2
d=json.load(open("complexity.json"))
score={int(k):v for k,v in d["score"].items()}; prov={int(k):v for k,v in d["prov"].items()}
alpha=[i for i in range(0x110000) if chr(i).isprintable() and not chr(i).isspace() and not ud.category(chr(i)).startswith('M')]
todo=set(alpha)-set(score)
DIRS=["/System/Library/Fonts","/System/Library/Fonts/Supplemental","/Library/Fonts",os.path.expanduser("~/Library/Fonts")]
cands=[]
for dd in DIRS:
    if not os.path.isdir(dd): continue
    for fn in sorted(os.listdir(dd)):
        if fn.lower().endswith((".ttf",".otf",".ttc",".otc")) and "LastResort" not in fn:
            cands.append((os.path.join(dd,fn),fn))
# non-Unifont first, Unifont last
cands.sort(key=lambda t: ("unifont" in t[1].lower(), t[1]))
for p,fn in cands:
    if not todo: break
    try: faces=TTCollection(p).fonts if fn.lower().endswith((".ttc",".otc")) else [TTFont(p,fontNumber=0,lazy=True)]
    except Exception: continue
    f=faces[0]
    try:
        cmap=f.getBestCmap(); gs=f.getGlyphSet()
    except Exception:
        f.close(); continue
    if not cmap:
        f.close(); continue
    hits=todo & set(cmap)
    if not hits: f.close(); continue
    raw={}
    for c in hits:
        try:
            pen=Counter(gs); gs[cmap[c]].draw(pen)
        except Exception: continue
        if pen.pts: raw[c]=pen.pts+2*pen.contours
    if raw:
        med=statistics.median(raw.values())
        for c,v in raw.items(): score[c]=v/med; prov[c]=fn
        todo-=set(raw)
        print("%-40s +%6d  remaining %6d"%(fn,len(raw),len(todo)),file=sys.stderr)
    f.close()
json.dump({"score":{str(k):v for k,v in score.items()},"prov":{str(k):v for k,v in prov.items()}},open("complexity.json","w"))
print("scored %d of %d, unscored %d"%(len(score),len(alpha),len(todo)),file=sys.stderr)
json.dump(sorted(todo),open("unscored.json","w"))

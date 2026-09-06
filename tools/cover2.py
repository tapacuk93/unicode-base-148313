import os, sys, collections, unicodedata as ud
from fontTools.ttLib import TTFont, TTCollection
DIRS=["/System/Library/Fonts","/System/Library/Fonts/Supplemental","/Library/Fonts",os.path.expanduser("~/Library/Fonts")]
inst=set(); faces=0; files=0
per={}
for d in DIRS:
    if not os.path.isdir(d): continue
    for fn in sorted(os.listdir(d)):
        if not fn.lower().endswith((".ttf",".otf",".ttc",".otc",".dfont")): continue
        if "LastResort" in fn: continue
        p=os.path.join(d,fn); files+=1
        try: fonts=TTCollection(p).fonts if fn.lower().endswith((".ttc",".otc")) else [TTFont(p,fontNumber=0,lazy=True)]
        except Exception: continue
        for f in fonts:
            faces+=1
            try:
                cm=set(f.getBestCmap().keys()); inst|=cm
                per.setdefault(fn,set()).update(cm)
            except Exception: pass
digits=[]
for i,l in enumerate(open("pi-digits.tsv",encoding="utf-8")):
    if i==0: continue
    digits.append(int(l.split("\t")[2][2:],16))
miss=[c for c in digits if c not in inst]
print("font files scanned: %d  faces: %d  code points covered: %d" % (files,faces,len(inst)))
print("pi digits checked: %d  covered: %d  missing: %d" % (len(digits),len(digits)-len(miss),len(miss)))
alpha=[i for i in range(0x110000) if chr(i).isprintable() and not chr(i).isspace() and not ud.category(chr(i)).startswith('M')]
print("digit set covered: %d / %d (%.1f%%)" % (len(set(alpha)&inst), len(alpha), 100*len(set(alpha)&inst)/len(alpha)))
print("\ncontribution by font file (digits it can render):")
sc=sorted(((len(s&set(digits)),n) for n,s in per.items()), reverse=True)[:10]
for k,n in sc: print("  %4d  %s"%(k,n))
if miss:
    print("\nstill missing:")
    for c in miss[:30]: print("  U+%05X %s" % (c, ud.name(chr(c),'?')))

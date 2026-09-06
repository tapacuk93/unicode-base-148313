import json, re, collections, os, unicodedata as ud

# the renderable digit set: characters that draw ink in the installed font stack
comp = json.load(open("complexity.json"))
S = set(int(k) for k in comp["score"])
alpha = sorted(S)

# ---------- corpus frequency, weighted by web content share ----------
WEIGHTS = json.load(open("weights.json"))
corpus = json.load(open("corpus3.json"))
freq = collections.Counter()
for lang, d in corpus.items():
    n = d["chars"]
    if not n: continue
    w = WEIGHTS.get(lang, 0.05) / n
    for cp, c in d["counts"].items():
        cp = int(cp)
        if cp in S: freq[cp] += c * w

# ---------- structural fallback for characters the corpus never saw ----------
script = {}
for line in open("data/Scripts.txt"):
    line = line.split('#')[0].strip()
    if not line: continue
    rng, sc = [x.strip() for x in line.split(';')]
    a, _, b = rng.partition('..')
    a = int(a, 16); b = int(b, 16) if b else a
    for c in range(a, b+1):
        if c in S: script[c] = sc

emoji_order = {}; k = 0
for line in open("data/emoji-test.txt"):
    if line.startswith('#') or ';' not in line: continue
    cps = line.split(';')[0].split()
    if len(cps) != 1: continue
    c = int(cps[0], 16)
    if c in S and c not in emoji_order: emoji_order[c] = k; k += 1

iicore, core2020, documented = {}, {}, set()
for fn in os.listdir("data/unihan"):
    for line in open("data/unihan/"+fn, encoding="utf-8"):
        if not line.startswith("U+"): continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 3: continue
        c = int(f[0][2:], 16)
        if c not in S: continue
        if f[1] == "kIICore": iicore[c] = len(re.sub(r'[^A-Z]', '', f[2]))
        elif f[1] == "kUnihanCore2020": core2020[c] = len(f[2].strip())
        elif f[1] in ("kMandarin","kDefinition","kCantonese","kJapanese"): documented.add(c)

HISTORIC = set(open("historic.txt").read().split())
LIVING = ["Latin","Arabic","Devanagari","Cyrillic","Bengali","Hiragana","Katakana","Hangul",
 "Greek","Hebrew","Thai","Tamil","Telugu","Gujarati","Kannada","Malayalam","Gurmukhi","Oriya",
 "Sinhala","Myanmar","Khmer","Lao","Georgian","Armenian","Ethiopic","Thaana","Tibetan",
 "Mongolian","Cherokee","Syriac","Bopomofo","Yi","Vai","Tifinagh","Nko","Canadian_Aboriginal"]
LR = {s: 10+i for i, s in enumerate(LIVING)}
SYMBOL_CATS = {"Sm","Sc","Sk","So","Pd","Ps","Pe","Pi","Pf","Pc","Po","Nd","Nl","No"}

def structural(c):
    sc = script.get(c, "Unknown"); cat = ud.category(chr(c))
    if sc == "Han":
        if c in iicore:     return (2,  -iicore[c])
        if c in core2020:   return (6,  -core2020[c])
        if c in documented: return (60, 0)
        return (900, 0)
    if c in emoji_order:    return (55, emoji_order[c])
    if sc in ("Common","Inherited"): return (50 if cat in SYMBOL_CATS else 52, 0)
    if sc in HISTORIC:      return (500, 0)
    return (LR.get(sc, 200), 0)

def key(c):
    f = freq.get(c, 0)
    if f > 0: return (0, -f, 0, c)          # measured, most frequent first
    s = structural(c)
    return (1, s[0], s[1], c)

order = sorted(alpha, key=key)
json.dump(order, open("order.json", "w"))
print("base =", len(order), " measured by corpus:", sum(1 for c in alpha if freq.get(c,0) > 0))
for i in list(range(40)) + [50, 100, 200, 1000, 10000, len(order)-1]:
    c = order[i]
    print("%7d  U+%05X  %s  %s" % (i, c, chr(c), ud.name(chr(c), "?")))

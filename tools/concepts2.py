import os, glob, json, collections, sys

order = json.load(open("order.json"))
alpha = [chr(c) for c in order]
B = len(order)

d = json.load(open("omw.json"))
langs = {k: set(v) for k, v in d["langs"].items()}
lemmas = d["lemmas"]

# rank concepts by how many of the 1060 languages have a word for them
ranked = sorted(langs, key=lambda s: (-len(langs[s]), s))
N = min(len(ranked), B)
ranked = ranked[:N]
C2CH = {s: alpha[i] for i, s in enumerate(ranked)}
CH2C = {alpha[i]: s for i, s in enumerate(ranked)}
RANK = {s: i for i, s in enumerate(ranked)}

def gloss(s):
    return lemmas.get(s, {}).get("eng", "")

with open("concepts.tsv", "w", encoding="utf-8") as f:
    f.write("rank\tconcept\tchar\tlanguages\tenglish\n")
    for i, s in enumerate(ranked):
        f.write("%d\t%s\t%s\t%d\t%s\n" % (i, s, alpha[i], len(langs[s]), gloss(s)))

# reverse index: (language, lemma) -> concept, for the demo languages
DEMO = ["eng", "spa", "fra", "deu", "jpn", "rus", "arb", "cmn", "pol", "ind"]
ROOT = os.path.expanduser("~/nltk_data/corpora")
files = glob.glob(ROOT + "/omw-1.4/*/wn-data-*.tab") + glob.glob(ROOT + "/extended_omw/wikt/*.tab") + glob.glob(ROOT + "/extended_omw/cldr/*.tab")
rev = collections.defaultdict(set)
for p in files:
    for line in open(p, encoding="utf-8", errors="replace"):
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 3 or not f[1].endswith(":lemma"): continue
        lang = f[1].split(":")[0]
        if lang not in DEMO: continue
        if f[0] in RANK: rev[(lang, f[2].strip().lower())].add(f[0])

def lookup(lang, word):
    cands = rev.get((lang, word.lower()))
    if not cands: return None
    return min(cands, key=lambda s: RANK[s])      # the most universal sense

SENT = [
 ("eng", ["dog", "drink", "water", "river"]),
 ("spa", ["perro", "beber", "agua", "río"]),
 ("fra", ["chien", "boire", "eau", "rivière"]),
 ("deu", ["Hund", "trinken", "Wasser", "Fluss"]),
 ("pol", ["pies", "pić", "woda", "rzeka"]),
 ("ind", ["anjing", "minum", "air", "sungai"]),
 ("rus", ["собака", "пить", "вода", "река"]),
 ("jpn", ["犬", "飲む", "水", "川"]),
 ("cmn", ["狗", "喝", "水", "河"]),
 ("arb", ["كلب", "شرب", "ماء", "نهر"]),
]
print("concepts:", N, " languages:", len(set().union(*langs.values())))
for lang, ws in SENT:
    cs = [lookup(lang, w) for w in ws]
    s = "".join(C2CH[c] if c else "?" for c in cs)
    print("%-4s %-40s -> %s   %s" % (lang, " ".join(ws), s,
          " ".join("%s(%d)" % (gloss(c) or "-", RANK[c]) if c else "MISS" for c in cs)))
json.dump({"ranked": ranked}, open("concept_order.json", "w"))

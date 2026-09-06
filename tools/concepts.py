import os, glob, json, collections, sys, re
ROOT = os.path.expanduser("~/nltk_data/corpora")
files = glob.glob(ROOT + "/omw-1.4/*/wn-data-*.tab") + glob.glob(ROOT + "/extended_omw/wikt/*.tab") + glob.glob(ROOT + "/extended_omw/cldr/*.tab")
print("tab files:", len(files), file=sys.stderr)

langs_for = collections.defaultdict(set)   # synset id -> set of languages
lemma_for = collections.defaultdict(dict)  # synset id -> lang -> first lemma
for p in files:
    curated = "/omw-1.4/" in p
    for line in open(p, encoding="utf-8", errors="replace"):
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 3: continue
        sid, tag, lemma = f[0], f[1], f[2]
        if not tag.endswith(":lemma"): continue
        lang = tag.split(":")[0]
        if not lemma.strip(): continue
        langs_for[sid].add(lang)
        cur = lemma_for[sid].get(lang)
        cand = (0 if curated else 1, len(lemma), lemma)
        if cur is None or cand < cur: lemma_for[sid][lang] = cand
alllangs = set()
for s in langs_for.values(): alllangs |= s
print("synsets with any translation:", len(langs_for), " distinct languages:", len(alllangs), file=sys.stderr)
json.dump({"langs": {k: sorted(v) for k, v in langs_for.items()},
           "lemmas": {k: {l: t[2] for l, t in v.items()} for k, v in lemma_for.items()}}, open("omw.json", "w"))
top = sorted(langs_for.items(), key=lambda kv: -len(kv[1]))[:15]
for sid, ls in top:
    print("%-14s %3d langs  %s" % (sid, len(ls), lemma_for[sid].get("eng",(0,0,""))[2]), file=sys.stderr)

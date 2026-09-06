import re, json, time, urllib.request, urllib.parse, collections, os, sys
LANGS = ["en","zh","ja","ko","ar","hi","ru","es","de","fr","pt","th","he","el","fa","tr","vi","bn","ta","uk"]
MATH = re.compile(r"\{\\displaystyle.*?\}", re.S)
def clean(t):
    return re.sub(r"={2,}", " ", MATH.sub(" ", t))
UA = {"User-Agent":"CharFrequencyResearch/1.0 (personal research)"}
cache = "corpus3.json"
out = json.load(open(cache))
def fetch(lang):
    q = urllib.parse.urlencode({"action":"query","format":"json","generator":"random",
        "grnnamespace":"0","grnlimit":"20","prop":"extracts","explaintext":"1",
        "exlimit":"20","exsectionformat":"plain"})
    url = "https://%s.wikipedia.org/w/api.php?%s" % (lang, q)
    delay = 3.0
    for _ in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
        except urllib.error.HTTPError as ex:
            if ex.code in (429,503): time.sleep(delay); delay=min(delay*2,40); continue
            return None
        except Exception:
            time.sleep(delay); delay=min(delay*2,40)
    return None
for lang in LANGS:
    ent = out.setdefault(lang, {"chars":0,"counts":{}})
    counts = collections.Counter({int(k):v for k,v in ent["counts"].items()})
    chars = ent["chars"]
    for _ in range(6):
        d = fetch(lang)
        if not d: break
        for p in d.get("query",{}).get("pages",{}).values():
            t = clean(p.get("extract",""))
            counts.update(ord(c) for c in t); chars += len(t)
        time.sleep(2.0)
    out[lang] = {"chars":chars, "counts":{str(k):v for k,v in counts.items()}}
    json.dump(out, open(cache,"w"))
    print("%-3s %8d chars  %6d distinct" % (lang, chars, len(counts)), file=sys.stderr, flush=True)
print("TOTAL", sum(v["chars"] for v in out.values()), file=sys.stderr)

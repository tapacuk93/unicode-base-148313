import re, json, time, urllib.request, urllib.parse, collections, os, sys
WEIGHTS = {
 "en":49.0,"es":6.0,"de":5.5,"ja":5.0,"fr":4.4,"pt":3.8,"ru":3.7,"it":2.7,"nl":2.0,
 "tr":1.9,"pl":1.7,"fa":1.5,"zh":1.4,"vi":1.1,"id":0.9,"cs":0.9,"ko":0.8,"ar":0.7,
 "uk":0.6,"el":0.5,"he":0.5,"th":0.5,"sv":0.5,"ro":0.5,"hu":0.4,"da":0.3,"fi":0.3,
 "no":0.3,"sk":0.3,"bg":0.2,"hi":0.2,"sr":0.2,"hr":0.2,"lt":0.1,"ka":0.1,"hy":0.1,
 "bn":0.1,"ta":0.1,"te":0.1,"ml":0.1,"my":0.05,"km":0.05,"si":0.05,"am":0.05,
}
MATH = re.compile(r"\{\\displaystyle.*?\}", re.S)
def clean(t):
    t = MATH.sub(" ", t)
    t = re.sub(r"={2,}", " ", t)
    return t
UA = {"User-Agent":"CharFrequencyResearch/1.0 (personal research; contact via github.com/unicode)"}
cache="corpus3.json"
out = json.load(open(cache)) if os.path.exists(cache) else {}

def fetch(lang, tries=6):
    q = urllib.parse.urlencode({"action":"query","format":"json","generator":"random",
        "grnnamespace":"0","grnlimit":"20","prop":"extracts","explaintext":"1","exsectionformat":"plain","exlimit":"20"})
    url = "https://%s.wikipedia.org/w/api.php?%s" % (lang, q)
    delay = 3.0
    for _ in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)
            return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(delay); delay = min(delay*2, 40); continue
            return None
        except Exception:
            time.sleep(delay); delay = min(delay*2, 40)
    return None

for lang in WEIGHTS:
    if out.get(lang, {}).get("chars", 0) > 5000: continue
    counts = collections.Counter(); chars = 0
    for _ in range(3):
        d = fetch(lang)
        if not d: break
        for p in d.get("query",{}).get("pages",{}).values():
            t = clean(p.get("extract","")); counts.update(t); chars += len(t)
        time.sleep(2.5)
    if chars:
        out[lang] = {"chars":chars, "counts":{str(ord(k)):v for k,v in counts.items()}}
        json.dump(out, open(cache,"w"))
    print("%-3s %8d chars" % (lang, chars), file=sys.stderr, flush=True)
print("TOTAL", sum(v["chars"] for v in out.values()), "langs", len(out), file=sys.stderr)

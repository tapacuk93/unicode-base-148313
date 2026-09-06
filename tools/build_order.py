import json, re, collections, unicodedata as ud, os, sys

# ---------- the digit set ----------
alpha = [i for i in range(0x110000)
         if chr(i).isprintable() and not chr(i).isspace()
         and not ud.category(chr(i)).startswith('M')]
S = set(alpha)

# ---------- 1. corpus frequency, weighted by web content share ----------
WEIGHTS = json.loads(open("weights.json").read())
corpus = json.load(open("corpus3.json"))
freq = collections.Counter()
for lang, d in corpus.items():
    n = d["chars"]
    if not n: continue
    w = WEIGHTS.get(lang, 0.05) / n          # normalise per language, then weight
    for cp, c in d["counts"].items():
        freq[int(cp)] += c * w

# ---------- 2. Unicode script + block ----------
script = {}
for line in open("data/Scripts.txt"):
    line = line.split('#')[0].strip()
    if not line: continue
    rng, sc = [x.strip() for x in line.split(';')]
    a, _, b = rng.partition('..')
    a = int(a, 16); b = int(b, 16) if b else a
    for c in range(a, b+1):
        if c in S: script[c] = sc

# ---------- 3. emoji presentation order (Unicode emoji-test.txt) ----------
emoji_order = {}
k = 0
for line in open("data/emoji-test.txt"):
    if line.startswith('#') or ';' not in line: continue
    cps = line.split(';')[0].split()
    if len(cps) != 1: continue
    c = int(cps[0], 16)
    if c in S and c not in emoji_order:
        emoji_order[c] = k; k += 1

# ---------- 4. Unihan commonality ----------
iicore, core2020, documented = {}, {}, set()
for fn in os.listdir("data/unihan"):
    for line in open("data/unihan/"+fn, encoding="utf-8"):
        if not line.startswith("U+"): continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 3: continue
        c = int(f[0][2:], 16)
        if c not in S: continue
        if f[1] == "kIICore":      iicore[c] = len(re.sub(r'[^A-Z]', '', f[2]))
        elif f[1] == "kUnihanCore2020": core2020[c] = len(f[2].strip())
        elif f[1] in ("kMandarin", "kDefinition", "kCantonese", "kJapanese"): documented.add(c)

HISTORIC = {
 "Egyptian_Hieroglyphs","Anatolian_Hieroglyphs","Cuneiform","Linear_A","Linear_B","Old_Italic",
 "Gothic","Ugaritic","Old_Persian","Deseret","Shavian","Osmanya","Cypriot","Phoenician","Lydian",
 "Lycian","Carian","Kharoshthi","Brahmi","Avestan","Old_Turkic","Old_Hungarian","Old_Permic",
 "Old_North_Arabian","Old_South_Arabian","Old_Sogdian","Sogdian","Elbasan","Caucasian_Albanian",
 "Duployan","Tangut","Nushu","Khitan_Small_Script","Meroitic_Cursive","Meroitic_Hieroglyphs",
 "Palmyrene","Nabataean","Hatran","Manichaean","Psalter_Pahlavi","Inscriptional_Pahlavi",
 "Inscriptional_Parthian","Bamum","Mende_Kikakui","Bassa_Vah","Pahawh_Hmong","Modi","Ahom",
 "Marchen","Bhaiksuki","Zanabazar_Square","Soyombo","Dogra","Makasar","Medefaidrin","Elymaic",
 "Chorasmian","Dives_Akuru","Yezidi","Vithkuqi","Old_Uyghur","Tangsa","Toto","Cypro_Minoan",
 "Kawi","Nag_Mundari","Garay","Gurung_Khema","Kirat_Rai","Ol_Onal","Sunuwar","Todhri","Tulu_Tigalari",
 "Sharada","Siddham","Takri","Khojki","Khudawadi","Multani","Mahajani","Tirhuta","Newa","Grantha",
 "SignWriting","Glagolitic","Coptic","Runic","Ogham","Tai_Viet","Tai_Tham","Tai_Le","New_Tai_Lue",
 "Buginese","Rejang","Batak","Buhid","Hanunoo","Tagbanwa","Tagalog","Balinese","Javanese","Sundanese",
 "Lepcha","Limbu","Saurashtra","Kaithi","Chakma","Sora_Sompeng","Warang_Citi","Miao","Mro","Osage",
 "Adlam","Wancho","Nandinagari","Hanifi_Rohingya","Masaram_Gondi","Gunjala_Gondi","Nyiakeng_Puachue_Hmong",
}
# living-script rank, ordered by estimated number of users
LIVING = ["Latin","Arabic","Devanagari","Cyrillic","Bengali","Hiragana","Katakana","Hangul",
 "Greek","Hebrew","Thai","Tamil","Telugu","Gujarati","Kannada","Malayalam","Gurmukhi","Oriya",
 "Sinhala","Myanmar","Khmer","Lao","Georgian","Armenian","Ethiopic","Thaana","Tibetan",
 "Mongolian","Cherokee","Syriac","Bopomofo","Yi","Vai","Tifinagh","Nko","Canadian_Aboriginal"]
LR = {s: 10+i for i, s in enumerate(LIVING)}

SYMBOL_CATS = {"Sm","Sc","Sk","So","Pd","Ps","Pe","Pi","Pf","Pc","Po","Nd","Nl","No"}

def rank(c):
    ch = chr(c)
    sc = script.get(c, "Unknown")
    cat = ud.category(ch)
    if sc == "Han":
        if c in iicore:   return (2,  -iicore[c], c)
        if c in core2020: return (6,  -core2020[c], c)
        if c in documented: return (60, 0, c)
        return (900, 0, c)
    if c in emoji_order:  return (55, emoji_order[c], c)
    if sc in ("Common","Inherited"):
        return (50 if cat in SYMBOL_CATS else 52, 0, c)
    if sc in HISTORIC:    return (500, 0, c)
    return (LR.get(sc, 200), 0, c)

ASCII_SYM = [c for c in range(0x21, 0x7F) if not chr(c).isalnum()]

def key(c):
    ch = chr(c)
    if 0x30 <= c <= 0x39:            return (0, c - 0x30, 0, 0)          # 0-9
    if 0x41 <= c <= 0x5A:            return (1, c - 0x41, 0, 0)          # A-Z
    if 0x61 <= c <= 0x7A:            return (1, 26 + c - 0x61, 0, 0)     # a-z
    if c in ASCII_SYM:               return (2, -freq.get(c, 0), c, 0)   # ASCII punctuation
    if freq.get(c, 0) > 0:           return (3, -freq[c], c, 0)          # seen in corpus
    r = rank(c)
    return (4, r[0], r[1], r[2])

ordered = sorted(alpha, key=key)
json.dump(ordered, open("order.json", "w"))
print("ordered", len(ordered))
for i in list(range(0, 80)) + [100, 200, 500, 1000, 5000, 20000, 152307]:
    c = ordered[i]
    print("%7d  U+%05X  %s  %s" % (i, c, chr(c), ud.name(chr(c), "?")))

import json, collections

order = json.load(open("order.json")); alpha = [chr(c) for c in order]
d = json.load(open("omw.json")); langs = {k:set(v) for k,v in d["langs"].items()}; lem = d["lemmas"]
ranked = json.load(open("concept_order.json"))["ranked"]
CH = {s: alpha[i] for i, s in enumerate(ranked)}
RANK = {s: i for i, s in enumerate(ranked)}
def eng(s): return lem.get(s, {}).get("eng", "")

SHOW = ["eng","spa","fra","deu","ita","pol","rus","jpn","cmn","arb","heb","ind","fin","ell"]
LNAME = {"eng":"English","spa":"Spanish","fra":"French","deu":"German","ita":"Italian",
 "pol":"Polish","rus":"Russian","jpn":"Japanese","cmn":"Chinese","arb":"Arabic",
 "heb":"Hebrew","ind":"Indonesian","fin":"Finnish","ell":"Greek"}

SENT = ["02084071-n", "01170052-v", "14845743-n", "09415671-n"]     # dog drink water riverbed
CORE = ranked[:12]

out = ["# Worked examples", "",
 "Every character below stands for a **concept**, not an English word. The index",
 "of the character is the concept's rank among 107,662 concepts, ordered by how",
 "many of 1,060 languages have a word for it.", "",
 "## One character, many languages", "",
 "The twelve most universal concepts, and the word each language uses for them.", "",
 "| Char | Rank | Languages | " + " | ".join(LNAME[l] for l in ["eng","spa","fra","rus","jpn","cmn"]) + " |",
 "| :---: | ---: | ---: | " + " | ".join("---" for _ in range(6)) + " |"]
for s in CORE:
    row = [CH[s], str(RANK[s]), str(len(langs[s]))] + [lem.get(s, {}).get(l, "") for l in ["eng","spa","fra","rus","jpn","cmn"]]
    out.append("| " + " | ".join(row) + " |")

out += ["", "## The same sentence from ten languages", "",
 "A dog drinks water from the riverbed. Written in any of these languages, it",
 "encodes to the identical four characters, because the characters index",
 "concepts rather than spellings.", "",
 "| Language | Words | Encoded |", "| --- | --- | :---: |"]
enc = "".join(CH[s] for s in SENT)
for l in SHOW:
    ws = [lem.get(s, {}).get(l) for s in SENT]
    if not all(ws): continue
    out.append("| %s | %s | %s |" % (LNAME[l], " ".join(ws), enc))

out += ["", "## Reading order and importance order", "",
 "Concept rank doubles as an importance measure. A concept almost every language",
 "names is common ground and carries little information. A concept only a few",
 "languages name is specific and carries a lot. Sorting a sentence's characters",
 "by descending rank puts the most informative concept first.", "",
 "| Concept | Char | Rank | Languages |", "| --- | :---: | ---: | ---: |"]
for s in sorted(SENT, key=lambda s: -RANK[s]):
    out.append("| %s | %s | %d | %d |" % (eng(s), CH[s], RANK[s], len(langs[s])))
out += ["", "Reading order: `%s`" % enc,
        "", "Importance order: `%s`" % "".join(CH[s] for s in sorted(SENT, key=lambda s: -RANK[s])), "",
        "The importance form is not reversible. It says what the sentence is about,",
        "not what it said.", ""]
open("examples.md","w",encoding="utf-8").write("\n".join(out))
print("\n".join(out[:20]))

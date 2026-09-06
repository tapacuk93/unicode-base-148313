import json, unicodedata as ud
d = json.load(open("complexity.json"))
score = {int(k): v for k, v in d["score"].items()}
prov  = {int(k): v for k, v in d["prov"].items()}
S = set(score)                      # only characters that draw real ink

def key(c):
    if 0x30 <= c <= 0x39: return (0, c - 0x30, 0)
    if 0x41 <= c <= 0x5A: return (1, c - 0x41, 0)
    if 0x61 <= c <= 0x7A: return (1, 26 + c - 0x61, 0)
    return (2, score[c], c)

order = sorted(S, key=key)
json.dump(order, open("order.json", "w"))
print("base =", len(order))
print("\nsimplest 30 after the alphanumerics:")
for i in range(62, 92):
    c = order[i]
    print("  %4d  U+%05X  %s  %-42s  %.3f  %s" % (i, c, chr(c), ud.name(chr(c), "?")[:42], score[c], prov[c]))
print("\nmost complex 8:")
for i in range(len(order)-8, len(order)):
    c = order[i]
    print("  %6d  U+%05X  %s  %-40s  %.2f  %s" % (i, c, chr(c), ud.name(chr(c), "?")[:40], score[c], prov[c]))

import json, os, sys, unicodedata as ud
sys.set_int_max_str_digits(200000)
from mpmath import mp, mpf, pi, e, sqrt, log, euler, zeta, catalan, gamma

order = json.load(open("order.json"))
B = len(order)
alpha = [chr(c) for c in order]
NDIG = 1000
mp.dps = int(NDIG * 5.2) + 60

CONSTS = [
    ("pi",      lambda: +pi,                 "Archimedes' constant, the circle ratio"),
    ("tau",     lambda: 2 * pi,              "the full-turn constant, 2 pi"),
    ("e",       lambda: +e,                  "Euler's number, the base of natural logarithms"),
    ("phi",     lambda: (1 + sqrt(5)) / 2,   "the golden ratio"),
    ("sqrt2",   lambda: sqrt(2),             "Pythagoras' constant, the square root of 2"),
    ("sqrt3",   lambda: sqrt(3),             "Theodorus' constant, the square root of 3"),
    ("ln2",     lambda: log(2),              "the natural logarithm of 2"),
    ("gamma",   lambda: +euler,              "the Euler-Mascheroni constant"),
    ("zeta3",   lambda: zeta(3),             "Apery's constant, zeta(3)"),
    ("catalan", lambda: +catalan,            "Catalan's constant"),
]

os.makedirs("constants", exist_ok=True)
summary = []
for name, fn, desc in CONSTS:
    v = fn()
    ip = int(v)
    frac_s = mp.nstr(v - ip, mp.dps, strip_zeros=False).split(".")[1]
    scale = 10 ** len(frac_s)
    frac = int(frac_s)
    digits = []
    for _ in range(NDIG):
        frac *= B
        digits.append(frac // scale)
        frac %= scale
    body = alpha[ip] + "." + "".join(alpha[d] for d in digits)
    open("constants/%s.txt" % name, "w", encoding="utf-8").write(body + "\n")
    with open("constants/%s.tsv" % name, "w", encoding="utf-8") as f:
        f.write("position\tvalue\tcodepoint\tchar\n")
        f.write("0\t%d\tU+%04X\t%s\n" % (ip, order[ip], alpha[ip]))
        for i, d in enumerate(digits, 1):
            f.write("%d\t%d\tU+%04X\t%s\n" % (i, d, order[d], alpha[d]))
    summary.append((name, desc, alpha[ip], body[2:12]))
    print("%-8s int=%d  first10=%s" % (name, ip, body[2:12]))

with open("unicode-digits.tsv", "w", encoding="utf-8") as f:
    f.write("index\tcodepoint\tchar\tname\n")
    for i, c in enumerate(order):
        f.write("%d\tU+%04X\t%s\t%s\n" % (i, c, chr(c), ud.name(chr(c), "<unnamed>")))
json.dump(summary, open("summary.json", "w"))
print("base", B)

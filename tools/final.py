import json, unicodedata as ud

order = json.load(open("order.json"))
B = len(order)
alpha = [chr(c) for c in order]

with open("unicode-digits.tsv", "w", encoding="utf-8") as f:
    f.write("index\tcodepoint\tchar\tname\n")
    for i, c in enumerate(order):
        f.write("%d\tU+%04X\t%s\t%s\n" % (i, c, chr(c), ud.name(chr(c), "<unnamed>")))

def arccot(x, unity):
    total = term = unity // x
    n, sign = 1, -1
    x2 = x * x
    while term:
        term //= x2
        total += sign * (term // (2 * n + 1))
        n += 1
        sign = -sign
    return total

N = 5300
scale = 10 ** N
pi = 16 * arccot(5, scale) - 4 * arccot(239, scale)
ip = pi // scale
frac = pi - ip * scale

NDIG = 1000
digits = []
for _ in range(NDIG):
    frac *= B
    digits.append(frac // scale)
    frac %= scale

body = alpha[ip] + "." + "".join(alpha[d] for d in digits)
with open("pi.txt", "w", encoding="utf-8") as f:
    f.write(body + "\n")

with open("pi-digits.tsv", "w", encoding="utf-8") as f:
    f.write("position\tvalue\tcodepoint\tchar\n")
    f.write("0\t%d\tU+%04X\t%s\n" % (ip, order[ip], alpha[ip]))
    for i, d in enumerate(digits, 1):
        f.write("%d\t%d\tU+%04X\t%s\n" % (i, d, order[d], alpha[d]))
print("base", B, "int part", ip, "->", alpha[ip])
print("first 12 digit values:", digits[:12])
print("first 12 chars:", "".join(alpha[d] for d in digits[:12]))

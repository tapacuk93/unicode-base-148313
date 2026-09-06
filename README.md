# unicode-base-148313

Mathematical constants written in a positional numeral system whose digits are
Unicode characters, ordered from the simplest glyph to the most complex.

The base is **148313**. One digit carries about 17.2 bits, so the 1000 digits in
each file under `constants/` encode roughly 5200 decimal digits of the constant.

The repository name still says 152308, the base before glyph rendering was made
a requirement. The base is 148313.

## The digit set

A character is a digit if all four hold:

- `str.isprintable()` is true, which excludes the Unicode Other and Separator categories
- it is not whitespace
- its general category is not a combining mark (`Mn`, `Mc`, `Me`)
- **it draws ink in the installed font stack**

The last condition is the one that matters in practice. Every earlier version of
this set produced files full of tofu boxes, because Unicode assigns far more
characters than any font collection draws. A character qualifies only if some
installed font maps it to a glyph whose outline contains at least one point.
Blank glyphs, zero-width jamo fillers, and unmapped code points are all excluded
by the same test.

Combining marks are excluded so that every digit occupies its own cell. If they
were kept, a mark landing in the sequence would stack onto the preceding glyph
and the visible length would no longer match the digit count.

That leaves 148,313 characters, numbered 0 through 148312. `tools/verify.py`
re-checks every emitted file against the font stack and currently reports zero
unrenderable characters across all ten constants.

## Digit ordering

Indices are assigned by how simple the character is to draw.

| Range | Contents | Ordered by |
| --- | --- | --- |
| 0-9 | ASCII digits | numeric value |
| 10-35 | `A`-`Z` | alphabetical |
| 36-61 | `a`-`z` | alphabetical |
| 62-148312 | everything else | measured glyph complexity, ascending |

Because index 3 is the character `3`, pi's integer part still prints as `3`, and
the same holds for every constant here since all their integer parts are below 10.

### How complexity was measured

Each character's glyph outline is walked with a pen from `fontTools`, counting
on-curve and off-curve points plus two per closed contour. That count is the raw
complexity: a shape needing more control points is a more complicated drawing.

Fonts differ in how densely they place points, so a raw count is not comparable
across families. Each font's scores are divided by that font's own median glyph,
putting everything on a scale where 1.0 means "a typical glyph in the font this
character was measured in".

Characters are measured in the first font that has them, from a preference list
that starts with Noto Sans and the Noto symbol faces, then Noto CJK, then
BabelStone Han and Plangothic for the CJK extensions, then every other installed
font. Unifont is deliberately last: its outlines are traced from a bitmap, so its
point counts describe the tracing grid rather than the shape.

The result matches intuition at both ends. The simplest characters are small
marks such as `U+1802` MONGOLIAN COMMA. The most complex are the shade blocks
`U+2591` through `U+2593`, which are drawn as hundreds of separate small squares.

Per-character scores and the font each was measured in are in `complexity.tsv`.

## The first 100 digits of the index

Read in two column pairs: 0-49 on the left, 50-99 on the right.

| Index | Code point | Char | Name | Index | Code point | Char | Name |
| ---: | --- | :---: | --- | ---: | --- | :---: | --- |
| 0 | U+0030 | `0` | DIGIT ZERO | 50 | U+006F | `o` | LATIN SMALL LETTER O |
| 1 | U+0031 | `1` | DIGIT ONE | 51 | U+0070 | `p` | LATIN SMALL LETTER P |
| 2 | U+0032 | `2` | DIGIT TWO | 52 | U+0071 | `q` | LATIN SMALL LETTER Q |
| 3 | U+0033 | `3` | DIGIT THREE | 53 | U+0072 | `r` | LATIN SMALL LETTER R |
| 4 | U+0034 | `4` | DIGIT FOUR | 54 | U+0073 | `s` | LATIN SMALL LETTER S |
| 5 | U+0035 | `5` | DIGIT FIVE | 55 | U+0074 | `t` | LATIN SMALL LETTER T |
| 6 | U+0036 | `6` | DIGIT SIX | 56 | U+0075 | `u` | LATIN SMALL LETTER U |
| 7 | U+0037 | `7` | DIGIT SEVEN | 57 | U+0076 | `v` | LATIN SMALL LETTER V |
| 8 | U+0038 | `8` | DIGIT EIGHT | 58 | U+0077 | `w` | LATIN SMALL LETTER W |
| 9 | U+0039 | `9` | DIGIT NINE | 59 | U+0078 | `x` | LATIN SMALL LETTER X |
| 10 | U+0041 | `A` | LATIN CAPITAL LETTER A | 60 | U+0079 | `y` | LATIN SMALL LETTER Y |
| 11 | U+0042 | `B` | LATIN CAPITAL LETTER B | 61 | U+007A | `z` | LATIN SMALL LETTER Z |
| 12 | U+0043 | `C` | LATIN CAPITAL LETTER C | 62 | U+1802 | `᠂` | MONGOLIAN COMMA |
| 13 | U+0044 | `D` | LATIN CAPITAL LETTER D | 63 | U+2796 | `➖` | HEAVY MINUS SIGN |
| 14 | U+0045 | `E` | LATIN CAPITAL LETTER E | 64 | U+16FE2 | `𖿢` | OLD CHINESE HOOK MARK |
| 15 | U+0046 | `F` | LATIN CAPITAL LETTER F | 65 | U+17F2 | `៲` | KHMER SYMBOL LEK ATTAK PII |
| 16 | U+0047 | `G` | LATIN CAPITAL LETTER G | 66 | U+17F6 | `៶` | KHMER SYMBOL LEK ATTAK PRAM-MUOY |
| 17 | U+0048 | `H` | LATIN CAPITAL LETTER H | 67 | U+17F8 | `៸` | KHMER SYMBOL LEK ATTAK PRAM-BEI |
| 18 | U+0049 | `I` | LATIN CAPITAL LETTER I | 68 | U+133FA | `𓏺` | EGYPTIAN HIEROGLYPH Z015 |
| 19 | U+004A | `J` | LATIN CAPITAL LETTER J | 69 | U+13404 | `𓐄` | EGYPTIAN HIEROGLYPH Z016 |
| 20 | U+004B | `K` | LATIN CAPITAL LETTER K | 70 | U+1F1F1 | `🇱` | REGIONAL INDICATOR SYMBOL LETTER L |
| 21 | U+004C | `L` | LATIN CAPITAL LETTER L | 71 | U+0D4E | `ൎ` | MALAYALAM LETTER DOT REPH |
| 22 | U+004D | `M` | LATIN CAPITAL LETTER M | 72 | U+145B1 | `𔖱` | ANATOLIAN HIEROGLYPH A383 RA OR RI |
| 23 | U+004E | `N` | LATIN CAPITAL LETTER N | 73 | U+145C1 | `𔗁` | ANATOLIAN HIEROGLYPH A397 |
| 24 | U+004F | `O` | LATIN CAPITAL LETTER O | 74 | U+1F1F9 | `🇹` | REGIONAL INDICATOR SYMBOL LETTER T |
| 25 | U+0050 | `P` | LATIN CAPITAL LETTER P | 75 | U+1803 | `᠃` | MONGOLIAN FULL STOP |
| 26 | U+0051 | `Q` | LATIN CAPITAL LETTER Q | 76 | U+16FE3 | `𖿣` | OLD CHINESE ITERATION MARK |
| 27 | U+0052 | `R` | LATIN CAPITAL LETTER R | 77 | U+1CE07 | `𜸇` | TOP LEFT BLACK LEFT-POINTING SMALL TRIANGLE |
| 28 | U+0053 | `S` | LATIN CAPITAL LETTER S | 78 | U+1CE30 | `𜸰` | LARGE TYPE PIECE LOWER HALF VERTEX OF M |
| 29 | U+0054 | `T` | LATIN CAPITAL LETTER T | 79 | U+1CE31 | `𜸱` | LARGE TYPE PIECE UPPER HALF VERTEX OF W |
| 30 | U+0055 | `U` | LATIN CAPITAL LETTER U | 80 | U+1CEB3 | `𜺳` | BLACK RIGHT TRIANGLE CARET |
| 31 | U+0056 | `V` | LATIN CAPITAL LETTER V | 81 | U+1D9F5 | `𝧵` | SIGNWRITING DYNAMIC ARROWHEAD SMALL |
| 32 | U+0057 | `W` | LATIN CAPITAL LETTER W | 82 | U+1D9F6 | `𝧶` | SIGNWRITING DYNAMIC ARROWHEAD LARGE |
| 33 | U+0058 | `X` | LATIN CAPITAL LETTER X | 83 | U+17F1 | `៱` | KHMER SYMBOL LEK ATTAK MUOY |
| 34 | U+0059 | `Y` | LATIN CAPITAL LETTER Y | 84 | U+17F4 | `៴` | KHMER SYMBOL LEK ATTAK BUON |
| 35 | U+005A | `Z` | LATIN CAPITAL LETTER Z | 85 | U+1F1FE | `🇾` | REGIONAL INDICATOR SYMBOL LETTER Y |
| 36 | U+0061 | `a` | LATIN SMALL LETTER A | 86 | U+1F1EB | `🇫` | REGIONAL INDICATOR SYMBOL LETTER F |
| 37 | U+0062 | `b` | LATIN SMALL LETTER B | 87 | U+1F1FF | `🇿` | REGIONAL INDICATOR SYMBOL LETTER Z |
| 38 | U+0063 | `c` | LATIN SMALL LETTER C | 88 | U+18800 | `𘠀` | TANGUT COMPONENT-001 |
| 39 | U+0064 | `d` | LATIN SMALL LETTER D | 89 | U+18801 | `𘠁` | TANGUT COMPONENT-002 |
| 40 | U+0065 | `e` | LATIN SMALL LETTER E | 90 | U+18B01 | `𘬁` | KHITAN SMALL SCRIPT CHARACTER-18B01 |
| 41 | U+0066 | `f` | LATIN SMALL LETTER F | 91 | U+18B94 | `𘮔` | KHITAN SMALL SCRIPT CHARACTER-18B94 |
| 42 | U+0067 | `g` | LATIN SMALL LETTER G | 92 | U+0F0B | `་` | TIBETAN MARK INTERSYLLABIC TSHEG |
| 43 | U+0068 | `h` | LATIN SMALL LETTER H | 93 | U+0F0D | `།` | TIBETAN MARK SHAD |
| 44 | U+0069 | `i` | LATIN SMALL LETTER I | 94 | U+FE8D | `ﺍ` | ARABIC LETTER ALEF ISOLATED FORM |
| 45 | U+006A | `j` | LATIN SMALL LETTER J | 95 | U+105D2 | `𐗒` | TODHRI LETTER I |
| 46 | U+006B | `k` | LATIN SMALL LETTER K | 96 | U+10CA3 | `𐲣` | OLD HUNGARIAN CAPITAL LETTER SHORT ER |
| 47 | U+006C | `l` | LATIN SMALL LETTER L | 97 | U+10CA5 | `𐲥` | OLD HUNGARIAN CAPITAL LETTER ESZ |
| 48 | U+006D | `m` | LATIN SMALL LETTER M | 98 | U+10CE3 | `𐳣` | OLD HUNGARIAN SMALL LETTER SHORT ER |
| 49 | U+006E | `n` | LATIN SMALL LETTER N | 99 | U+10CE5 | `𐳥` | OLD HUNGARIAN SMALL LETTER ESZ |
The full index is in `unicode-digits.tsv`, one row per digit, with the four
columns unpaired.

## Constants

Each constant has a rendered `.txt` and a `.tsv` giving position, digit value,
code point, and character.

| Constant | What it is | Integer part | First five digits |
| --- | --- | :---: | --- |
| `pi` | Archimedes' constant, the circle ratio | `3` | 𫤫🯱쓔𬮐𢛤 |
| `tau` | the full-turn constant, 2 pi | `6` | 𣦢𠩎𤇥뭶𤁯 |
| `e` | Euler's number, the base of natural logarithms | `2` | 𗆖𧵱斻𨢘ஶ |
| `phi` | the golden ratio | `1` | 𧧒𪷙𮢷𑆤䷦ |
| `sqrt2` | Pythagoras' constant, the square root of 2 | `1` | 𱌪햼菊𧹯𫠁 |
| `sqrt3` | Theodorus' constant, the square root of 3 | `1` | 𨷂𣚻𠏡ꐻ䅃 |
| `ln2` | the natural logarithm of 2 | `0` | ᘧ𑆢煽醥𗶪 |
| `gamma` | the Euler-Mascheroni constant | `0` | 焳𬀒𓇢🗨ጾ |
| `zeta3` | Apery's constant, zeta(3) | `1` | 西㈱𛇑𔒝쐱 |
| `catalan` | Catalan's constant | `0` | 𭍊䄏걣톀ǵ |

## Files

| File | Contents |
| --- | --- |
| `constants/*.txt` | the constant in base 148313, 1000 fractional digits |
| `constants/*.tsv` | the same digits as position, value, code point, character |
| `unicode-digits.tsv` | the complete 148,313-entry digit index |
| `complexity.tsv` | per-digit complexity score and the font it was measured in |
| `tools/` | the scripts that build all of the above |

## What you need to install to read it

No single font can render this. OpenType glyph IDs are 16 bits, so one font file
holds at most 65,536 glyphs, and the digit set is more than twice that. You need
a stack, and a text editor that walks font fallback.

**The digit set is defined against the font stack below.** Install less and you
will see boxes; install these and every character in every file has a glyph.

| Font | Covers | Digits measured in it | How to install |
| --- | --- | ---: | --- |
| Plangothic P1 and P2 | CJK Ext B through I | 48671 | GitHub releases, `Plangothic_Project` |
| Noto Sans CJK | CJK base, Hangul, kana | 43641 | `brew install --cask font-noto-sans-cjk` |
| BabelStone Han | CJK Ext A through I | 31756 | `babelstone.co.uk`, direct TTF |
| GNU Unifont | rare BMP and Plane 1 leftovers | 968 | `unifoundry.com`, or `brew install --cask font-gnu-unifont` |

Plus the wider Noto set and the macOS system fonts for everything else:

```
brew install --cask font-noto-sans font-noto-serif-cjk \
  font-noto-sans-symbols font-noto-sans-symbols-2 font-noto-sans-math \
  font-noto-emoji font-noto-sans-egyptian-hieroglyphs \
  font-noto-sans-anatolian-hieroglyphs
```

The Homebrew cask for Unifont pulls from `ftpmirror.gnu.org`, which returned 504
during this build. The unifoundry mirror worked.

Egyptian Hieroglyphs Extended-A, `U+13460` to `U+143FF`, has no free font
coverage yet. Those characters are simply not in the digit set.

## Reproducing

```
pip install fonttools mpmath
python tools/complexity.py    # measures glyph complexity, preferred fonts first
python tools/complexity2.py   # sweeps every remaining installed font
python tools/order2.py        # writes order.json
python tools/final2.py        # writes constants/ and unicode-digits.tsv
python tools/verify.py        # confirms every emitted character has a glyph
```

The base is a function of what is installed. Run this on a machine with a
different font set and you get a different, smaller or larger, base.

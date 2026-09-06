# unicode-base-148313

A positional numeral system whose digits are Unicode characters, ordered by how
commonly each character is used. Base **148313**.

Two things are written in it here. Ten mathematical constants, under
`constants/`, each to 1000 digits, which is about 5200 decimal digits. And
sentences, where each *concept* is written as the single digit whose index
equals how universal that concept is across the world's languages.

## The digit set

A character is a digit if all four hold:

- `str.isprintable()` is true, which excludes the Unicode Other and Separator categories
- it is not whitespace
- its general category is not a combining mark (`Mn`, `Mc`, `Me`)
- **it draws ink in the installed font stack**

The last condition is the one that matters in practice. Unicode assigns far more
characters than any font collection draws, and earlier versions of this set
produced files full of tofu boxes. A character qualifies only if some installed
font maps it to a glyph whose outline contains at least one point. Blank glyphs,
zero-width jamo fillers, and unmapped code points all fail the same test.

Combining marks are excluded so that every digit occupies its own cell.

That leaves 148,313 characters, numbered 0 through 148312. `tools/verify.py`
re-checks every emitted file against the font stack and reports zero
unrenderable characters.

## Digit ordering

Index 0 is the most commonly used character in the set, and the ranking runs
from there. No range is reserved: the ASCII digits and letters land wherever
their frequency puts them, which is why index 0 is `e`, not `0`.

### How frequency was measured

Plain-text extracts were pulled from Wikipedia across 44 languages chosen to
cover the major writing systems, about 700,000 characters in total. Section
markers and LaTeX math blocks are stripped, because an early pass without that
filter ranked `=` above `.` and `,` purely from `== Heading ==` markup.

Each language's counts are normalised by its own sample size and then weighted by
that language's approximate share of web content, so English dominates without
erasing the rest. Weights are in `tools/weights.json`, raw counts in
`data/corpus3.json`.

Only 2,964 characters appear in a sample that size. The rest, which is almost all
of the set, falls back to a structural ranking:

- Han ideographs rank by Unihan commonality, using `kIICore` first, then
  `kUnihanCore2020`, then whether the character has a reading or definition at
  all. Rare extension ideographs land at the very bottom.
- Other characters rank by whether their script is in living use, with historic
  and liturgical scripts below symbols and emoji.
- Emoji follow the order in Unicode's `emoji-test.txt`.
- Ties break by code point.

`complexity.tsv` carries a separate per-character measurement, the glyph outline
complexity used to decide renderability. It no longer drives the ordering.

## The first 100 digits of the index

Read in two column pairs: 0-49 on the left, 50-99 on the right.

| Index | Code point | Char | Name | Index | Code point | Char | Name |
| ---: | --- | :---: | --- | ---: | --- | :---: | --- |
| 0 | U+0065 | `e` | LATIN SMALL LETTER E | 50 | U+0440 | `р` | CYRILLIC SMALL LETTER ER |
| 1 | U+0061 | `a` | LATIN SMALL LETTER A | 51 | U+0052 | `R` | LATIN CAPITAL LETTER R |
| 2 | U+006E | `n` | LATIN SMALL LETTER N | 52 | U+0442 | `т` | CYRILLIC SMALL LETTER TE |
| 3 | U+0069 | `i` | LATIN SMALL LETTER I | 53 | U+0022 | `"` | QUOTATION MARK |
| 4 | U+006F | `o` | LATIN SMALL LETTER O | 54 | U+0044 | `D` | LATIN CAPITAL LETTER D |
| 5 | U+0072 | `r` | LATIN SMALL LETTER R | 55 | U+0046 | `F` | LATIN CAPITAL LETTER F |
| 6 | U+0074 | `t` | LATIN SMALL LETTER T | 56 | U+0048 | `H` | LATIN CAPITAL LETTER H |
| 7 | U+0073 | `s` | LATIN SMALL LETTER S | 57 | U+0034 | `4` | DIGIT FOUR |
| 8 | U+006C | `l` | LATIN SMALL LETTER L | 58 | U+0441 | `с` | CYRILLIC SMALL LETTER ES |
| 9 | U+0064 | `d` | LATIN SMALL LETTER D | 59 | U+004C | `L` | LATIN CAPITAL LETTER L |
| 10 | U+0063 | `c` | LATIN SMALL LETTER C | 60 | U+0038 | `8` | DIGIT EIGHT |
| 11 | U+0075 | `u` | LATIN SMALL LETTER U | 61 | U+0035 | `5` | DIGIT FIVE |
| 12 | U+0068 | `h` | LATIN SMALL LETTER H | 62 | U+0057 | `W` | LATIN CAPITAL LETTER W |
| 13 | U+006D | `m` | LATIN SMALL LETTER M | 63 | U+0432 | `в` | CYRILLIC SMALL LETTER VE |
| 14 | U+0070 | `p` | LATIN SMALL LETTER P | 64 | U+5E74 | `年` | CJK UNIFIED IDEOGRAPH-5E74 |
| 15 | U+0067 | `g` | LATIN SMALL LETTER G | 65 | U+043B | `л` | CYRILLIC SMALL LETTER EL |
| 16 | U+0066 | `f` | LATIN SMALL LETTER F | 66 | U+00E9 | `é` | LATIN SMALL LETTER E WITH ACUTE |
| 17 | U+002E | `.` | FULL STOP | 67 | U+0036 | `6` | DIGIT SIX |
| 18 | U+0062 | `b` | LATIN SMALL LETTER B | 68 | U+0047 | `G` | LATIN CAPITAL LETTER G |
| 19 | U+002C | `,` | COMMA | 69 | U+043A | `к` | CYRILLIC SMALL LETTER KA |
| 20 | U+0076 | `v` | LATIN SMALL LETTER V | 70 | U+004E | `N` | LATIN CAPITAL LETTER N |
| 21 | U+0079 | `y` | LATIN SMALL LETTER Y | 71 | U+0646 | `ن` | ARABIC LETTER NOON |
| 22 | U+006B | `k` | LATIN SMALL LETTER K | 72 | U+0078 | `x` | LATIN SMALL LETTER X |
| 23 | U+0031 | `1` | DIGIT ONE | 73 | U+0631 | `ر` | ARABIC LETTER REH |
| 24 | U+0077 | `w` | LATIN SMALL LETTER W | 74 | U+7DDA | `線` | CJK UNIFIED IDEOGRAPH-7DDA |
| 25 | U+0032 | `2` | DIGIT TWO | 75 | U+06CC | `ی` | ARABIC LETTER FARSI YEH |
| 26 | U+0030 | `0` | DIGIT ZERO | 76 | U+003A | `:` | COLON |
| 27 | U+0045 | `E` | LATIN CAPITAL LETTER E | 77 | U+0056 | `V` | LATIN CAPITAL LETTER V |
| 28 | U+0053 | `S` | LATIN CAPITAL LETTER S | 78 | U+0027 | `'` | APOSTROPHE |
| 29 | U+0039 | `9` | DIGIT NINE | 79 | U+004F | `O` | LATIN CAPITAL LETTER O |
| 30 | U+0041 | `A` | LATIN CAPITAL LETTER A | 80 | U+0434 | `д` | CYRILLIC SMALL LETTER DE |
| 31 | U+043E | `о` | CYRILLIC SMALL LETTER O | 81 | U+0648 | `و` | ARABIC LETTER WAW |
| 32 | U+0430 | `а` | CYRILLIC SMALL LETTER A | 82 | U+043C | `м` | CYRILLIC SMALL LETTER EM |
| 33 | U+0043 | `C` | LATIN CAPITAL LETTER C | 83 | U+0443 | `у` | CYRILLIC SMALL LETTER U |
| 34 | U+0438 | `и` | CYRILLIC SMALL LETTER I | 84 | U+0645 | `م` | ARABIC LETTER MEEM |
| 35 | U+0435 | `е` | CYRILLIC SMALL LETTER IE | 85 | U+2013 | `–` | EN DASH |
| 36 | U+0054 | `T` | LATIN CAPITAL LETTER T | 86 | U+062A | `ت` | ARABIC LETTER TEH |
| 37 | U+043D | `н` | CYRILLIC SMALL LETTER EN | 87 | U+0644 | `ل` | ARABIC LETTER LAM |
| 38 | U+007A | `z` | LATIN SMALL LETTER Z | 88 | U+004B | `K` | LATIN CAPITAL LETTER K |
| 39 | U+002D | `-` | HYPHEN-MINUS | 89 | U+FF08 | `（` | FULLWIDTH LEFT PARENTHESIS |
| 40 | U+0042 | `B` | LATIN CAPITAL LETTER B | 90 | U+FF09 | `）` | FULLWIDTH RIGHT PARENTHESIS |
| 41 | U+0028 | `(` | LEFT PARENTHESIS | 91 | U+062F | `د` | ARABIC LETTER DAL |
| 42 | U+0029 | `)` | RIGHT PARENTHESIS | 92 | U+043F | `п` | CYRILLIC SMALL LETTER PE |
| 43 | U+004D | `M` | LATIN CAPITAL LETTER M | 93 | U+5C71 | `山` | CJK UNIFIED IDEOGRAPH-5C71 |
| 44 | U+0050 | `P` | LATIN CAPITAL LETTER P | 94 | U+004A | `J` | LATIN CAPITAL LETTER J |
| 45 | U+0627 | `ا` | ARABIC LETTER ALEF | 95 | U+9053 | `道` | CJK UNIFIED IDEOGRAPH-9053 |
| 46 | U+0049 | `I` | LATIN CAPITAL LETTER I | 96 | U+0071 | `q` | LATIN SMALL LETTER Q |
| 47 | U+0037 | `7` | DIGIT SEVEN | 97 | U+3001 | `、` | IDEOGRAPHIC COMMA |
| 48 | U+0033 | `3` | DIGIT THREE | 98 | U+306E | `の` | HIRAGANA LETTER NO |
| 49 | U+006A | `j` | LATIN SMALL LETTER J | 99 | U+3002 | `。` | IDEOGRAPHIC FULL STOP |
The full index is in `unicode-digits.tsv`, one row per digit, with the four
columns unpaired.

## Concepts

`concepts.tsv` maps concepts, not English words, onto the digits. A concept is a
WordNet synset, and its rank is how many of 1,060 languages have a word for it,
counted from the Open Multilingual WordNet together with the Wiktionary and CLDR
translation sets. 107,662 concepts are ranked, so the dictionary is smaller than
the base and stops before the digits run out.

The top of the list is what you would expect of shared human vocabulary.

| Rank | Char | Languages | Concept |
| ---: | :---: | ---: | --- |
| 0 | `e` | 387 | dog |
| 1 | `a` | 373 | water |
| 2 | `n` | 344 | fish |
| 3 | `i` | 246 | butterfly |
| 4 | `o` | 231 | bee |
| 5 | `r` | 226 | horse |
| 6 | `t` | 223 | tree |

Because the index is language-independent, a sentence written in any of these
languages encodes to the identical string. `examples.md` carries a four-concept
sentence in the nine languages that have a word for every concept in it,
including Russian, Japanese and Chinese.

Rank also measures importance. A concept nearly every language names is common
ground and carries little information. A concept few languages name is specific
and carries a lot. Sorting a sentence by descending rank puts its most
informative concept first. That form is not reversible: it says what the
sentence is about, not what it said.

Words shown for each language are the shortest curated lemma, which is
occasionally a synonym or an abbreviation rather than the citation form.

## Constants

Each constant has a rendered `.txt` and a `.tsv` giving position, digit value,
code point, and character.

| Constant | What it is | Integer digit | First five digits |
| --- | --- | :---: | --- |
| `pi` | Archimedes' constant, the circle ratio | `i` | 𡷹撥惢𑄼𣨂 |
| `tau` | the full-turn constant, 2 pi | `t` | ᙿ搁꺳⸟𭻑 |
| `e` | Euler's number, the base of natural logarithms | `n` | 𘆗𧰱𡀭𑥐骾 |
| `phi` | the golden ratio | `a` | 𱟫𤟿𛉔虐𨴳 |
| `sqrt2` | Pythagoras' constant, the square root of 2 | `a` | 𠩆ൔ𢀹𪻲𡋿 |
| `sqrt3` | Theodorus' constant, the square root of 3 | `a` | 𘦙𑉀𥨠퉥𠽛 |
| `ln2` | the natural logarithm of 2 | `e` | 𗌇𛅼𭋶𭲙𭸑 |
| `gamma` | the Euler-Mascheroni constant | `e` | 𪈒𫍱ﺖ䄝뜴 |
| `zeta3` | Apery's constant, zeta(3) | `a` | 몃𒌞躄𭞶𤏠 |
| `catalan` | Catalan's constant | `e` | 𭨙𮇤𣥌咶𮍜 |

Every constant here has an integer part below 10, so the character before the
point is just that small index: `i` is 3, and `t` is 6.

## Files

| File | Contents |
| --- | --- |
| `constants/*.txt` | the constant in base 148313, 1000 fractional digits |
| `constants/*.tsv` | the same digits as position, value, code point, character |
| `concepts.tsv` | concept, rank, digit, and how many languages name it |
| `examples.md` | one sentence encoded from thirteen languages |
| `unicode-digits.tsv` | the complete 148,313-entry digit index |
| `complexity.tsv` | per-digit glyph complexity and the font it was measured in |
| `tools/` | the scripts that build all of the above |
| `data/corpus3.json` | raw character counts from the Wikipedia sample |

## What you need to install to read it

No single font can render this. OpenType glyph IDs are 16 bits, so one font file
holds at most 65,536 glyphs, and the digit set is more than twice that. You need
a stack, and an application that walks font fallback.

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

Restart the application after installing. Safari and other WebKit views build
their font fallback list once per process and will not pick up fonts activated
afterward.

Egyptian Hieroglyphs Extended-A, `U+13460` to `U+143FF`, has no free font
coverage yet. Those characters are simply not in the digit set.

## Known issue

The base includes 26 regional indicator symbols. Two of them adjacent in a
string merge into a single flag emoji, which would collapse two digits into one
cell. No current file contains an adjacent pair. Dropping them would cost 26
characters and close it.

## Reproducing

```
pip install fonttools mpmath
python tools/complexity.py    # measures glyph complexity, preferred fonts first
python tools/complexity2.py   # sweeps every remaining installed font
python tools/corpus3.py       # samples Wikipedia across 44 languages
python tools/corpus4.py       # deepens the major-script languages
python tools/order3.py        # writes order.json
python tools/final3.py        # writes constants/ and unicode-digits.tsv
python tools/concepts.py      # counts languages per concept
python tools/concepts2.py     # writes concepts.tsv
python tools/examples.py      # writes examples.md
python tools/verify.py        # confirms every emitted character has a glyph
```

`order3.py` also expects `Scripts.txt`, `emoji-test.txt` and the Unihan database
under `data/`, all from `unicode.org`, and `concepts.py` expects the NLTK
corpora `wordnet`, `omw-1.4` and `extended_omw`, unzipped.

The base is a function of what is installed. Run this on a machine with a
different font set and you get a different base.

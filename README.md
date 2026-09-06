# unicode-base-152308

Pi written in a positional numeral system whose digits are Unicode characters.

The base is **152308**. One digit carries about 17.2 bits, so the 1000 digits in
`pi.txt` encode roughly 5250 decimal digits of pi.

## The digit set

A character is a digit if all three hold:

- `str.isprintable()` is true, which excludes the Unicode Other and Separator categories
- it is not whitespace
- its general category is not a combining mark (`Mn`, `Mc`, `Me`)

Marks are excluded so that every digit occupies its own cell. If they were kept,
a mark landing in the sequence would stack onto the preceding glyph and the
visible length would no longer match the digit count.

That leaves 152,308 characters, numbered 0 through 152307.

## Digit ordering

Indices are assigned by how commonly the character is used, not by code point.

| Range | Contents | Ordered by |
| --- | --- | --- |
| 0-9 | ASCII digits | numeric value |
| 10-35 | `A`-`Z` | alphabetical |
| 36-61 | `a`-`z` | alphabetical |
| 62-93 | ASCII punctuation and symbols | measured frequency |
| 94-~2000 | everything else seen in the corpus | measured frequency |
| rest | everything unseen | script and Unihan commonality, then code point |

Because index 3 is the character `3`, pi's integer part still prints as `3`.

### How frequency was measured

Plain-text extracts were pulled from Wikipedia across 44 languages chosen to
cover the major writing systems. Section markers and LaTeX math blocks were
stripped, because an earlier pass without that filter ranked `=` above `.` and
`,` purely from `== Heading ==` markup.

Each language's counts are normalised by its own sample size and then weighted
by that language's approximate share of web content, so English dominates but
does not erase the rest. The weights are in `tools/weights.json` and the raw
counts in `data/corpus3.json`.

Characters that never appeared in the sample, which is most of the set, fall
back to a structural ranking:

- Han ideographs are ranked by Unihan commonality, using `kIICore` first, then
  `kUnihanCore2020`, then whether the character has a reading or definition at
  all. Rare extension ideographs land at the very bottom.
- Other characters are ranked by whether their script is in living use, with
  historic and liturgical scripts placed below symbols and emoji.
- Emoji follow the order in Unicode's `emoji-test.txt`.
- Ties break by code point.

## The first 100 digits of the index

| Index | Code point | Character | Name |
| ---: | --- | :---: | --- |
| 0 | U+0030 | `0` | DIGIT ZERO |
| 1 | U+0031 | `1` | DIGIT ONE |
| 2 | U+0032 | `2` | DIGIT TWO |
| 3 | U+0033 | `3` | DIGIT THREE |
| 4 | U+0034 | `4` | DIGIT FOUR |
| 5 | U+0035 | `5` | DIGIT FIVE |
| 6 | U+0036 | `6` | DIGIT SIX |
| 7 | U+0037 | `7` | DIGIT SEVEN |
| 8 | U+0038 | `8` | DIGIT EIGHT |
| 9 | U+0039 | `9` | DIGIT NINE |
| 10 | U+0041 | `A` | LATIN CAPITAL LETTER A |
| 11 | U+0042 | `B` | LATIN CAPITAL LETTER B |
| 12 | U+0043 | `C` | LATIN CAPITAL LETTER C |
| 13 | U+0044 | `D` | LATIN CAPITAL LETTER D |
| 14 | U+0045 | `E` | LATIN CAPITAL LETTER E |
| 15 | U+0046 | `F` | LATIN CAPITAL LETTER F |
| 16 | U+0047 | `G` | LATIN CAPITAL LETTER G |
| 17 | U+0048 | `H` | LATIN CAPITAL LETTER H |
| 18 | U+0049 | `I` | LATIN CAPITAL LETTER I |
| 19 | U+004A | `J` | LATIN CAPITAL LETTER J |
| 20 | U+004B | `K` | LATIN CAPITAL LETTER K |
| 21 | U+004C | `L` | LATIN CAPITAL LETTER L |
| 22 | U+004D | `M` | LATIN CAPITAL LETTER M |
| 23 | U+004E | `N` | LATIN CAPITAL LETTER N |
| 24 | U+004F | `O` | LATIN CAPITAL LETTER O |
| 25 | U+0050 | `P` | LATIN CAPITAL LETTER P |
| 26 | U+0051 | `Q` | LATIN CAPITAL LETTER Q |
| 27 | U+0052 | `R` | LATIN CAPITAL LETTER R |
| 28 | U+0053 | `S` | LATIN CAPITAL LETTER S |
| 29 | U+0054 | `T` | LATIN CAPITAL LETTER T |
| 30 | U+0055 | `U` | LATIN CAPITAL LETTER U |
| 31 | U+0056 | `V` | LATIN CAPITAL LETTER V |
| 32 | U+0057 | `W` | LATIN CAPITAL LETTER W |
| 33 | U+0058 | `X` | LATIN CAPITAL LETTER X |
| 34 | U+0059 | `Y` | LATIN CAPITAL LETTER Y |
| 35 | U+005A | `Z` | LATIN CAPITAL LETTER Z |
| 36 | U+0061 | `a` | LATIN SMALL LETTER A |
| 37 | U+0062 | `b` | LATIN SMALL LETTER B |
| 38 | U+0063 | `c` | LATIN SMALL LETTER C |
| 39 | U+0064 | `d` | LATIN SMALL LETTER D |
| 40 | U+0065 | `e` | LATIN SMALL LETTER E |
| 41 | U+0066 | `f` | LATIN SMALL LETTER F |
| 42 | U+0067 | `g` | LATIN SMALL LETTER G |
| 43 | U+0068 | `h` | LATIN SMALL LETTER H |
| 44 | U+0069 | `i` | LATIN SMALL LETTER I |
| 45 | U+006A | `j` | LATIN SMALL LETTER J |
| 46 | U+006B | `k` | LATIN SMALL LETTER K |
| 47 | U+006C | `l` | LATIN SMALL LETTER L |
| 48 | U+006D | `m` | LATIN SMALL LETTER M |
| 49 | U+006E | `n` | LATIN SMALL LETTER N |
| 50 | U+006F | `o` | LATIN SMALL LETTER O |
| 51 | U+0070 | `p` | LATIN SMALL LETTER P |
| 52 | U+0071 | `q` | LATIN SMALL LETTER Q |
| 53 | U+0072 | `r` | LATIN SMALL LETTER R |
| 54 | U+0073 | `s` | LATIN SMALL LETTER S |
| 55 | U+0074 | `t` | LATIN SMALL LETTER T |
| 56 | U+0075 | `u` | LATIN SMALL LETTER U |
| 57 | U+0076 | `v` | LATIN SMALL LETTER V |
| 58 | U+0077 | `w` | LATIN SMALL LETTER W |
| 59 | U+0078 | `x` | LATIN SMALL LETTER X |
| 60 | U+0079 | `y` | LATIN SMALL LETTER Y |
| 61 | U+007A | `z` | LATIN SMALL LETTER Z |
| 62 | U+002C | `,` | COMMA |
| 63 | U+002E | `.` | FULL STOP |
| 64 | U+002D | `-` | HYPHEN-MINUS |
| 65 | U+0028 | `(` | LEFT PARENTHESIS |
| 66 | U+0029 | `)` | RIGHT PARENTHESIS |
| 67 | U+002F | `/` | SOLIDUS |
| 68 | U+003A | `:` | COLON |
| 69 | U+0022 | `"` | QUOTATION MARK |
| 70 | U+0027 | `'` | APOSTROPHE |
| 71 | U+003D | `=` | EQUALS SIGN |
| 72 | U+003B | `;` | SEMICOLON |
| 73 | U+0021 | `!` | EXCLAMATION MARK |
| 74 | U+003F | `?` | QUESTION MARK |
| 75 | U+003E | `>` | GREATER-THAN SIGN |
| 76 | U+005B | `[` | LEFT SQUARE BRACKET |
| 77 | U+005D | `]` | RIGHT SQUARE BRACKET |
| 78 | U+002B | `+` | PLUS SIGN |
| 79 | U+0026 | `&` | AMPERSAND |
| 80 | U+007C | `\|` | VERTICAL LINE |
| 81 | U+005F | `_` | LOW LINE |
| 82 | U+005C | `\` | REVERSE SOLIDUS |
| 83 | U+002A | `*` | ASTERISK |
| 84 | U+0025 | `%` | PERCENT SIGN |
| 85 | U+007E | `~` | TILDE |
| 86 | U+0023 | `#` | NUMBER SIGN |
| 87 | U+0060 | ``` | GRAVE ACCENT |
| 88 | U+007B | `{` | LEFT CURLY BRACKET |
| 89 | U+007D | `}` | RIGHT CURLY BRACKET |
| 90 | U+0024 | `$` | DOLLAR SIGN |
| 91 | U+003C | `<` | LESS-THAN SIGN |
| 92 | U+0040 | `@` | COMMERCIAL AT |
| 93 | U+005E | `^` | CIRCUMFLEX ACCENT |
| 94 | U+043E | `о` | CYRILLIC SMALL LETTER O |
| 95 | U+0438 | `и` | CYRILLIC SMALL LETTER I |
| 96 | U+0430 | `а` | CYRILLIC SMALL LETTER A |
| 97 | U+0435 | `е` | CYRILLIC SMALL LETTER IE |
| 98 | U+0627 | `ا` | ARABIC LETTER ALEF |
| 99 | U+043D | `н` | CYRILLIC SMALL LETTER EN |
The full index is in `unicode-digits.tsv`, one row per digit, same four columns.

## Files

| File | Contents |
| --- | --- |
| `pi.txt` | pi in base 152308, 1000 fractional digits |
| `pi-digits.tsv` | the same digits as position, value, code point, character |
| `unicode-digits.tsv` | the complete 152,308-entry digit index |
| `font-coverage.txt` | which installed fonts render which digits |
| `tools/` | the scripts that build all of the above |
| `data/corpus3.json` | raw character counts from the Wikipedia sample |

## What you need to install to read it

No single font can render this. OpenType glyph IDs are 16 bits, so one font file
holds at most 65,536 glyphs, and the digit set is more than twice that. You need
a stack, and a text editor that walks font fallback.

A stock macOS install renders less than half of it. These are the fonts that
close the gap, measured against the 1000 digits in `pi.txt`.

| Font | Covers | Digits it renders | How to install |
| --- | --- | ---: | --- |
| Plangothic P1 and P2 | CJK Ext B through I | 654 | GitHub releases, `Plangothic_Project` |
| BabelStone Han | CJK Ext A through I | 400 | `babelstone.co.uk`, direct TTF |
| GNU Unifont | all of the BMP, bitmap style | 337 | `unifoundry.com`, or `brew install --cask font-gnu-unifont` |
| Noto Sans and Noto CJK | Latin, Greek, Cyrillic, Indic, CJK base | 267 | `brew install --cask font-noto-sans font-noto-sans-cjk font-noto-serif-cjk` |

The Homebrew cask for Unifont pulls from `ftpmirror.gnu.org`, which returned 504
during this build. The unifoundry mirror worked.

Also useful for the symbol and historic-script digits:

```
brew install --cask font-noto-sans-symbols font-noto-sans-symbols-2 \
  font-noto-sans-math font-noto-emoji \
  font-noto-sans-egyptian-hieroglyphs font-noto-sans-anatolian-hieroglyphs
```

### Known gap

With all of the above installed, 27 of the 1000 digits still have no glyph. Every
one is in Egyptian Hieroglyphs Extended-A, `U+13460` to `U+143FF`, added in
Unicode 16.0. No free font covers that block yet. Across the whole digit set the
coverage is 148,313 of 152,308, or 97.4 percent.

## Reproducing

```
pip install fonttools
python tools/corpus3.py      # samples Wikipedia, writes corpus3.json
python tools/build_order.py  # writes order.json
python tools/final.py        # writes pi.txt, pi-digits.tsv, unicode-digits.tsv
python tools/cover2.py       # writes font-coverage.txt
```

`build_order.py` also expects `Scripts.txt`, `emoji-test.txt` and the Unihan
database under `data/`, all from `unicode.org`.

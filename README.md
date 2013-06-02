# Names for all(!) numbers

One for the category 'senseless knowledge': every number, regardless of its size, has a name.

To jump into action, `./say.py --help` and `--example` are your friends (or jump to section usage).
If you want to understand the full thing, this is how it works:

## 1-999 999
We need simple definitions for the first ones (one, two, three…). Most languages have some exceptions for small numbers,
but nothing interesting here. I guess you know how to count :-)

### 1 000 000 and above
There are two systems, building the names of large numbers. The difference between them is very simple.
Both are using the same algorithm, slightly modified. The lib covers both of them.

#### Short scale; used in the UK and the USA
A new word is build, for every 3 zeros.

| Number        | Name           |
| ------------- |:-------------:|
| 1.000.000      | million |
| 1.000.000.000      | billion      |
| 1.000.000.000.000 | trillion      |

#### Long scale; used in most parts of Europe
Every word is reused, with the postfix `lliard` to indicate 3 more zeros. This is, why the long scale system does need a
new word every 6 zeros.

| Number        | Name           |
| ------------- |:-------------:|
| 1.000.000      | million |
| 1.000.000.000      | milliard      |
| 1.000.000.000.000 | billion      |
| 1.000.000.000.000.000 | billiard      |
| 1.000.000.000.000.000.000 | trillion      |

#### Summarized
Both systems starting with `million` as word for 6 zeros (to be precisely: `mi` is the 'word' and `llion` just the
postfix to make it one). The algorithm to build new words is the same, but short scale
use it every 3 zeros, while long scale does it every 6.

### Building new words
The first 999 words are simple the Latin names for 1 to 999. I do not cover the rules to build latin names here,
but you will have no problem, finding these information. A good (german) article is
[this](http://de.wikipedia.org/wiki/Zahlennamen) one (wikipedia); or simply read the code :-)
Find a table for all 999 names at the end of this doc.

That was simple. Both systems take the Latin names for 1 to 999 to create new words for numbers. Short scale takes a
new word all 3 digits, appending llion. Long scale takes a new word all 6 digits, appending llion or lliard.
One exception: if the latin number is > 9 and < 100 and ends with an 'a', it is replaced with an 'i', before appending llion or lliard.
Some examples:

| Zeros | Short scale(us) |  Latin number | Long scale (eu) |  Latin number |
| ------------- |:-------------:| :-------------:|:-------------:|:-------------:|
| 6 | million | 1 | million | 1 |
| 9 | billion | 2 | milliard | 1 |
| 12 | trillion | 3 | billion | 2 |
| 15 | quadrillion | 4 | billiard | 2 |
| 18 | quintillion | 5 | trillion | 3 |
| 21 | sextillion | 6 | trilliard | 3 |
| 99 | duotrigintillion | 32 | sedezilliarde | 16 |
| 300 | novenonagintillion | 99 | quinquagintillion | 50 |
| 1011 | sestrigintatrecentillion | 336 | oktosexagintazentilliarde | 168 |
| 3000 | novenonagintanongentillion | 999 | quingentillion | 500 |


Short scale would not be able to generate a new word for the number with 3003 digits (long scale has the same problem
with 6000). To create more words, following algorithm is used: The Latin number is divided into blocks of thousands.
For every block (which is a number from 000-999), we take the latin name and put `lli` between them. If the block contains
only zeros, `ni` is used.

3003 zeros in short scale, needs Latin number 1000. Splitted into blocks: 1_000. Latin for 1 is `mi`, so the full name is
`mi-lli-ni-llion` (which is the number with 6000 zeros in long scale).

Some more advanced examples (the `-` delimiter are not part of the 'real' name):

| Zeros | Short scale(us) |  Latin number | Long scale (eu) |  Latin number |
| ------------- |:-------------:| :-------------:|:-------------:|:-------------:|
| 100011 | trestriginti-lli-sestrigintatrecenti-llion | 33 336 | sedezi-lli-oktosexagintaseszenti-lliarde | 16 668 |
| 987654321 | novemvigintitrecenti-lli-oktodeciducenti-lli-sexcenti-llion | 329 218 106 | quattuorsexagintazenti-lli-novenseszenti-lli-tresquinquaginti-lliarde | 164 609 53 |


## Usage
to see all examples: ./say.py --example

say.py does also show, how to use the lib. Public functions are `say` and `sayByExp`. To see everything in action, use following
arguments. Simplest call: ./say.py 94283203948239048209482409283490...2840923432 (--shortScale, if you want the us/uk style)

<pre>
usage: say.py [-T] [-A] [-H] [-E] [-S] [-M] [-U] [-G] [-GG] [-GGG] [-h] [-e]
              [-SL] [-v] [-c] [-C] [-s] [-ch] [-n] [-N | -sy] [-f] [-u] [-b]
              [-l] [-g] [-d [DELIMITER]] [-L LOCALE] [-z | -r]
              [number]

Write names of (very) big numbers.

select one of these:
  number                say this number
  -T, --time            say the number of seconds the universe exists
  -A, --avogadro        say the avogadro constant; atoms in 12g carbon
  -H, --human           say the number of atoms of a 70 kg human
  -E, --earth           say the number of atoms of the earth
  -S, --sun             say the number of atoms of the sun
  -M, --milkyWay        say the number of atoms in our galaxy
  -U, --universe        say the number of atoms in the universe
  -G, --googol          say a googol (10^100)
  -GG, --googolplex     say a googolplex (10^googol)
  -GGG, --googolplexplex
                        say a googolplexplex (10^googolplex)

help:
  -h, --help            show this help message and exit
  -e, --example         show examples and exit
  -SL, --showLocales    show available locales and exit
  -v, --version         show program's version number and exit
  -c, --licence         show licence information and exit
  -C, --fullLicence     show licence file and exit; tries to download and save licence, if not available

optional arguments:
  -s, --shortScale      use american style: 1 000 000 000 is 1 billion; 1 milliarde if not set - implicit using -l
  -ch, --chuquet        use old latin prefixes like duodeviginti for oktodezi
  -n, --numeric         say the number also in numeric form; it is not recommended to use this option with more than 1 000 000 digits
  -N, --numericOnly     say the number only in numeric form
  -sy, --synonym        say sexdezillion, novemdezillion and quinquillion for sedezillion, novendezillion and quintillion
  -f, --force           ignore size warnings
  -u, --noUmlaut        use ue and oe instead of german umlaut; this might become handy, if you cannot change your terminal's encoding

format:
  -b, --byLine          write components line by line
  -l, --latinOnly       say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"
  -g, --grouping        group thousand blocks; implicit using -n
  -d [DELIMITER], --delimiter [DELIMITER]
                        separate latin prefixes; using '-' if argument stands alone - this is very useful to understand how the numbers get build
  -L LOCALE, --locale LOCALE
                        locale for formatting numbers; only useful with -g/--grouping (see -SL/--showLocales)

number:
  -z, --zeros           do not say given number, but the number with that many zeros
  -r, --random          do not say given number, but a random number with that many digits
</pre>


## List of numbers, with their latin names
To generate the list yourself:
```python
from sayNumber.backend import _sayLatin
names = [_sayLatin(number) for number in range(1, 1000)]
```

| number | name | number | name | number | name |
| ------------- |-------------| -------------|-------------|-------------|-------------|-------------|-------------|
|1 | mi |2 | bi |3 | tri |
|4 | quadri |5 | quinti |6 | sexti |
|7 | septi |8 | okti |9 | noni |
|10 | dezi |11 | undezi |12 | duodezi |
|13 | tredezi |14 | quattuordezi |15 | quindezi |
|16 | sedezi |17 | septendezi |18 | oktodezi |
|19 | novendezi |20 | viginti |21 | unviginti |
|22 | duoviginti |23 | tresviginti |24 | quattuorviginti |
|25 | quinquaviginti |26 | sesviginti |27 | septemviginti |
|28 | oktoviginti |29 | novemviginti |30 | triginta |
|31 | untriginta |32 | duotriginta |33 | trestriginta |
|34 | quattuortriginta |35 | quinquatriginta |36 | sestriginta |
|37 | septentriginta |38 | oktotriginta |39 | noventriginta |
|40 | quadraginta |41 | unquadraginta |42 | duoquadraginta |
|43 | tresquadraginta |44 | quattuorquadraginta |45 | quinquaquadraginta |
|46 | sesquadraginta |47 | septenquadraginta |48 | oktoquadraginta |
|49 | novenquadraginta |50 | quinquaginta |51 | unquinquaginta |
|52 | duoquinquaginta |53 | tresquinquaginta |54 | quattuorquinquaginta |
|55 | quinquaquinquaginta |56 | sesquinquaginta |57 | septenquinquaginta |
|58 | oktoquinquaginta |59 | novenquinquaginta |60 | sexaginta |
|61 | unsexaginta |62 | duosexaginta |63 | tresexaginta |
|64 | quattuorsexaginta |65 | quinquasexaginta |66 | sesexaginta |
|67 | septensexaginta |68 | oktosexaginta |69 | novensexaginta |
|70 | septuaginta |71 | unseptuaginta |72 | duoseptuaginta |
|73 | treseptuaginta |74 | quattuorseptuaginta |75 | quinquaseptuaginta |
|76 | seseptuaginta |77 | septenseptuaginta |78 | oktoseptuaginta |
|79 | novenseptuaginta |80 | oktoginta |81 | unoktoginta |
|82 | duooktoginta |83 | treoktoginta |84 | quattuoroktoginta |
|85 | quinquaoktoginta |86 | sexoktoginta |87 | septemoktoginta |
|88 | oktooktoginta |89 | novemoktoginta |90 | nonaginta |
|91 | unnonaginta |92 | duononaginta |93 | trenonaginta |
|94 | quattuornonaginta |95 | quinquanonaginta |96 | senonaginta |
|97 | septenonaginta |98 | oktononaginta |99 | novenonaginta |
|100 | zenti |101 | unzenti |102 | duozenti |
|103 | treszenti |104 | quattuorzenti |105 | quinquazenti |
|106 | sexzenti |107 | septenzenti |108 | oktozenti |
|109 | novenzenti |110 | dezizenti |111 | undezizenti |
|112 | duodezizenti |113 | tredezizenti |114 | quattuordezizenti |
|115 | quindezizenti |116 | sedezizenti |117 | septendezizenti |
|118 | oktodezizenti |119 | novendezizenti |120 | vigintizenti |
|121 | unvigintizenti |122 | duovigintizenti |123 | tresvigintizenti |
|124 | quattuorvigintizenti |125 | quinquavigintizenti |126 | sesvigintizenti |
|127 | septemvigintizenti |128 | oktovigintizenti |129 | novemvigintizenti |
|130 | trigintazenti |131 | untrigintazenti |132 | duotrigintazenti |
|133 | trestrigintazenti |134 | quattuortrigintazenti |135 | quinquatrigintazenti |
|136 | sestrigintazenti |137 | septentrigintazenti |138 | oktotrigintazenti |
|139 | noventrigintazenti |140 | quadragintazenti |141 | unquadragintazenti |
|142 | duoquadragintazenti |143 | tresquadragintazenti |144 | quattuorquadragintazenti |
|145 | quinquaquadragintazenti |146 | sesquadragintazenti |147 | septenquadragintazenti |
|148 | oktoquadragintazenti |149 | novenquadragintazenti |150 | quinquagintazenti |
|151 | unquinquagintazenti |152 | duoquinquagintazenti |153 | tresquinquagintazenti |
|154 | quattuorquinquagintazenti |155 | quinquaquinquagintazenti |156 | sesquinquagintazenti |
|157 | septenquinquagintazenti |158 | oktoquinquagintazenti |159 | novenquinquagintazenti |
|160 | sexagintazenti |161 | unsexagintazenti |162 | duosexagintazenti |
|163 | tresexagintazenti |164 | quattuorsexagintazenti |165 | quinquasexagintazenti |
|166 | sesexagintazenti |167 | septensexagintazenti |168 | oktosexagintazenti |
|169 | novensexagintazenti |170 | septuagintazenti |171 | unseptuagintazenti |
|172 | duoseptuagintazenti |173 | treseptuagintazenti |174 | quattuorseptuagintazenti |
|175 | quinquaseptuagintazenti |176 | seseptuagintazenti |177 | septenseptuagintazenti |
|178 | oktoseptuagintazenti |179 | novenseptuagintazenti |180 | oktogintazenti |
|181 | unoktogintazenti |182 | duooktogintazenti |183 | treoktogintazenti |
|184 | quattuoroktogintazenti |185 | quinquaoktogintazenti |186 | sexoktogintazenti |
|187 | septemoktogintazenti |188 | oktooktogintazenti |189 | novemoktogintazenti |
|190 | nonagintazenti |191 | unnonagintazenti |192 | duononagintazenti |
|193 | trenonagintazenti |194 | quattuornonagintazenti |195 | quinquanonagintazenti |
|196 | senonagintazenti |197 | septenonagintazenti |198 | oktononagintazenti |
|199 | novenonagintazenti |200 | duzenti |201 | unduzenti |
|202 | duoduzenti |203 | treduzenti |204 | quattuorduzenti |
|205 | quinquaduzenti |206 | seduzenti |207 | septenduzenti |
|208 | oktoduzenti |209 | novenduzenti |210 | deziduzenti |
|211 | undeziduzenti |212 | duodeziduzenti |213 | tredeziduzenti |
|214 | quattuordeziduzenti |215 | quindeziduzenti |216 | sedeziduzenti |
|217 | septendeziduzenti |218 | oktodeziduzenti |219 | novendeziduzenti |
|220 | vigintiduzenti |221 | unvigintiduzenti |222 | duovigintiduzenti |
|223 | tresvigintiduzenti |224 | quattuorvigintiduzenti |225 | quinquavigintiduzenti |
|226 | sesvigintiduzenti |227 | septemvigintiduzenti |228 | oktovigintiduzenti |
|229 | novemvigintiduzenti |230 | trigintaduzenti |231 | untrigintaduzenti |
|232 | duotrigintaduzenti |233 | trestrigintaduzenti |234 | quattuortrigintaduzenti |
|235 | quinquatrigintaduzenti |236 | sestrigintaduzenti |237 | septentrigintaduzenti |
|238 | oktotrigintaduzenti |239 | noventrigintaduzenti |240 | quadragintaduzenti |
|241 | unquadragintaduzenti |242 | duoquadragintaduzenti |243 | tresquadragintaduzenti |
|244 | quattuorquadragintaduzenti |245 | quinquaquadragintaduzenti |246 | sesquadragintaduzenti |
|247 | septenquadragintaduzenti |248 | oktoquadragintaduzenti |249 | novenquadragintaduzenti |
|250 | quinquagintaduzenti |251 | unquinquagintaduzenti |252 | duoquinquagintaduzenti |
|253 | tresquinquagintaduzenti |254 | quattuorquinquagintaduzenti |255 | quinquaquinquagintaduzenti |
|256 | sesquinquagintaduzenti |257 | septenquinquagintaduzenti |258 | oktoquinquagintaduzenti |
|259 | novenquinquagintaduzenti |260 | sexagintaduzenti |261 | unsexagintaduzenti |
|262 | duosexagintaduzenti |263 | tresexagintaduzenti |264 | quattuorsexagintaduzenti |
|265 | quinquasexagintaduzenti |266 | sesexagintaduzenti |267 | septensexagintaduzenti |
|268 | oktosexagintaduzenti |269 | novensexagintaduzenti |270 | septuagintaduzenti |
|271 | unseptuagintaduzenti |272 | duoseptuagintaduzenti |273 | treseptuagintaduzenti |
|274 | quattuorseptuagintaduzenti |275 | quinquaseptuagintaduzenti |276 | seseptuagintaduzenti |
|277 | septenseptuagintaduzenti |278 | oktoseptuagintaduzenti |279 | novenseptuagintaduzenti |
|280 | oktogintaduzenti |281 | unoktogintaduzenti |282 | duooktogintaduzenti |
|283 | treoktogintaduzenti |284 | quattuoroktogintaduzenti |285 | quinquaoktogintaduzenti |
|286 | sexoktogintaduzenti |287 | septemoktogintaduzenti |288 | oktooktogintaduzenti |
|289 | novemoktogintaduzenti |290 | nonagintaduzenti |291 | unnonagintaduzenti |
|292 | duononagintaduzenti |293 | trenonagintaduzenti |294 | quattuornonagintaduzenti |
|295 | quinquanonagintaduzenti |296 | senonagintaduzenti |297 | septenonagintaduzenti |
|298 | oktononagintaduzenti |299 | novenonagintaduzenti |300 | trezenti |
|301 | untrezenti |302 | duotrezenti |303 | trestrezenti |
|304 | quattuortrezenti |305 | quinquatrezenti |306 | sestrezenti |
|307 | septentrezenti |308 | oktotrezenti |309 | noventrezenti |
|310 | dezitrezenti |311 | undezitrezenti |312 | duodezitrezenti |
|313 | tredezitrezenti |314 | quattuordezitrezenti |315 | quindezitrezenti |
|316 | sedezitrezenti |317 | septendezitrezenti |318 | oktodezitrezenti |
|319 | novendezitrezenti |320 | vigintitrezenti |321 | unvigintitrezenti |
|322 | duovigintitrezenti |323 | tresvigintitrezenti |324 | quattuorvigintitrezenti |
|325 | quinquavigintitrezenti |326 | sesvigintitrezenti |327 | septemvigintitrezenti |
|328 | oktovigintitrezenti |329 | novemvigintitrezenti |330 | trigintatrezenti |
|331 | untrigintatrezenti |332 | duotrigintatrezenti |333 | trestrigintatrezenti |
|334 | quattuortrigintatrezenti |335 | quinquatrigintatrezenti |336 | sestrigintatrezenti |
|337 | septentrigintatrezenti |338 | oktotrigintatrezenti |339 | noventrigintatrezenti |
|340 | quadragintatrezenti |341 | unquadragintatrezenti |342 | duoquadragintatrezenti |
|343 | tresquadragintatrezenti |344 | quattuorquadragintatrezenti |345 | quinquaquadragintatrezenti |
|346 | sesquadragintatrezenti |347 | septenquadragintatrezenti |348 | oktoquadragintatrezenti |
|349 | novenquadragintatrezenti |350 | quinquagintatrezenti |351 | unquinquagintatrezenti |
|352 | duoquinquagintatrezenti |353 | tresquinquagintatrezenti |354 | quattuorquinquagintatrezenti |
|355 | quinquaquinquagintatrezenti |356 | sesquinquagintatrezenti |357 | septenquinquagintatrezenti |
|358 | oktoquinquagintatrezenti |359 | novenquinquagintatrezenti |360 | sexagintatrezenti |
|361 | unsexagintatrezenti |362 | duosexagintatrezenti |363 | tresexagintatrezenti |
|364 | quattuorsexagintatrezenti |365 | quinquasexagintatrezenti |366 | sesexagintatrezenti |
|367 | septensexagintatrezenti |368 | oktosexagintatrezenti |369 | novensexagintatrezenti |
|370 | septuagintatrezenti |371 | unseptuagintatrezenti |372 | duoseptuagintatrezenti |
|373 | treseptuagintatrezenti |374 | quattuorseptuagintatrezenti |375 | quinquaseptuagintatrezenti |
|376 | seseptuagintatrezenti |377 | septenseptuagintatrezenti |378 | oktoseptuagintatrezenti |
|379 | novenseptuagintatrezenti |380 | oktogintatrezenti |381 | unoktogintatrezenti |
|382 | duooktogintatrezenti |383 | treoktogintatrezenti |384 | quattuoroktogintatrezenti |
|385 | quinquaoktogintatrezenti |386 | sexoktogintatrezenti |387 | septemoktogintatrezenti |
|388 | oktooktogintatrezenti |389 | novemoktogintatrezenti |390 | nonagintatrezenti |
|391 | unnonagintatrezenti |392 | duononagintatrezenti |393 | trenonagintatrezenti |
|394 | quattuornonagintatrezenti |395 | quinquanonagintatrezenti |396 | senonagintatrezenti |
|397 | septenonagintatrezenti |398 | oktononagintatrezenti |399 | novenonagintatrezenti |
|400 | quadringenti |401 | unquadringenti |402 | duoquadringenti |
|403 | tresquadringenti |404 | quattuorquadringenti |405 | quinquaquadringenti |
|406 | sesquadringenti |407 | septenquadringenti |408 | oktoquadringenti |
|409 | novenquadringenti |410 | deziquadringenti |411 | undeziquadringenti |
|412 | duodeziquadringenti |413 | tredeziquadringenti |414 | quattuordeziquadringenti |
|415 | quindeziquadringenti |416 | sedeziquadringenti |417 | septendeziquadringenti |
|418 | oktodeziquadringenti |419 | novendeziquadringenti |420 | vigintiquadringenti |
|421 | unvigintiquadringenti |422 | duovigintiquadringenti |423 | tresvigintiquadringenti |
|424 | quattuorvigintiquadringenti |425 | quinquavigintiquadringenti |426 | sesvigintiquadringenti |
|427 | septemvigintiquadringenti |428 | oktovigintiquadringenti |429 | novemvigintiquadringenti |
|430 | trigintaquadringenti |431 | untrigintaquadringenti |432 | duotrigintaquadringenti |
|433 | trestrigintaquadringenti |434 | quattuortrigintaquadringenti |435 | quinquatrigintaquadringenti |
|436 | sestrigintaquadringenti |437 | septentrigintaquadringenti |438 | oktotrigintaquadringenti |
|439 | noventrigintaquadringenti |440 | quadragintaquadringenti |441 | unquadragintaquadringenti |
|442 | duoquadragintaquadringenti |443 | tresquadragintaquadringenti |444 | quattuorquadragintaquadringenti |
|445 | quinquaquadragintaquadringenti |446 | sesquadragintaquadringenti |447 | septenquadragintaquadringenti |
|448 | oktoquadragintaquadringenti |449 | novenquadragintaquadringenti |450 | quinquagintaquadringenti |
|451 | unquinquagintaquadringenti |452 | duoquinquagintaquadringenti |453 | tresquinquagintaquadringenti |
|454 | quattuorquinquagintaquadringenti |455 | quinquaquinquagintaquadringenti |456 | sesquinquagintaquadringenti |
|457 | septenquinquagintaquadringenti |458 | oktoquinquagintaquadringenti |459 | novenquinquagintaquadringenti |
|460 | sexagintaquadringenti |461 | unsexagintaquadringenti |462 | duosexagintaquadringenti |
|463 | tresexagintaquadringenti |464 | quattuorsexagintaquadringenti |465 | quinquasexagintaquadringenti |
|466 | sesexagintaquadringenti |467 | septensexagintaquadringenti |468 | oktosexagintaquadringenti |
|469 | novensexagintaquadringenti |470 | septuagintaquadringenti |471 | unseptuagintaquadringenti |
|472 | duoseptuagintaquadringenti |473 | treseptuagintaquadringenti |474 | quattuorseptuagintaquadringenti |
|475 | quinquaseptuagintaquadringenti |476 | seseptuagintaquadringenti |477 | septenseptuagintaquadringenti |
|478 | oktoseptuagintaquadringenti |479 | novenseptuagintaquadringenti |480 | oktogintaquadringenti |
|481 | unoktogintaquadringenti |482 | duooktogintaquadringenti |483 | treoktogintaquadringenti |
|484 | quattuoroktogintaquadringenti |485 | quinquaoktogintaquadringenti |486 | sexoktogintaquadringenti |
|487 | septemoktogintaquadringenti |488 | oktooktogintaquadringenti |489 | novemoktogintaquadringenti |
|490 | nonagintaquadringenti |491 | unnonagintaquadringenti |492 | duononagintaquadringenti |
|493 | trenonagintaquadringenti |494 | quattuornonagintaquadringenti |495 | quinquanonagintaquadringenti |
|496 | senonagintaquadringenti |497 | septenonagintaquadringenti |498 | oktononagintaquadringenti |
|499 | novenonagintaquadringenti |500 | quingenti |501 | unquingenti |
|502 | duoquingenti |503 | tresquingenti |504 | quattuorquingenti |
|505 | quinquaquingenti |506 | sesquingenti |507 | septenquingenti |
|508 | oktoquingenti |509 | novenquingenti |510 | deziquingenti |
|511 | undeziquingenti |512 | duodeziquingenti |513 | tredeziquingenti |
|514 | quattuordeziquingenti |515 | quindeziquingenti |516 | sedeziquingenti |
|517 | septendeziquingenti |518 | oktodeziquingenti |519 | novendeziquingenti |
|520 | vigintiquingenti |521 | unvigintiquingenti |522 | duovigintiquingenti |
|523 | tresvigintiquingenti |524 | quattuorvigintiquingenti |525 | quinquavigintiquingenti |
|526 | sesvigintiquingenti |527 | septemvigintiquingenti |528 | oktovigintiquingenti |
|529 | novemvigintiquingenti |530 | trigintaquingenti |531 | untrigintaquingenti |
|532 | duotrigintaquingenti |533 | trestrigintaquingenti |534 | quattuortrigintaquingenti |
|535 | quinquatrigintaquingenti |536 | sestrigintaquingenti |537 | septentrigintaquingenti |
|538 | oktotrigintaquingenti |539 | noventrigintaquingenti |540 | quadragintaquingenti |
|541 | unquadragintaquingenti |542 | duoquadragintaquingenti |543 | tresquadragintaquingenti |
|544 | quattuorquadragintaquingenti |545 | quinquaquadragintaquingenti |546 | sesquadragintaquingenti |
|547 | septenquadragintaquingenti |548 | oktoquadragintaquingenti |549 | novenquadragintaquingenti |
|550 | quinquagintaquingenti |551 | unquinquagintaquingenti |552 | duoquinquagintaquingenti |
|553 | tresquinquagintaquingenti |554 | quattuorquinquagintaquingenti |555 | quinquaquinquagintaquingenti |
|556 | sesquinquagintaquingenti |557 | septenquinquagintaquingenti |558 | oktoquinquagintaquingenti |
|559 | novenquinquagintaquingenti |560 | sexagintaquingenti |561 | unsexagintaquingenti |
|562 | duosexagintaquingenti |563 | tresexagintaquingenti |564 | quattuorsexagintaquingenti |
|565 | quinquasexagintaquingenti |566 | sesexagintaquingenti |567 | septensexagintaquingenti |
|568 | oktosexagintaquingenti |569 | novensexagintaquingenti |570 | septuagintaquingenti |
|571 | unseptuagintaquingenti |572 | duoseptuagintaquingenti |573 | treseptuagintaquingenti |
|574 | quattuorseptuagintaquingenti |575 | quinquaseptuagintaquingenti |576 | seseptuagintaquingenti |
|577 | septenseptuagintaquingenti |578 | oktoseptuagintaquingenti |579 | novenseptuagintaquingenti |
|580 | oktogintaquingenti |581 | unoktogintaquingenti |582 | duooktogintaquingenti |
|583 | treoktogintaquingenti |584 | quattuoroktogintaquingenti |585 | quinquaoktogintaquingenti |
|586 | sexoktogintaquingenti |587 | septemoktogintaquingenti |588 | oktooktogintaquingenti |
|589 | novemoktogintaquingenti |590 | nonagintaquingenti |591 | unnonagintaquingenti |
|592 | duononagintaquingenti |593 | trenonagintaquingenti |594 | quattuornonagintaquingenti |
|595 | quinquanonagintaquingenti |596 | senonagintaquingenti |597 | septenonagintaquingenti |
|598 | oktononagintaquingenti |599 | novenonagintaquingenti |600 | seszenti |
|601 | unseszenti |602 | duoseszenti |603 | treseszenti |
|604 | quattuorseszenti |605 | quinquaseszenti |606 | seseszenti |
|607 | septenseszenti |608 | oktoseszenti |609 | novenseszenti |
|610 | deziseszenti |611 | undeziseszenti |612 | duodeziseszenti |
|613 | tredeziseszenti |614 | quattuordeziseszenti |615 | quindeziseszenti |
|616 | sedeziseszenti |617 | septendeziseszenti |618 | oktodeziseszenti |
|619 | novendeziseszenti |620 | vigintiseszenti |621 | unvigintiseszenti |
|622 | duovigintiseszenti |623 | tresvigintiseszenti |624 | quattuorvigintiseszenti |
|625 | quinquavigintiseszenti |626 | sesvigintiseszenti |627 | septemvigintiseszenti |
|628 | oktovigintiseszenti |629 | novemvigintiseszenti |630 | trigintaseszenti |
|631 | untrigintaseszenti |632 | duotrigintaseszenti |633 | trestrigintaseszenti |
|634 | quattuortrigintaseszenti |635 | quinquatrigintaseszenti |636 | sestrigintaseszenti |
|637 | septentrigintaseszenti |638 | oktotrigintaseszenti |639 | noventrigintaseszenti |
|640 | quadragintaseszenti |641 | unquadragintaseszenti |642 | duoquadragintaseszenti |
|643 | tresquadragintaseszenti |644 | quattuorquadragintaseszenti |645 | quinquaquadragintaseszenti |
|646 | sesquadragintaseszenti |647 | septenquadragintaseszenti |648 | oktoquadragintaseszenti |
|649 | novenquadragintaseszenti |650 | quinquagintaseszenti |651 | unquinquagintaseszenti |
|652 | duoquinquagintaseszenti |653 | tresquinquagintaseszenti |654 | quattuorquinquagintaseszenti |
|655 | quinquaquinquagintaseszenti |656 | sesquinquagintaseszenti |657 | septenquinquagintaseszenti |
|658 | oktoquinquagintaseszenti |659 | novenquinquagintaseszenti |660 | sexagintaseszenti |
|661 | unsexagintaseszenti |662 | duosexagintaseszenti |663 | tresexagintaseszenti |
|664 | quattuorsexagintaseszenti |665 | quinquasexagintaseszenti |666 | sesexagintaseszenti |
|667 | septensexagintaseszenti |668 | oktosexagintaseszenti |669 | novensexagintaseszenti |
|670 | septuagintaseszenti |671 | unseptuagintaseszenti |672 | duoseptuagintaseszenti |
|673 | treseptuagintaseszenti |674 | quattuorseptuagintaseszenti |675 | quinquaseptuagintaseszenti |
|676 | seseptuagintaseszenti |677 | septenseptuagintaseszenti |678 | oktoseptuagintaseszenti |
|679 | novenseptuagintaseszenti |680 | oktogintaseszenti |681 | unoktogintaseszenti |
|682 | duooktogintaseszenti |683 | treoktogintaseszenti |684 | quattuoroktogintaseszenti |
|685 | quinquaoktogintaseszenti |686 | sexoktogintaseszenti |687 | septemoktogintaseszenti |
|688 | oktooktogintaseszenti |689 | novemoktogintaseszenti |690 | nonagintaseszenti |
|691 | unnonagintaseszenti |692 | duononagintaseszenti |693 | trenonagintaseszenti |
|694 | quattuornonagintaseszenti |695 | quinquanonagintaseszenti |696 | senonagintaseszenti |
|697 | septenonagintaseszenti |698 | oktononagintaseszenti |699 | novenonagintaseszenti |
|700 | septingenti |701 | unseptingenti |702 | duoseptingenti |
|703 | treseptingenti |704 | quattuorseptingenti |705 | quinquaseptingenti |
|706 | seseptingenti |707 | septenseptingenti |708 | oktoseptingenti |
|709 | novenseptingenti |710 | deziseptingenti |711 | undeziseptingenti |
|712 | duodeziseptingenti |713 | tredeziseptingenti |714 | quattuordeziseptingenti |
|715 | quindeziseptingenti |716 | sedeziseptingenti |717 | septendeziseptingenti |
|718 | oktodeziseptingenti |719 | novendeziseptingenti |720 | vigintiseptingenti |
|721 | unvigintiseptingenti |722 | duovigintiseptingenti |723 | tresvigintiseptingenti |
|724 | quattuorvigintiseptingenti |725 | quinquavigintiseptingenti |726 | sesvigintiseptingenti |
|727 | septemvigintiseptingenti |728 | oktovigintiseptingenti |729 | novemvigintiseptingenti |
|730 | trigintaseptingenti |731 | untrigintaseptingenti |732 | duotrigintaseptingenti |
|733 | trestrigintaseptingenti |734 | quattuortrigintaseptingenti |735 | quinquatrigintaseptingenti |
|736 | sestrigintaseptingenti |737 | septentrigintaseptingenti |738 | oktotrigintaseptingenti |
|739 | noventrigintaseptingenti |740 | quadragintaseptingenti |741 | unquadragintaseptingenti |
|742 | duoquadragintaseptingenti |743 | tresquadragintaseptingenti |744 | quattuorquadragintaseptingenti |
|745 | quinquaquadragintaseptingenti |746 | sesquadragintaseptingenti |747 | septenquadragintaseptingenti |
|748 | oktoquadragintaseptingenti |749 | novenquadragintaseptingenti |750 | quinquagintaseptingenti |
|751 | unquinquagintaseptingenti |752 | duoquinquagintaseptingenti |753 | tresquinquagintaseptingenti |
|754 | quattuorquinquagintaseptingenti |755 | quinquaquinquagintaseptingenti |756 | sesquinquagintaseptingenti |
|757 | septenquinquagintaseptingenti |758 | oktoquinquagintaseptingenti |759 | novenquinquagintaseptingenti |
|760 | sexagintaseptingenti |761 | unsexagintaseptingenti |762 | duosexagintaseptingenti |
|763 | tresexagintaseptingenti |764 | quattuorsexagintaseptingenti |765 | quinquasexagintaseptingenti |
|766 | sesexagintaseptingenti |767 | septensexagintaseptingenti |768 | oktosexagintaseptingenti |
|769 | novensexagintaseptingenti |770 | septuagintaseptingenti |771 | unseptuagintaseptingenti |
|772 | duoseptuagintaseptingenti |773 | treseptuagintaseptingenti |774 | quattuorseptuagintaseptingenti |
|775 | quinquaseptuagintaseptingenti |776 | seseptuagintaseptingenti |777 | septenseptuagintaseptingenti |
|778 | oktoseptuagintaseptingenti |779 | novenseptuagintaseptingenti |780 | oktogintaseptingenti |
|781 | unoktogintaseptingenti |782 | duooktogintaseptingenti |783 | treoktogintaseptingenti |
|784 | quattuoroktogintaseptingenti |785 | quinquaoktogintaseptingenti |786 | sexoktogintaseptingenti |
|787 | septemoktogintaseptingenti |788 | oktooktogintaseptingenti |789 | novemoktogintaseptingenti |
|790 | nonagintaseptingenti |791 | unnonagintaseptingenti |792 | duononagintaseptingenti |
|793 | trenonagintaseptingenti |794 | quattuornonagintaseptingenti |795 | quinquanonagintaseptingenti |
|796 | senonagintaseptingenti |797 | septenonagintaseptingenti |798 | oktononagintaseptingenti |
|799 | novenonagintaseptingenti |800 | oktingenti |801 | unoktingenti |
|802 | duooktingenti |803 | treoktingenti |804 | quattuoroktingenti |
|805 | quinquaoktingenti |806 | sexoktingenti |807 | septemoktingenti |
|808 | oktooktingenti |809 | novemoktingenti |810 | dezioktingenti |
|811 | undezioktingenti |812 | duodezioktingenti |813 | tredezioktingenti |
|814 | quattuordezioktingenti |815 | quindezioktingenti |816 | sedezioktingenti |
|817 | septendezioktingenti |818 | oktodezioktingenti |819 | novendezioktingenti |
|820 | vigintioktingenti |821 | unvigintioktingenti |822 | duovigintioktingenti |
|823 | tresvigintioktingenti |824 | quattuorvigintioktingenti |825 | quinquavigintioktingenti |
|826 | sesvigintioktingenti |827 | septemvigintioktingenti |828 | oktovigintioktingenti |
|829 | novemvigintioktingenti |830 | trigintaoktingenti |831 | untrigintaoktingenti |
|832 | duotrigintaoktingenti |833 | trestrigintaoktingenti |834 | quattuortrigintaoktingenti |
|835 | quinquatrigintaoktingenti |836 | sestrigintaoktingenti |837 | septentrigintaoktingenti |
|838 | oktotrigintaoktingenti |839 | noventrigintaoktingenti |840 | quadragintaoktingenti |
|841 | unquadragintaoktingenti |842 | duoquadragintaoktingenti |843 | tresquadragintaoktingenti |
|844 | quattuorquadragintaoktingenti |845 | quinquaquadragintaoktingenti |846 | sesquadragintaoktingenti |
|847 | septenquadragintaoktingenti |848 | oktoquadragintaoktingenti |849 | novenquadragintaoktingenti |
|850 | quinquagintaoktingenti |851 | unquinquagintaoktingenti |852 | duoquinquagintaoktingenti |
|853 | tresquinquagintaoktingenti |854 | quattuorquinquagintaoktingenti |855 | quinquaquinquagintaoktingenti |
|856 | sesquinquagintaoktingenti |857 | septenquinquagintaoktingenti |858 | oktoquinquagintaoktingenti |
|859 | novenquinquagintaoktingenti |860 | sexagintaoktingenti |861 | unsexagintaoktingenti |
|862 | duosexagintaoktingenti |863 | tresexagintaoktingenti |864 | quattuorsexagintaoktingenti |
|865 | quinquasexagintaoktingenti |866 | sesexagintaoktingenti |867 | septensexagintaoktingenti |
|868 | oktosexagintaoktingenti |869 | novensexagintaoktingenti |870 | septuagintaoktingenti |
|871 | unseptuagintaoktingenti |872 | duoseptuagintaoktingenti |873 | treseptuagintaoktingenti |
|874 | quattuorseptuagintaoktingenti |875 | quinquaseptuagintaoktingenti |876 | seseptuagintaoktingenti |
|877 | septenseptuagintaoktingenti |878 | oktoseptuagintaoktingenti |879 | novenseptuagintaoktingenti |
|880 | oktogintaoktingenti |881 | unoktogintaoktingenti |882 | duooktogintaoktingenti |
|883 | treoktogintaoktingenti |884 | quattuoroktogintaoktingenti |885 | quinquaoktogintaoktingenti |
|886 | sexoktogintaoktingenti |887 | septemoktogintaoktingenti |888 | oktooktogintaoktingenti |
|889 | novemoktogintaoktingenti |890 | nonagintaoktingenti |891 | unnonagintaoktingenti |
|892 | duononagintaoktingenti |893 | trenonagintaoktingenti |894 | quattuornonagintaoktingenti |
|895 | quinquanonagintaoktingenti |896 | senonagintaoktingenti |897 | septenonagintaoktingenti |
|898 | oktononagintaoktingenti |899 | novenonagintaoktingenti |900 | nongenti |
|901 | unnongenti |902 | duonongenti |903 | trenongenti |
|904 | quattuornongenti |905 | quinquanongenti |906 | senongenti |
|907 | septenongenti |908 | oktonongenti |909 | novenongenti |
|910 | dezinongenti |911 | undezinongenti |912 | duodezinongenti |
|913 | tredezinongenti |914 | quattuordezinongenti |915 | quindezinongenti |
|916 | sedezinongenti |917 | septendezinongenti |918 | oktodezinongenti |
|919 | novendezinongenti |920 | vigintinongenti |921 | unvigintinongenti |
|922 | duovigintinongenti |923 | tresvigintinongenti |924 | quattuorvigintinongenti |
|925 | quinquavigintinongenti |926 | sesvigintinongenti |927 | septemvigintinongenti |
|928 | oktovigintinongenti |929 | novemvigintinongenti |930 | trigintanongenti |
|931 | untrigintanongenti |932 | duotrigintanongenti |933 | trestrigintanongenti |
|934 | quattuortrigintanongenti |935 | quinquatrigintanongenti |936 | sestrigintanongenti |
|937 | septentrigintanongenti |938 | oktotrigintanongenti |939 | noventrigintanongenti |
|940 | quadragintanongenti |941 | unquadragintanongenti |942 | duoquadragintanongenti |
|943 | tresquadragintanongenti |944 | quattuorquadragintanongenti |945 | quinquaquadragintanongenti |
|946 | sesquadragintanongenti |947 | septenquadragintanongenti |948 | oktoquadragintanongenti |
|949 | novenquadragintanongenti |950 | quinquagintanongenti |951 | unquinquagintanongenti |
|952 | duoquinquagintanongenti |953 | tresquinquagintanongenti |954 | quattuorquinquagintanongenti |
|955 | quinquaquinquagintanongenti |956 | sesquinquagintanongenti |957 | septenquinquagintanongenti |
|958 | oktoquinquagintanongenti |959 | novenquinquagintanongenti |960 | sexagintanongenti |
|961 | unsexagintanongenti |962 | duosexagintanongenti |963 | tresexagintanongenti |
|964 | quattuorsexagintanongenti |965 | quinquasexagintanongenti |966 | sesexagintanongenti |
|967 | septensexagintanongenti |968 | oktosexagintanongenti |969 | novensexagintanongenti |
|970 | septuagintanongenti |971 | unseptuagintanongenti |972 | duoseptuagintanongenti |
|973 | treseptuagintanongenti |974 | quattuorseptuagintanongenti |975 | quinquaseptuagintanongenti |
|976 | seseptuagintanongenti |977 | septenseptuagintanongenti |978 | oktoseptuagintanongenti |
|979 | novenseptuagintanongenti |980 | oktogintanongenti |981 | unoktogintanongenti |
|982 | duooktogintanongenti |983 | treoktogintanongenti |984 | quattuoroktogintanongenti |
|985 | quinquaoktogintanongenti |986 | sexoktogintanongenti |987 | septemoktogintanongenti |
|988 | oktooktogintanongenti |989 | novemoktogintanongenti |990 | nonagintanongenti |
|991 | unnonagintanongenti |992 | duononagintanongenti |993 | trenonagintanongenti |
|994 | quattuornonagintanongenti |995 | quinquanonagintanongenti |996 | senonagintanongenti |
|997 | septenonagintanongenti |998 | oktononagintanongenti |999 | novenonagintanongenti |

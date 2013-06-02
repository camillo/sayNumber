# -*- coding: iso-8859-1 -*-

# Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com
# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

import os
import string
import logging

logger = logging.getLogger(__name__)

# German has a lot of exceptions during the first 20 numbers, so easiest thing is
# to collect them in a dict, instead of writing special code.
GERMAN_SMALL_NUMBERS = {
    '0': 'null',      '1': 'eins',       '2': 'zwei',       '3': 'drei',      '4': 'vier',
    '5': 'f�nf',      '6': 'sechs',      '7': 'sieben',     '8': 'acht',      '9': 'neun',
    '10': 'zehn',     '11': 'elf',       '12': 'zw�lf',     '13': 'dreizehn', '14': 'vierzehn',
    '15': 'f�nfzehn', '16': 'sechszehn', '17': 'siebzehn',  '18': 'achtzehn', '19': 'neunzehn'}

# These are exceptions, building german 2 digit numbers like 72.
GERMAN_DEZI_EXCEPTIONS = {
    '2': 'zwan',
    '6': 'sech',
    '7': 'sieb'
}

# These are the prefixes to build latin numbers.
LATIN_PREFIXES = [
    # 0: list of one-prefixes, that stands alone (numbers 1-9)
    ['mi', 'bi', 'tri', 'quadri', 'quinti', 'sexti', 'septi', 'okti', 'noni'],
    # 1: list of one-prefixes, that needs to get combined with a ten or hundred prefix.
    [['un', ], ['duo', ], ['tre', 's'], ['quattuor', ], ['quinqua', ],
    ['se', 's', 'x'], ['septe', 'm', 'n'], ['okto', ], ['nove', 'm', 'n']],
    # 2: list of ten-prefixes
    [['dezi', 'n'], ['viginti', 'm', 's'], ['triginta', 'n', 's'], ['quadraginta', 'n', 's'],
    ['quinquaginta', 'n', 's'], ['sexaginta', 'n'], ['septuaginta', 'n'], ['oktoginta', 'm', 'x'], ['nonaginta', ]],
    # 3: list of hundred-prefixes
    [['zenti', 'n', 'x'], ['duzenti', 'n'], ['trezenti', 'n', 's'], ['quadringenti', 'n', 's'],
    ['quingenti', 'n', 's'], ['seszenti', 'n'], ['septingenti', 'n'], ['oktingenti', 'm', 'x'], ['nongenti', ]]
]
# Named indexes for LATIN_PREFIXES to make code better readable.
ALONE_ONES, COMBINE_ONES, TENS, HUNDREDS = 0, 1, 2, 3

# There are two exceptions, building latin numbers
# 1. quinquadezi has a different name: quindezi
# 2. 103 would normally be trezenti, but this is reserved for 300. This is, why 103 is treszenti.
COMBINE_EXCEPTIONS = {
    'quinquadezi': ['quin', 'dezi'],
    'trezenti': ['tres', 'zenti']
}

# These are valid synonyms, that can be used.
LATIN_SYNONYMS = {
    16: ['sex', 'dezi'],
    19: ['novem', 'dezi'],
    5: ['quinqui', ]
}


def _sayLatin(number, delimiter='', synonym=False):
    """
    Build the latin word for given number.
    @param number int from 1 to 999.
    @param delimiter Separates the prefixes
    @return The latin word for given number.
    """
    if not 0 < number < 1000:
        raise ValueError("Number must be 1-999; given: [%s]." % number)
    if delimiter and delimiter in string.ascii_lowercase:
        raise ValueError("Delimiter must not be a-z.")
    logger.debug("say latin: %s", number)

    if synonym and number in LATIN_SYNONYMS:
        return delimiter.join(LATIN_SYNONYMS[number])

    one = number % 10
    ten = (number - one) % 100
    hundred = number - ten - one

    hundredPrefix = LATIN_PREFIXES[HUNDREDS][hundred / 100 - 1] if hundred else None
    tenPrefix = LATIN_PREFIXES[TENS][ten / 10 - 1] if ten else None

    combineHundredIfNeeded = lambda ret: ret + delimiter + hundredPrefix[0] if hundred else ret

    if ten == 0 and hundred == 0:
        return LATIN_PREFIXES[ALONE_ONES][one - 1]
    if one == 0:
        if ten == 0:
            return hundredPrefix[0]
        else:
            ret = tenPrefix[0]
            return combineHundredIfNeeded(ret)

    onePrefix = LATIN_PREFIXES[COMBINE_ONES][one - 1]

    def combineOne(other):
        """ Combine the one prefix, with a ten or hundred. """
        additionalCharacter = set(onePrefix[1:]).intersection(other[1:])
        ret = onePrefix[0] + (additionalCharacter.pop() if additionalCharacter else '') + delimiter + other[0]
        exception = COMBINE_EXCEPTIONS.get(ret.replace(delimiter, ''), None)
        return delimiter.join(exception) if exception else ret

    if ten == 0:
        return combineOne(hundredPrefix)
    ret = combineOne(tenPrefix)
    return combineHundredIfNeeded(ret)


def _sayLongScale(zeros, plural=False, delimiter='', synonym=False):
    """
    Build the word for the number, starting with a 1, followed by as many 0 as specified in zeros.
    @param zeros the number of "0"s, following the "1". Must be 6 at least and zeros mod 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long scale system.
    """
    if zeros < 6:
        raise ValueError('Zeros must be 6 or greater.')
    if zeros % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    sixes, lliarde = divmod(zeros, 6)
    ret = ""
    while sixes > 0:
        # We do one thousand block per iteration, starting with the the lowest value.
        current = sixes % 1000
        if current == 0:
            # This is the prefix for 000
            prefix = "ni" + delimiter
            logger.debug("say latin: 000")
        else:
            prefix = _sayLatin(current, delimiter, synonym)
            # If we combine a ten prefix, without a hundred prefix, the 'a' changes to 'i' if present at last position.
            if 100 > current > 9 and prefix[-1] == "a":
                prefix = prefix[:-1] + 'i'
            sixes -= current
            prefix += delimiter
        # This is the prefix for separating the thousand blocks. We skip this, if this is the first iteration.
        if ret:
            prefix += "lli" + delimiter
        ret = prefix + ret
        sixes /= 1000
    # Now add the postfix to make a word.
    if lliarde:
        ret += "lliarde"
        pluralPostfix = "n"
    else:
        ret += "llion"
        pluralPostfix = "en"
    return ret + pluralPostfix if plural else ret


def _sayShortScale(zeros, plural=False, delimiter='', synonym=False):
    """
    Build the word for the number, starting with a 1, followed by as many 0 as specified in zeros.
    @param zeros the number of "0"s, following the "1". Must be 6 at least and zeros mod 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long scale system.
    """
    if zeros < 6:
        raise ValueError('Zeros must be 6 or greater.')
    if zeros % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    longScaleZeros = 2 * zeros - 6
    ret = _sayLongScale(longScaleZeros, plural=False, delimiter=delimiter, synonym=synonym).replace('z', 'c')

    return ret + "s" if plural else ret


def sayByExp(zeros, plural=False, delimiter='', shortScale=False, synonym=False):
    """
    Build the word for the number, starting with a 1, followed by as many "0" as specified in zeros.
    @param zeros the number of "0", following the "1". Must be 3 at least and zeros % 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @param delimiter Separates the latin prefixes.
    @param shortScale True, to use us/uk system, german otherwise
    """
    if zeros < 3:
        raise ValueError('Zeros must be 3 or greater.')
    if zeros % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    if zeros == 3:
        if shortScale:
            ret = "thousand"
        else:
            ret = "tausend"
    elif shortScale:
        ret = _sayShortScale(zeros, plural, delimiter, synonym)
    else:
        ret = _sayLongScale(zeros, plural, delimiter, synonym)
    return ret


def _sayGermanShortNumber(shortNumber, sayEin):
    """
    Helper to say a short number, that is used before another part (neunzehn millionen or eine million or ein tausend)
    @param sayEin True to say ein, instead of eine in case of shortNmuber == 1
    """
    if shortNumber == "1":
        return "ein" if sayEin else "eine"
    return GERMAN_SMALL_NUMBERS[shortNumber]


def _sayGerman(number, componentsLeft):
    """
    Helper to build the german word for given number.
    @param number Must be 0-999.
    """
    if not 0 <= int(number) <= 999:
        raise ValueError("Number must be 0-999")
    number = str(number)
    if number in GERMAN_SMALL_NUMBERS:
        return _sayGermanShortNumber(number, componentsLeft == 2)
    currentLen = len(number)
    ret = ""
    if currentLen == 3:
        if not number[0] == "0":
            ret = _sayGermanShortNumber(number[0], sayEin=True) + "hundert"
        return ret + _sayGerman(number[1:], componentsLeft)

    if number[0] == "0":
        if number[1] == "0":
            return ""
        return GERMAN_SMALL_NUMBERS[number[1]]
    if not number[1] == "0":
        ret = _sayGermanShortNumber(number[1], sayEin=True) + "und"
    ret += GERMAN_DEZI_EXCEPTIONS.get(number[0], GERMAN_SMALL_NUMBERS[number[0]]) + "zig"
    return ret


def _splitThousandBlocks(number):
    """
    Helper that splits the given number to blocks of thousands.
    @return array of blocks. As lower the index, as higher the value.
    """
    ret = []
    currentNumber = str(number)
    firstNumbers = len(number) % 3
    if firstNumbers:
        ret.append(currentNumber[0:firstNumbers])
        currentNumber = currentNumber[firstNumbers:]
    while len(currentNumber) > 0:
        ret.append(currentNumber[0:3])
        currentNumber = currentNumber[3:]
    return ret


def say(number, byLine=False, latinOnly=False, delimiter='', shortScale=False, synonym=False):
    """
    Build the  world for given number.
    @param number The number to build (can be a string or int).
    @param byLine True, if a \n should be added between the parts of the spoken word.
    @param latinOnly If True build "123 millionen"; "einhundertdreiundzwanzingmillionen" otherwise.
    @param shortScale True, if the us system should be used.
    @return the word for given number.
    """
    number = str(number)
    if number in GERMAN_SMALL_NUMBERS:
        return GERMAN_SMALL_NUMBERS[number]
    blocks = _splitThousandBlocks(number)
    blocksLeft = len(blocks)
    ret = ""
    isFirstComponent = True
    for thousandBlock in blocks:
        try:
            if thousandBlock == "000":
                continue
            if latinOnly:
                if not byLine and not isFirstComponent:
                    ret += " "
                ret += str(int(thousandBlock))
                if blocksLeft > 1:
                    ret += " "
            else:
                ret += _sayGerman(thousandBlock, blocksLeft) + (delimiter if blocksLeft > 1 else '')
            if blocksLeft > 1:
                ret += sayByExp((blocksLeft - 1) * 3, plural=int(thousandBlock) > 1, delimiter=delimiter, shortScale=shortScale, synonym=synonym)
            if byLine:
                ret += os.linesep
        finally:
            blocksLeft -= 1
            isFirstComponent = False

    return ret
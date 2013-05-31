# -*- coding: iso-8859-1 -*-

# Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com
# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

import os

# German has a lot of exceptions during the first 20 numbers, so easiest thing is
# to collect them in a dict, instead of writing special code.
SMALL_NUMBERS = {
    '0': 'null',      '1': 'eins',       '2': 'zwei',       '3': 'drei',      '4': 'vier',
    '5': 'fünf',      '6': 'sechs',      '7': 'sieben',     '8': 'acht',      '9': 'neun',
    '10': 'zehn',     '11': 'elf',       '12': 'zwölf',     '13': 'dreizehn', '14': 'vierzehn',
    '15': 'fünfzehn', '16': 'sechszehn', '17': 'siebzehn',  '18': 'achtzehn', '19': 'neunzehn'}

# These are exceptions, building german 2 digit numbers like 72.
GERMAN_DEZI_EXCEPTIONS = {
    '2': 'zwan',
    '6': 'sech',
    '7': 'sieb'
}

# These are the prefixes to build latin numbers.
# @see http://de.wikipedia.org/wiki/Zahlennamen#Nomenklatur_f.C3.BCr_Zahlen_ab_1_000_000 for details.
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
    'quinquadezi': 'quindezi',
    'trezenti': 'treszenti'
}


def _sayLatin(number):
    """
    Build the latin word for given number.
    @param number int from 1 to 999.
    @return The latin word for given number.
    """
    if not 0 < number < 1000:
        raise ValueError("Number must be 1-999; given: [%s]." % number)

    one = number % 10
    ten = (number - one) % 100
    hundred = number - ten - one
    oneIndex, tenIndex, hundredIndex = one - 1, ten / 10 - 1, hundred / 100 - 1

    if ten == 0 and hundred == 0:
        return LATIN_PREFIXES[ALONE_ONES][oneIndex]
    if one == 0:
        if ten == 0:
            return LATIN_PREFIXES[HUNDREDS][hundredIndex][0]
        else:
            ret = LATIN_PREFIXES[TENS][tenIndex][0]
            return ret + LATIN_PREFIXES[HUNDREDS][hundredIndex][0] if hundred else ret

    onePrefix = LATIN_PREFIXES[COMBINE_ONES][oneIndex]

    def combineOnePrefix(one, other):
        """ Combine the one prefix, with a ten or hundred. """
        additionalCharacter = set(one[1:]).intersection(other[1:])
        ret = one[0] + (additionalCharacter.pop() if additionalCharacter else '') + other[0]
        return COMBINE_EXCEPTIONS.get(ret, ret)

    if ten == 0:
        return combineOnePrefix(onePrefix, LATIN_PREFIXES[HUNDREDS][hundredIndex])
    ret = combineOnePrefix(onePrefix, LATIN_PREFIXES[TENS][tenIndex])
    return ret + LATIN_PREFIXES[HUNDREDS][hundredIndex][0] if hundred else ret


def _sayLongLadder(zeros, plural=False):
    """
    Build the word for the number, starting with a 1, followed by as many 0 as specified in zeros.
    @param zeros the number of "0"s, following the "1". Must be 6 at least and zeros mod 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long ladder system.
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
            prefix = "ni"
        else:
            prefix = _sayLatin(current)
            # If we combine a ten prefix, without a hundred prefix, the 'a' changes to 'i' if present at last position.
            if 100 > current > 9 and prefix[-1] == "a":
                prefix = prefix[:-1] + 'i'
            sixes -= current
        # This is the prefix for separating the thousand blocks. We skip this, if this is the firs iteration.
        if ret:
            prefix += "lli"
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


def sayByExp(zeros, plural=False):
    """
    Build the word for the number, starting with a 1, followed by as many "0" as specified in zeros.
    @param zeros the number of "0", following the "1". Must be 3 at least and zeros % 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long ladder system if zeros > 3, german tausend otherwise.
    """
    if zeros < 3:
        raise ValueError('Zeros must be 3 or greater.')
    if zeros % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    if zeros == 3:
        ret = "tausend"
    else:
        ret = _sayLongLadder(zeros, plural)
    return ret


def _sayShortNumber(shortNumber, sayEin):
    """
    Helper to say a short number, that is used before another part (neunzehn millionen or eine million or ein tausend)
    @param sayEin True to say ein, instead of eine in case of shortNmuber == 1
    """
    if shortNumber == "1":
        return "ein" if sayEin else "eine"
    return SMALL_NUMBERS[shortNumber]


def _sayGerman(number, componentsLeft):
    """
    Helper to build the german word for given number.
    @param number Must be 0-999.
    """
    if not 0 <= int(number) <= 999:
        raise ValueError("Number must be 0-999")
    number = str(number)
    if number in SMALL_NUMBERS:
        return _sayShortNumber(number, componentsLeft == 2)
    currentLen = len(number)
    ret = ""
    if currentLen == 3:
        if not number[0] == "0":
            ret = _sayShortNumber(number[0], sayEin=True) + "hundert"
        return ret + _sayGerman(number[1:], componentsLeft)

    if number[0] == "0":
        if number[1] == "0":
            return ""
        return SMALL_NUMBERS[number[1]]
    if not number[1] == "0":
        ret = _sayShortNumber(number[1], sayEin=True) + "und"
    ret += GERMAN_DEZI_EXCEPTIONS.get(number[0], SMALL_NUMBERS[number[0]]) + "zig"
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


def say(number, byLine=False, latinOnly=False):
    """
    Build the german world for given number, using the long ladder system.
    @param number The number to build (can be a string or int).
    @param byLine True, if a \n should be added between the parts of the spoken word.
    @param latinOnly If True build "123 millionen"; "einhundertdreiundzwanzingmillionen" otherwise.
    @return the german word for given number.
    """
    number = str(number)
    if number in SMALL_NUMBERS:
        return SMALL_NUMBERS[number]
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
                ret += _sayGerman(thousandBlock, blocksLeft)
            if blocksLeft > 1:
                ret += sayByExp((blocksLeft - 1) * 3, plural=int(thousandBlock) > 1)
            if byLine:
                ret += os.linesep
        finally:
            blocksLeft -= 1
            isFirstComponent = False

    return ret
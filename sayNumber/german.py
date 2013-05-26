# -*- coding: iso-8859-1 -*-
import os

# German has a lot of exceptions during the first 20 numbers, so easiest thing is
# to collect them in a dict, instead of writing special code.
SMALL_NUMBERS = {
    '0': 'null',
    '1': 'eins',
    '2': 'zwei',
    '3': 'drei',
    '4': 'vier',
    '5': 'fünf',
    '6': 'sechs',
    '7': 'sieben',
    '8': 'acht',
    '9': 'neun',
    '10': 'zehn',
    '11': 'elf',
    '12': 'zwölf',
    '13': 'dreizehn',
    '14': 'vierzehn',
    '15': 'fünfzehn',
    '16': 'sechszehn',
    '17': 'siebzehn',
    '18': 'achtzehn',
    '19': 'neunzehn'}

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
    # 3: list of hundred prefixes
    [['zenti', 'n', 'x'], ['duzenti', 'n'], ['trezenti', 'n', 's'], ['quadringenti', 'n', 's'], ['quingenti', 'n', 's'],
     ['seszenti', 'n'], ['septingenti', 'n'], ['oktingenti', 'm', 'x'], ['nongenti', ]]
]


# There are two exceptions, building latin numbers
# 1. quinquadezi has a different name: quindezi
# 2. 103 would normally be trezenti, but this is reserved for 300. This is, why 103 is treszenti.
COMBINE_EXCEPTIONS = {
    'quinquadezi': 'quindezi',
    'trezenti': 'treszenti'
}


# These are exceptions, building 2 digit numbers like 72.
DECI_EXCEPTIONS = {
    '2': 'zwan',
    '6': 'sech',
    '7': 'sieb'
}


def sayLatin(number):
    """
    Build the latin word for given number.
    @param number an number from 1 to 999.
    @return The latin word for given number.
    """
    if number < 1 or number > 999:
        raise ValueError("Number must be 1-999.")

    def combineOnePrefix(one, other):
        """
        Combines the one prefix, with a ten or hundred.
        """
        ret = one[0] + other[0]
        for currentSpecial in one[1:]:
            if currentSpecial in other[1:]:
                ret = one[0] + currentSpecial + other[0]
                break

        return COMBINE_EXCEPTIONS.get(ret, ret)

    currentNumber = number
    one = currentNumber % 10
    currentNumber -= one
    ten = currentNumber % 100
    hundred = currentNumber - ten

    #TODO: I did not find something better, but there MUST be a more elegant way of combining the prefixes.
    if ten == 0 and hundred == 0:
        return LATIN_PREFIXES[0][one - 1]
    if one == 0:
        if ten == 0:
            return LATIN_PREFIXES[3][hundred / 100 - 1][0]
        else:
            ret = LATIN_PREFIXES[2][ten / 10 - 1][0]
            return ret + LATIN_PREFIXES[3][hundred / 100 - 1][0] if hundred > 0 else ret

    onePrefix = LATIN_PREFIXES[1][one - 1]
    if ten == 0:
        return combineOnePrefix(onePrefix, LATIN_PREFIXES[3][hundred / 100 - 1])
    ret = combineOnePrefix(onePrefix, LATIN_PREFIXES[2][ten / 10 - 1])
    return ret + LATIN_PREFIXES[3][hundred / 100 - 1][0] if hundred > 0 else ret


def sayLongLadder(zeros, plural=False):
    """
    Build the word for the number, starting with a 1, followed by as many 0 as specified in zeros.
    @param zeros the number of "0", following the "1". Must be 6 at least and zeros % 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long ladder system.
    """
    if zeros < 6:
        raise ValueError('Zeros must be 6 or greater.')
    if not zeros % 3 == 0:
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
            prefix = sayLatin(current)
            # If we combine a ten prefix, without a hundred prefix, the 'a' changes to 'i' if present at last position.
            if 100 > current > 9 and prefix[-1] == "a":
                prefix = prefix[:-1] + 'i'
            sixes -= current
        sixes /= 1000
        # This is the prefix for separating the thousand blocks. We skip this, if this is the firs iteration.
        if ret:
            prefix += "lli"
        ret = prefix + ret
    # Now add the postfix to make a word.
    if lliarde:
        ret += "lliarde"
        pluralPostfix = "n"
    else:
        ret += "llion"
        pluralPostfix = "en"
    if plural:
        ret += pluralPostfix
    return ret


def sayByExp(zeros, plural):
    """
    Build the word for the number, starting with a 1, followed by as many "0" as specified in zeros.
    @param zeros the number of "0", following the "1". Must be 3 at least and zeros % 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long ladder system if zeros > 3, german tausend otherwise.
    """
    if zeros < 3:
        raise ValueError('Zeros must be 3 or greater.')
    elif not zeros % 3 == 0:
        raise ValueError("Zeros mod 3 must be 0.")
    elif zeros == 3:
        ret = "tausend"
    else:
        ret = sayLongLadder(zeros, plural)
    return ret


def _sayDeci(digit):
    """
    Helper to build the german tens.
    """
    return DECI_EXCEPTIONS.get(digit, SMALL_NUMBERS[digit]) + "zig"


def _sayShortNumber(shortNumber, componentsLeft):
    """
    Helper to say a short number, that is used before another part (zwanzig millionen or eine million or ein tausend)
    """
    if shortNumber == "1" and componentsLeft > 0:
        return "ein" if componentsLeft == 2 else "eine"
    return SMALL_NUMBERS[shortNumber]


def _say999(number, componentsLeft):
    """
    Helper to build the german word for given number.
    @param number Must be 0-999.
    """
    if number in SMALL_NUMBERS:
        return _sayShortNumber(number, componentsLeft)
    currentLen = len(number)
    ret = ""
    if currentLen == 3:
        if not number[0] == "0":
            ret = _sayShortNumber(number[0], 2) + "hundert"
        return ret + _say999(number[1:], componentsLeft)

    if number[0] == "0":
        if number[1] == "0":
            return ""
        return SMALL_NUMBERS[number[1]]
    if not number[1] == "0":
        ret = _sayShortNumber(number[1], 2) + "und"
    ret += _sayDeci(number[0])
    return ret


def _split(number):
    """
    Helper that splits the given number to blocks of thousands.
    @return array of blocks. As lower the index, as higher the value.
    """
    ret = []
    currentNumber = number
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
    @param number The number to build.
    @param byLine True, if a \n should be added between the parts of the spoken word.
    @param latinOnly If True build "123 millionen"; "einhundertdreiundzwanzingmillionen" otherwise.
    @return the german word for given number.
    """
    number = str(number)
    if number in SMALL_NUMBERS:
        return SMALL_NUMBERS[number]
    components = _split(number)
    componentsLeft = len(components)
    ret = ""
    isFirstComponent = True
    for currentComponent in components:
        try:
            if currentComponent == "000":
                continue
            if latinOnly:
                if not byLine and not isFirstComponent:
                    ret += " "
                ret += str(int(currentComponent))
                if componentsLeft > 1:
                    ret += " "
            else:
                ret += _say999(currentComponent, componentsLeft)
            if componentsLeft > 1:
                ret += sayByExp((componentsLeft - 1) * 3, plural=int(currentComponent) > 1)
            if byLine:
                ret += os.linesep
        finally:
            componentsLeft -= 1
            isFirstComponent = False

    return ret
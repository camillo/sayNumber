# Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com
# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

import os
from logging import getLogger

latinLogger = getLogger("latin")


def _sayLatin(numberToSay, delimiter='', synonym=False, chuquet=False, **_):
    if not 0 <= numberToSay < 1000:
        raise ValueError("Number must be 0-999; given: [%s]." % numberToSay)

    from latinNumbers import LATIN_NUMBERS, LATIN_SYNONYMS, CHUQUET_PREFIXES
    if chuquet and numberToSay in CHUQUET_PREFIXES:
        latinLogger.debug("using chuquet prefix")
        target = CHUQUET_PREFIXES[numberToSay]
    elif synonym and numberToSay in LATIN_SYNONYMS:
        latinLogger.debug("using synonym")
        target = LATIN_SYNONYMS[numberToSay]
    else:
        latinLogger.debug("using normal latin prefix" + (
                          "; no chuquet prefix available" if chuquet
                          else "; no synonym available" if synonym
                          else ''))
        target = LATIN_NUMBERS[numberToSay]

    latinLogger.info("%s -> %s", numberToSay, "-".join(target))
    return delimiter.join(target)


def sayLatin(numberToSay, delimiter='', synonym=False, chuquet=False):
    """
    Combine the latin prefixes for given number.
    @param delimiter Separates the used prefixes if set.
    @param synonym Use sexdezillion, novemdezillion and quinquillion for sedezillion, novendezillion and quintillion.
    @param chuquet Use old latin prefixes like duodeviginti instead of oktodezi
    @return Combined prefixes, that can be used to make a word, by appending llion ord lliard.
    """
    numberToSay = int(numberToSay)
    if not 0 < numberToSay < 1000:
        raise ValueError("Number must be 1-999; given: [%s]." % numberToSay)
    return _sayLatin(numberToSay, delimiter, synonym, chuquet)


def _sayLongScale(zerosAfterOne, plural=False, delimiter='', **kwargs):
    """
    Build the word for the number, starting with a 1, followed by as many 0 as specified in zeros.
    @param zerosAfterOne the number of "0"s, following the "1". Must be 6 at least and zeros mod 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long scale system.
    """
    if zerosAfterOne < 6:
        raise ValueError('Zeros must be 6 or greater.')
    if zerosAfterOne % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    sixes, lliarde = divmod(zerosAfterOne, 6)
    ret = ""
    while sixes > 0:
        # We do one thousand block per iteration, starting with the the lowest value.
        current = sixes % 1000
        prefix = _sayLatin(current, delimiter, **kwargs)
        # If we combine a ten prefix, without a hundred prefix, the 'a' changes to 'i' if present at last position.
        if 100 > current > 9 and prefix[-1] == "a":
            prefix = prefix[:-1] + 'i'
        prefix += delimiter
        # This is the prefix for separating the thousand blocks. We skip this, if this is the first iteration.
        if ret:
            prefix += "lli" + delimiter
        ret = prefix + ret
        sixes -= current
        sixes /= 1000
    # Now add the postfix to make a word.
    if lliarde:
        ret += "lliard"
    else:
        ret += "llion"
    return ret + 's' if plural else ret


def _sayShortScale(zerosAfterOne, plural=False, **kwargs):
    """
    Build the word for the number, starting with a 1, followed by as many 0 as specified in zeros.
    @param zerosAfterOne the number of "0"s, following the "1". Must be 6 at least and zeros mod 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @return the word, using the long scale system.
    """
    if zerosAfterOne < 6:
        raise ValueError('Zeros must be 6 or greater.')
    if zerosAfterOne % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    longScaleZeros = 2 * zerosAfterOne - 6
    return _sayLongScale(longScaleZeros, plural=plural, **kwargs)


def sayByExp(zerosAfterOne, plural=False, shortScale=False, forceZ=False, forceC=False, **kwargs):
    """
    Build the word for the number, starting with a 1, followed by as many "0" as specified in zeros.
    @param zerosAfterOne the number of "0", following the "1". Must be 3 at least and zeros % 3 == 0.
    @param plural True, if the plural form should be returned, False for singular.
    @param shortScale True, to use us/uk system, german otherwise
    """
    if zerosAfterOne < 3:
        raise ValueError('Zeros must be 3 or greater.')
    if zerosAfterOne % 3 > 0:
        raise ValueError("Zeros mod 3 must be 0.")
    if zerosAfterOne == 3:
        ret = "thousand"
    elif shortScale:
        ret = _sayShortScale(zerosAfterOne, plural, **kwargs)
    else:
        ret = _sayLongScale(zerosAfterOne, plural, **kwargs)
    if forceC or (shortScale and not forceZ):
        ret = ret.replace("z", "c")
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


def say(number, byLine=False, forceSingular=False, forcePlural=False, **kwargs):
    """
    Build the  world for given number.
    @param number The number to build (can be a string or int).
    @param byLine True, if a \n should be added between the parts of the spoken word.
    @return the word for given number.
    """
    number = str(number)
    if number < 1000:
        return number
    blocks = _splitThousandBlocks(number)
    blocksLeft = len(blocks)
    ret = ""
    isFirstComponent = True
    for thousandBlock in blocks:
        try:
            if thousandBlock == "000":
                continue
            if not byLine and not isFirstComponent:
                ret += " "
            thousandValue = int(thousandBlock)
            ret += str(thousandValue)
            if blocksLeft > 1:
                ret += " "
                plural = forcePlural or (thousandValue > 1 and not forceSingular)
                ret += sayByExp((blocksLeft - 1) * 3, plural=plural, **kwargs)
            if byLine:
                ret += os.linesep
        finally:
            blocksLeft -= 1
            isFirstComponent = False

    return ret
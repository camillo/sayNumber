# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

import string
from logging import getLogger, INFO
from latinNumbers import LATIN_NUMBERS, LATIN_SYNONYMS, CHUQUET_PREFIXES

logger = getLogger(__name__)


def sayLatin(numberToSay, delimiter='', synonym=False, chuquet=False, **_):
    if not 0 <= numberToSay < 1000:
        raise ValueError("Number must be 0-999; given: [%s]." % numberToSay)

    if chuquet and numberToSay in CHUQUET_PREFIXES:
        logger.debug("using chuquet prefix")
        target = CHUQUET_PREFIXES[numberToSay]
    elif synonym and numberToSay in LATIN_SYNONYMS:
        logger.debug("using synonym")
        target = LATIN_SYNONYMS[numberToSay]
    else:
        logger.debug("using normal latin prefix")
        target = LATIN_NUMBERS[numberToSay]
    if logger.isEnabledFor(INFO):
        logger.info("%s -> %s", numberToSay, "-".join(target))
    return delimiter.join(target)


# *************************************************************************
# * Following staff is generating the source code of latinNumbers.py.     *
# * If you want to understand, how the Latin numbers get build, go ahead. *

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


def _sayLatin(numberToSay, delimiter=''):
    """
    Build the latin word for given number.
    @param numberToSay int from 1 to 999.
    @param delimiter Separates the prefixes
    @return The latin word for given number.
    """
    if not 0 < numberToSay < 1000:
        raise ValueError("Number must be 1-999; given: [%s]." % numberToSay)
    if delimiter and delimiter in string.ascii_lowercase:
        raise ValueError("Delimiter must not be a-z.")
    logger.debug("say latin: %s", numberToSay)

    one = numberToSay % 10
    ten = (numberToSay - one) % 100
    hundred = numberToSay - ten - one

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


if __name__ == "__main__":
    # If you start this script (python latin.py), the dicts in latinNumbers.py get generated. We do this precalculation
    # to save time, building REALLY(!) big numbers.

    ret = """# Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com
# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

# This file is auto generated, running python latin.py.
# Changes to this file will be overridden without warning, when running latin.py again (will not happen automatically).

# These are valid synonyms, that can be used.
LATIN_SYNONYMS = {
    5: ['quinqui', ],
    16: ['sex', 'dezi'],
    19: ['novem', 'dezi'],
}

# This are the prefixes, using old latin numbers as invented by Nicolas Chuquet
CHUQUET_PREFIXES = {
    18: ['duo', 'de', 'viginti'],
    19: ['un', 'de', 'viginti'],
    28: ['duo', 'de', 'triginta'],
    29: ['un', 'de', 'triginta'],
    38: ['duo', 'de', 'quadraginta'],
    39: ['un', 'de', 'quadraginta'],
    48: ['duo', 'de', 'quinquaginta'],
    49: ['un', 'de', 'quinquaginta'],
    58: ['duo', 'de', 'sexaginta'],
    59: ['un', 'de', 'sexaginta'],
    68: ['duo', 'de', 'septuaginta'],
    69: ['un', 'de', 'septuaginta'],
    78: ['duo', 'de', 'octoginta'],
    79: ['un', 'de', 'octoginta'],
    88: ['duo', 'de', 'nonaginta'],
    89: ['un', 'de', 'nonaginta'],
    98: ['duo', 'de', 'centi'],
    99: ['un', 'de', 'centi'],
}

# This are the combined prefixes to use for numbers 1 to 999; plus the standalone prefix 'ni' for 000
"""
    ret += "LATIN_NUMBERS = {\r"
    ret += "    0: ['ni'],\r"
    for number in range(1, 1000):
        latin = _sayLatin(number, delimiter='-')
        line = "    %d: [" % number
        for component in latin.split('-'):
            line += "'%s', " % component
        line += "],"
        ret += line + "\r"
    ret += "}"
    with open('latinNumbers.py', 'w') as sourceCode:
        sourceCode.write(ret)

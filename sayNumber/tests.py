# Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com
# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

import unittest
from backend import say, sayByExp, _splitThousandBlocks, _sayLongScale
from latin import sayLatin as _sayLatin


class TestInternal(unittest.TestCase):
    def testSplit(self):
        split = _splitThousandBlocks('1')
        self.assertEqual(1, len(split))
        self.assertEqual('1', split[0])
        split = _splitThousandBlocks('42')
        self.assertEqual(1, len(split))
        self.assertEqual('42', split[0])
        split = _splitThousandBlocks('100')
        self.assertEqual(1, len(split))
        self.assertEqual('100', split[0])
        split = _splitThousandBlocks('1000')
        self.assertEqual(2, len(split))
        self.assertEqual('1', split[0])
        self.assertEqual('000', split[1])
        split = _splitThousandBlocks('4221')
        self.assertEqual(2, len(split))
        self.assertEqual('4', split[0])
        self.assertEqual('221', split[1])
        split = _splitThousandBlocks('4221777')
        self.assertEqual(3, len(split))
        self.assertEqual('4', split[0])
        self.assertEqual('221', split[1])
        self.assertEqual('777', split[2])

    def testLatinConsistence(self):
        numbers = []
        for current in range(1, 1000):
            currentNumber = _sayLatin(current)
            if currentNumber in numbers:
                self.fail("%s already in list [%s]" % (currentNumber, current))
            numbers.append(currentNumber)


class Test1000To9999999(unittest.TestCase):

    def test1000(self):
        self.assertEqual(say('1000'), '1 thousand')

    def test1001(self):
        self.assertEqual(say('1001'), '1 thousand 1')

    def test42721(self):
        self.assertEqual(say('42721'), '42 thousand 721')


class TestE6ToE18(unittest.TestCase):

    def testE6(self):
        self.assertEqual(say('1000000'), '1 million')
        self.assertEqual(say('1000001'), '1 million 1')

    def testE9(self):
        self.assertEqual(say('1000000000'), '1 milliard')
        self.assertEqual(say('2000000000'), '2 milliards')
        self.assertEqual(say('2100000000'), '2 milliards 100 millions')


class TestLatin(unittest.TestCase):

    def testOnes(self):
        self.assertEqual('mi', _sayLatin(1))
        self.assertEqual('bi', _sayLatin(2))
        self.assertEqual('tri', _sayLatin(3))
        self.assertEqual('quadri', _sayLatin(4))
        self.assertEqual('quinti', _sayLatin(5))
        self.assertEqual('sexti', _sayLatin(6))
        self.assertEqual('septi', _sayLatin(7))
        self.assertEqual('okti', _sayLatin(8))
        self.assertEqual('noni', _sayLatin(9))

    def testTens(self):
        self.assertEqual('dezi', _sayLatin(10))
        self.assertEqual('viginti', _sayLatin(20))
        self.assertEqual('triginta', _sayLatin(30))
        self.assertEqual('quadraginta', _sayLatin(40))
        self.assertEqual('quinquaginta', _sayLatin(50))
        self.assertEqual('sexaginta', _sayLatin(60))
        self.assertEqual('septuaginta', _sayLatin(70))
        self.assertEqual('oktoginta', _sayLatin(80))
        self.assertEqual('nonaginta', _sayLatin(90))

    def testHundert(self):
        self.assertEqual('zenti', _sayLatin(100))
        self.assertEqual('duzenti', _sayLatin(200))
        self.assertEqual('trezenti', _sayLatin(300))
        self.assertEqual('quadringenti', _sayLatin(400))
        self.assertEqual('quingenti', _sayLatin(500))
        self.assertEqual('seszenti', _sayLatin(600))
        self.assertEqual('septingenti', _sayLatin(700))
        self.assertEqual('oktingenti', _sayLatin(800))
        self.assertEqual('nongenti', _sayLatin(900))

    def testOnePrefixes(self):
        self.assertEqual('duoquadraginta', _sayLatin(42))
        self.assertEqual('sesviginti', _sayLatin(26))
        self.assertEqual('septensexaginta', _sayLatin(67))
        self.assertEqual('sesquadringenti', _sayLatin(406))
        self.assertEqual('sesexagintaseszenti', _sayLatin(666))

    def testOneExceptions(self):
        self.assertEqual('quindezi', _sayLatin(15))
        self.assertEqual('treszenti', _sayLatin(103))

    def testOther(self):
        self.assertEqual('dezizenti', _sayLatin(110))

    def testSynonyms(self):
        self.assertEqual('sedezi', _sayLatin(16))
        self.assertEqual('sexdezi', _sayLatin(16, synonym=True))
        self.assertEqual('sex-dezi', _sayLatin(16, delimiter='-', synonym=True))

        self.assertEqual('novendezi', _sayLatin(19))
        self.assertEqual('novemdezi', _sayLatin(19, synonym=True))

        self.assertEqual('quinti', _sayLatin(5))
        self.assertEqual('quinqui', _sayLatin(5, synonym=True))


class LongScaleTest(unittest.TestCase):
    def testForceC(self):
        self.assertEqual('duocentillion', sayByExp(612, forceC=True))

    def test6000(self):
        self.assertEqual('millinillion', _sayLongScale(6000))
        self.assertEqual('millinillinillion', _sayLongScale(6000000))
        self.assertEqual('millinillinilliard', _sayLongScale(6000003))
        self.assertEqual('nonillinovenonagintanongentillion', _sayLongScale(59994))

    def testWordPrefix(self):
        self.assertEqual('million', _sayLongScale(6))
        self.assertEqual('millions', _sayLongScale(6, True))
        self.assertEqual('milliard', _sayLongScale(9))
        self.assertEqual('milliards', _sayLongScale(9, True))

    def testTenWithoutHundred(self):
        self.assertEqual('trigintillion', _sayLongScale(180))


class ShortScaleTest(unittest.TestCase):
    def testTo303(self):
        self.assertEqual('million', sayByExp(6, shortScale=True))
        self.assertEqual('billion', sayByExp(9, shortScale=True))
        self.assertEqual('trillion', sayByExp(12, shortScale=True))
        self.assertEqual('quadrillion', sayByExp(15, shortScale=True))
        self.assertEqual('septendecillion', sayByExp(54, shortScale=True))
        self.assertEqual('quadragintillion', sayByExp(123, shortScale=True))
        self.assertEqual('centillion', sayByExp(303, shortScale=True))
        self.assertEqual('duocentillion', sayByExp(309, shortScale=True))

    def testForceZ(self):
        self.assertEqual('duozentillion', sayByExp(309, shortScale=True, forceZ=True))


class DelimiterTest(unittest.TestCase):
    def testTresZenti(self):
        self.assertEqual('tres-zenti', _sayLatin(103, delimiter="-"))

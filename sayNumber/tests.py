# -*- coding: iso-8859-1 -*-
import unittest
from german import say, _split, _sayLatin, _sayLongLadder


class TestInternal(unittest.TestCase):
    def testSplit(self):
        split = _split('1')
        self.assertEqual(1, len(split))
        self.assertEqual('1', split[0])
        split = _split('42')
        self.assertEqual(1, len(split))
        self.assertEqual('42', split[0])
        split = _split('100')
        self.assertEqual(1, len(split))
        self.assertEqual('100', split[0])
        split = _split('1000')
        self.assertEqual(2, len(split))
        self.assertEqual('1', split[0])
        self.assertEqual('000', split[1])
        split = _split('4221')
        self.assertEqual(2, len(split))
        self.assertEqual('4', split[0])
        self.assertEqual('221', split[1])
        split = _split('4221777')
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


class TestTo12(unittest.TestCase):
    def test0isNull(self):
        self.assertEqual(say('0'), 'null')

    def test1isEins(self):
        self.assertEqual(say('1'), 'eins')

    def test2isZwei(self):
        self.assertEqual(say('2'), 'zwei')

    def test3isDrei(self):
        self.assertEqual(say('3'), 'drei')

    def test4isVier(self):
        self.assertEqual(say('4'), 'vier')

    def test5isFuenf(self):
        self.assertEqual(say('5'), 'fünf')

    def test6isSechs(self):
        self.assertEqual(say('6'), 'sechs')

    def test7isSieben(self):
        self.assertEqual(say('7'), 'sieben')

    def test8isAcht(self):
        self.assertEqual(say('8'), 'acht')

    def test9isNeun(self):
        self.assertEqual(say('9'), 'neun')

    def test10isZehn(self):
        self.assertEqual(say('10'), 'zehn')

    def test11isElf(self):
        self.assertEqual(say('11'), 'elf')

    def test12isZehn(self):
        self.assertEqual(say('12'), 'zwölf')


class Test13To19(unittest.TestCase):

    def test13(self):
        self.assertEqual(say('13'), 'dreizehn')

    def test14(self):
        self.assertEqual(say('14'), 'vierzehn')

    def test15(self):
        self.assertEqual(say('15'), 'fünfzehn')

    def test16(self):
        self.assertEqual(say('16'), 'sechszehn')

    def test17(self):
        self.assertEqual(say('17'), 'siebzehn')

    def test18(self):
        self.assertEqual(say('18'), 'achtzehn')

    def test19(self):
        self.assertEqual(say('19'), 'neunzehn')


class Test20To99(unittest.TestCase):

    def test20(self):
        self.assertEqual(say('20'), 'zwanzig')

    def test21(self):
        self.assertEqual(say('21'), 'einundzwanzig')

    def test39(self):
        self.assertEqual(say('39'), 'neununddreizig')

    def test62(self):
        self.assertEqual(say('62'), 'zweiundsechzig')

    def test75(self):
        self.assertEqual(say('75'), 'fünfundsiebzig')

    def test80(self):
        self.assertEqual(say('80'), 'achtzig')

    def test99(self):
        self.assertEqual(say('99'), 'neunundneunzig')


class Test100To999(unittest.TestCase):

    def test100(self):
        self.assertEqual(say('100'), 'einhundert')

    def test101(self):
        self.assertEqual(say('101'), 'einhunderteins')

    def test400(self):
        self.assertEqual(say('400'), 'vierhundert')

    def test666(self):
        self.assertEqual(say('666'), 'sechshundertsechsundsechzig')

    def test987(self):
        self.assertEqual(say('987'), 'neunhundertsiebenundachtzig')


class Test1000To9999999(unittest.TestCase):

    def test1000(self):
        self.assertEqual(say('1000'), 'eintausend')

    def test1001(self):
        self.assertEqual(say('1001'), 'eintausendeins')

    def test42721(self):
        self.assertEqual(say('42721'), 'zweiundvierzigtausendsiebenhunderteinundzwanzig')

    def test999999(self):
        self.assertEqual(say('999999'), 'neunhundertneunundneunzigtausendneunhundertneunundneunzig')


class TestE6ToE18(unittest.TestCase):

    def testE6(self):
        self.assertEqual(say('1000000'), 'einemillion')
        self.assertEqual(say('1000001'), 'einemillioneins')

    def testE9(self):
        self.assertEqual(say('1000000000'), 'einemilliarde')
        self.assertEqual(say('2000000000'), 'zweimilliarden')
        self.assertEqual(say('2100000000'), 'zweimilliardeneinhundertmillionen')


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

    def testOther(self):
        self.assertEqual('dezizenti', _sayLatin(110))

    def testOneExceptions(self):
        self.assertEqual('quindezi', _sayLatin(15))
        self.assertEqual('treszenti', _sayLatin(103))


class LongLadderTest(unittest.TestCase):
    def test6000(self):
        self.assertEqual('millinillion', _sayLongLadder(6000))
        self.assertEqual('millinillinillion', _sayLongLadder(6000000))
        self.assertEqual('millinillinilliarde', _sayLongLadder(6000003))
        self.assertEqual('nonillinovenonagintanongentillion', _sayLongLadder(59994))

    def testWordPrefix(self):
        self.assertEqual('million', _sayLongLadder(6))
        self.assertEqual('millionen', _sayLongLadder(6, True))
        self.assertEqual('milliarde', _sayLongLadder(9))
        self.assertEqual('milliarden', _sayLongLadder(9, True))

    def testTenWithoutHundred(self):
        self.assertEqual('trigintillion', _sayLongLadder(180))
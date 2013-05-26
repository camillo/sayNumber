# -*- coding: iso-8859-1 -*-
import unittest
from german import say, _split, sayLatin, sayLongLadder


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
            currentNumber = sayLatin(current)
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
        self.assertEqual('mi', sayLatin(1))
        self.assertEqual('bi', sayLatin(2))
        self.assertEqual('tri', sayLatin(3))
        self.assertEqual('quadri', sayLatin(4))
        self.assertEqual('quinti', sayLatin(5))
        self.assertEqual('sexti', sayLatin(6))
        self.assertEqual('septi', sayLatin(7))
        self.assertEqual('okti', sayLatin(8))
        self.assertEqual('noni', sayLatin(9))

    def testTens(self):
        self.assertEqual('dezi', sayLatin(10))
        self.assertEqual('viginti', sayLatin(20))
        self.assertEqual('triginta', sayLatin(30))
        self.assertEqual('quadraginta', sayLatin(40))
        self.assertEqual('quinquaginta', sayLatin(50))
        self.assertEqual('sexaginta', sayLatin(60))
        self.assertEqual('septuaginta', sayLatin(70))
        self.assertEqual('oktoginta', sayLatin(80))
        self.assertEqual('nonaginta', sayLatin(90))

    def testHundert(self):
        self.assertEqual('zenti', sayLatin(100))
        self.assertEqual('duzenti', sayLatin(200))
        self.assertEqual('trezenti', sayLatin(300))
        self.assertEqual('quadringenti', sayLatin(400))
        self.assertEqual('quingenti', sayLatin(500))
        self.assertEqual('seszenti', sayLatin(600))
        self.assertEqual('septingenti', sayLatin(700))
        self.assertEqual('oktingenti', sayLatin(800))
        self.assertEqual('nongenti', sayLatin(900))

    def testOnePrefixes(self):
        self.assertEqual('duoquadraginta', sayLatin(42))
        self.assertEqual('sesviginti', sayLatin(26))
        self.assertEqual('septensexaginta', sayLatin(67))
        self.assertEqual('sesquadringenti', sayLatin(406))
        self.assertEqual('sesexagintaseszenti', sayLatin(666))

    def testOther(self):
        self.assertEqual('dezizenti', sayLatin(110))

    def testQuindezi(self):
        self.assertEqual('quindezi', sayLatin(15))

    def testTreszenti(self):
        self.assertEqual('treszenti', sayLatin(103))


class LongLadderTest(unittest.TestCase):
    def test6000(self):
        self.assertEqual('millinillion', sayLongLadder(6000))
        self.assertEqual('millinillinillion', sayLongLadder(6000000))
        self.assertEqual('millinillinilliarde', sayLongLadder(6000003))
        self.assertEqual('nonillinovenonagintanongentillion', sayLongLadder(59994))
        self.assertEqual('million', sayLongLadder(6))
        self.assertEqual('millionen', sayLongLadder(6, True))
        self.assertEqual('milliarde', sayLongLadder(9))
        self.assertEqual('milliarden', sayLongLadder(9, True))

    def testTenWithoutHundred(self):
        self.assertEqual('trigintillion', sayLongLadder(180))
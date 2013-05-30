#!/usr/bin/env python

import argparse
import random
from german import say, sayByExp


EXAMPLES = """Examples

say.py 123
einhundertdreiundzwanzig

say.py --zeros 123
vigintilliarde

say.py --random 123
siebenhundertvierundsechzigvigintillioneneinhundertvierzignovendezilliardene ... izigtausenddreihundertvierzehn

say.py --random --latinOnly 123
398 vigintillionen 249 novendezilliarden 87 novendezillionen 534 oktodezilliarden 809 oktodezillionen ...

say.py --random --latinOnly --byLine 123
923 vigintillionen
910 novendezilliarden
...

say.py --random --latinOnly --numeric 123
217764231953087899423934113226947903488766240424414874685303342506908446655767312941208736464299524772777802411207853347868
===
217 vigintillionen 764 novendezilliarden 231 novendezillionen 953 oktodezilliarden 87 oktodezillionen ..."""


def main(args):
    number = args.number[0]
    if args.zeros:
        # Do not say given number, but the number with that many zeros.
        zeros, zerosLeft = divmod(number, 3)
        zeros *= 3
        ret = ""
        plural = False
        if zerosLeft:
            ret = "1%s " % "".join(["0" for _ in range(int(zerosLeft))])
            plural = True
        ret += sayByExp(zeros, plural)
        numeric = "1" + "0" * number
    elif args.random:
        # Do not say given number, but a random number with that many digits.
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        numeric = random.choice(digits)
        digits.append('0')
        numeric += "".join([random.choice(digits) for _ in range(number - 1)])
        ret = say(numeric, byLine=args.byLine, latinOnly=args.latinOnly)
    else:
        ret = say(number, byLine=args.byLine, latinOnly=args.latinOnly)
        numeric = number
    if args.numeric:
        ret = "%s\n===\n%s" % (numeric, ret)
    print ret.decode('iso-8859-1')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Write german names of (very) big numbers, using long ladder system.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=EXAMPLES)
    parser.add_argument('--byLine', '-b', dest='byLine', action='store_true',
                        help='Write components line by line.')
    parser.add_argument('--latinOnly', '-l', dest='latinOnly', action='store_true',
                        help='Say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"')
    parser.add_argument('--zeros', '-z', dest='zeros', action='store_true',
                        help='Do not say given number, but the number with that many zeros.')
    parser.add_argument('--random', '-r', dest='random', action='store_true',
                        help='Do not say given number, but a random number with that many digits.')
    parser.add_argument('--numeric', '-n', dest='numeric', action='store_true',
                        help="Say the number also in numeric form.")
    parser.add_argument('number', nargs=1, type=int, help='The number to say.')

    args = parser.parse_args()
    try:
        if args.zeros and args.random:
            raise ValueError("Options random and zeros cannot be combined.")

        main(args)
    except Exception as ex:
        print ex.message
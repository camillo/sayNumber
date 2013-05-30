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


class ArgFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _format_usage(self, usage, actions, groups, prefix):
        ret = super(argparse.ArgumentDefaultsHelpFormatter, self)._format_usage(usage, actions, groups, prefix)
        return ret.replace("[number]", "number")


def main(args):
    number = args.number
    if args.zeros:
        # Do not say given number, but the number with that many zeros.
        zeros, zerosLeft = divmod(number, 3)
        zeros *= 3
        ret = ""
        plural = False
        if zerosLeft:
            ret = ("10" if zerosLeft == 1 else "100") + " "
            plural = True
        ret += sayByExp(zeros, plural)
        numeric = "1" + "0" * number if args.numeric else None
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
                                     formatter_class=ArgFormatter,
                                     epilog="Use -e to see examples.")
    parser.add_argument('-e', '--example', dest='example', action='store_true',
                        help='show examples and exit')
    parser.add_argument('-b', '--byLine', dest='byLine', action='store_true',
                        help='Write components line by line.')
    parser.add_argument('-l', '--latinOnly', dest='latinOnly', action='store_true',
                        help='Say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"')
    parser.add_argument('-z', '--zeros', dest='zeros', action='store_true',
                        help='Do not say given number, but the number with that many zeros.')
    parser.add_argument('-r', '--random', dest='random', action='store_true',
                        help='Do not say given number, but a random number with that many digits.')
    parser.add_argument('-n', '--numeric', dest='numeric', action='store_true',
                        help="Say the number also in numeric form.")
    parser.add_argument('number', nargs='?', type=int, default=-1, help='The number to say.')

    args = parser.parse_args()

    try:
        if args.example:
            parser.exit(message=EXAMPLES)
        if args.number < 0:
            raise ValueError("Missing argument number.")
        if args.zeros and args.random:
            raise ValueError("Options random and zeros cannot be combined.")
        main(args)
    except Exception as ex:
        parser.error(ex.message)

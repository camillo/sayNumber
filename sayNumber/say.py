#!/usr/bin/env python
import argparse
import random
from german import say, sayByExp


class ExampleAction(argparse._HelpAction):
    """Write the examples and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        parser.exit(message="""
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
217 vigintillionen 764 novendezilliarden 231 novendezillionen 953 oktodezilliarden 87 oktodezillionen ...""")


def main(args):
    number = args.number[0]
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
    def atLeastZero(value):
        try:
            ret = int(value)
            if ret < 0:
                raise argparse.ArgumentTypeError("Value must be 0 or greater.")
            return ret
        except ValueError:
            raise argparse.ArgumentTypeError("not a number: '%s'" % value)

    parser = argparse.ArgumentParser(description='Write german names of (very) big numbers, using long ladder system.',
                                     epilog="Use -e to see examples.")
    parser.add_argument('-e', '--example', action=ExampleAction, dest='example', default=argparse.SUPPRESS,
                        help='show examples and exit')
    parser.add_argument('-b', '--byLine', dest='byLine', action='store_true',
                        help='write components line by line')
    parser.add_argument('-l', '--latinOnly', dest='latinOnly', action='store_true',
                        help='say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"')
    buildGroup = parser.add_mutually_exclusive_group()
    buildGroup.add_argument('-z', '--zeros', dest='zeros', action='store_true',
                            help='do not say given number, but the number with that many zeros.')
    buildGroup.add_argument('-r', '--random', dest='random', action='store_true',
                            help='do not say given number, but a random number with that many digits.')
    parser.add_argument('-n', '--numeric', dest='numeric', action='store_true',
                        help="say the number also in numeric form.")
    parser.add_argument('number', nargs=1, type=atLeastZero, help='The number to say.')

    args = parser.parse_args()

    try:
        main(args)
    except Exception as ex:
        print "error, executing command: " + ex.message
        import sys
        sys.exit(1)
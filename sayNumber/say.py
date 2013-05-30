#!/usr/bin/env python

import argparse
import random
from german import say, sayByExp


def main(args):
    number = args.number[0]
    if args.zeros:
        # Do not say given number, but the number with that many zeros.
        zeros, zerosLeft = divmod(number, 3)
        zeros *= 3
        ret = ""
        plural = False
        if zerosLeft:
            ret = "1" + "".join(["0" for _ in range(zerosLeft)]) + " "
            plural = True
        ret += sayByExp(zeros, plural)
        print ret
    elif args.random:
        # Do not say given number, but a random number with that many digits.
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        randomNumber = random.choice(digits)
        digits.append('0')
        randomNumber += "".join([random.choice(digits) for _ in range(number - 1)])
        print say(randomNumber, byLine=args.byLine, latinOnly=args.latinOnly)
    else:
        print say(number, byLine=args.byLine, latinOnly=args.latinOnly)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Write german names of (very) big numbers, using long ladder system.')
    parser.add_argument('--byLine', dest='byLine', action='store_true',
                        help='Write components line by line.')
    parser.add_argument('--latinOnly', dest='latinOnly', action='store_true',
                        help='Say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"')
    parser.add_argument('--zeros', dest='zeros', action='store_true',
                        help='Do not say given number, but the number with that many zeros.')
    parser.add_argument('--random', dest='random', action='store_true',
                        help='Do not say given number, but a random number with that many digits.')
    parser.add_argument('number', nargs=1, type=int, help='The number to say.')

    args = parser.parse_args()
    try:
        if args.zeros and args.random:
            raise ValueError("Options random and zeros cannot be combined.")

        main(args)
    except Exception as ex:
        print ex.message


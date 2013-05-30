#!/usr/bin/env python

# Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com
# This program is free software; find details in file LICENCE or here:
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

import argparse
import random
from german import say, sayByExp

VERSION = "1.0"


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
217 vigintillionen 764 novendezilliarden 231 novendezillionen 953 oktodezilliarden 87 oktodezillionen ...

say.py --random --latinOnly --numeric --grouping 123
695.128.681.352.561.722.639.169 ...
===
695 vigintillionen 128 novendezilliarden  ...
""")

COPYRIGHT = "Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com"


class LicenceAction(argparse._HelpAction):
    """ Show licence and exit """
    def __call__(self, parser, namespace, values, option_string=None):
        parser.exit(message=COPYRIGHT + """\n
    Find full licence in file LICENCE or use option -C/--fullLicence

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
""")


class FullLicenceAction(argparse._HelpAction):
    """ Show full licence and exit """
    def __call__(self, parser, namespace, values, option_string=None):
        import os
        myDir = os.path.abspath(os.path.dirname(__file__))
        try:
            with open(os.path.join(myDir, 'LICENSE'), 'r') as licenceFile:
                parser.exit(message=COPYRIGHT + "\n" + licenceFile.read())
        except IOError:
            parser.error("Licence file not found. Find licence here: http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt")


class GroupingAction(argparse._StoreTrueAction):
    """ Add numeric option, if grouping is used """
    def __call__(self, parser, args, values, option=None):
        args.grouping = True
        args.numeric = True


def main(args):
    number = args.number[0]
    if args.zeros:
        # Do not say given number, but the number with that many zeros.
        zeros, zerosLeft = divmod(number, 3)
        zeros *= 3
        ret = ("10" if zerosLeft == 1 else "100") + " " if zerosLeft else ""
        ret += sayByExp(zeros, zerosLeft)
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
        import locale
        locale.setlocale(locale.LC_NUMERIC, '')
        print locale.format("%d", int(numeric), grouping=args.grouping) + "\n==="
    print ret.decode('latin-1')


if __name__ == "__main__":
    def atLeastZero(value):
        try:
            ret = int(value)
            if ret < 0:
                raise argparse.ArgumentTypeError("Value must be 0 or greater.")
            return ret
        except ValueError:
            raise argparse.ArgumentTypeError("not a number: '%s'" % value)

    parser = argparse.ArgumentParser(description='Write german names of (very) big numbers.',
                                     epilog="Please report bugs to daniel.marohn@gmail.com.\nFind more information here: http://de.wikipedia.org/wiki/Zahlennamen",
                                     formatter_class=argparse.RawTextHelpFormatter, add_help=False)

    group = parser.add_argument_group('help')
    group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                       help="show this help message and exit")
    group.add_argument('-e', '--example', action=ExampleAction, dest='example', default=argparse.SUPPRESS,
                       help='show examples and exit')
    group.add_argument('-v', '--version', action='version', version=VERSION)
    group.add_argument('-c', '--licence', action=LicenceAction, default=argparse.SUPPRESS,
                       help="show licence information and exit")
    group.add_argument('-C', '--fullLicence', action=FullLicenceAction, default=argparse.SUPPRESS,
                       help="show full licence and exit")

    group = parser.add_argument_group('optional arguments')
    group.add_argument('-n', '--numeric', dest='numeric', action='store_true',
                       help="say the number also in numeric form")

    group = parser.add_argument_group('format')
    group.add_argument('-b', '--byLine', dest='byLine', action='store_true',
                       help='write components line by line')
    group.add_argument('-l', '--latinOnly', dest='latinOnly', action='store_true',
                       help='say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"')
    group.add_argument('-g', '--grouping', dest='grouping', action=GroupingAction,
                       help="group thousand blocks; implicit using -n")

    group = parser.add_argument_group('number')
    buildGroup = group.add_mutually_exclusive_group()
    buildGroup.add_argument('-z', '--zeros', dest='zeros', action='store_true',
                            help='do not say given number, but the number with that many zeros')
    buildGroup.add_argument('-r', '--random', dest='random', action='store_true',
                            help='do not say given number, but a random number with that many digits')
    parser.add_argument('number', nargs=1, type=atLeastZero, help='the number to say')

    args = parser.parse_args()

    try:
        main(args)
    except Exception as ex:
        print "error, executing command: " + ex.message
        import sys
        sys.exit(1)
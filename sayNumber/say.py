#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

COPYRIGHT = "Copyright (C) 2013 Daniel Marohn - daniel.marohn@gmail.com"
VERSION = "1.0"
# This program is free software; find details in file LICENCE or here:
# https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE

import sys
import argparse


class MessageAction(argparse._HelpAction):
    """ Write a message and exit. """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            parser.exit(message=self.message())
        except Exception as ex:
            parser.error(ex.message)

    def message(self):
        raise NotImplementedError("not implemented yet.")


class ExampleAction(MessageAction):
    """Write the examples and exit."""

    def message(self):
        return """
say.py 123
einhundertdreiundzwanzig

say.py 9999999345349583045894
neuntrilliardenneunhundertneunundneunzigtrillionenneunhundertneunundneunzigbilli
ardendreihundertf�nfundvierzigbillionendreihundertneunundvierzigmilliardenf�nfhu
ndertdreiundachtzigmillionenf�nfundvierzigtausendachthundertvierundneunzig

say.py --zeros 123
vigintilliarde

say.py --zeros 1000000
10 sesexagintazentillisesexagintaseszentilliarden

say.py --zeros 9999999345349583045894
100 millisesexagintaseszentillisesexagintaseszentilliseptenquinquagintaquingenti
llioktoquinquagintaquingentillitresexagintaduzentilliquadragintaoktingentilliduo
oktogintanongentillionen

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
217 vigintillionen 764 novendezilliarden 231 novendezillionen 953 oktodezilliarden 87 oktodezillionen ...

say.py --random --latinOnly --numeric --grouping 123
695.128.681.352.561.722.639.169 ...
695 vigintillionen 128 novendezilliarden  ...

say.py --googol --numeric --grouping
10.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000
zehnsedezilliarden

say.py --googolplex
10 millisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentillisesexagintaseszentilliarden
"""


class LicenceAction(MessageAction):
    """ Show licence and exit """
    def message(self):
        return COPYRIGHT + """\n
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
"""


class FullLicenceAction(MessageAction):
    """ Show full licence and exit """
    def message(self):
        import os
        myDir = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(myDir, 'LICENSE')
        try:
            with open(filename, 'r') as licenceFile:
                return COPYRIGHT + "\n" + licenceFile.read()
        except IOError:
            # noinspection PyBroadException
            try:
                import httplib
                conn = httplib.HTTPSConnection("raw.github.com")
                conn.request("GET", "/camillo/sayNumber/master/sayNumber/LICENSE")
                response = conn.getresponse()
                if response.status == httplib.OK:
                    licence = response.read()
                    try:
                        with open(filename, 'w') as licenceFile:
                            licenceFile.write(licence)
                    except IOError:
                        pass
                    return COPYRIGHT + "\n%s" % licence
                else:
                    raise Exception("no 200 OK [%s %s]" % (response.status, response.reason))
            except Exception as _:
                raise Exception("Licence file not found. Find licence here: https://raw.github.com/camillo/sayNumber/master/sayNumber/LICENSE")


class GroupingAction(argparse._StoreTrueAction):
    """ Add numeric option, if grouping is used """
    def __call__(self, parser, args, values, option=None):
        args.grouping = True
        args.numeric = True


def atLeastZero(value):
    """ Check that value is numeric and >0 """
    try:
        ret = int(value)
        if ret < 0:
            raise argparse.ArgumentTypeError("Value must be 0 or greater.")
        return ret
    except ValueError:
        raise argparse.ArgumentTypeError("not a number: '%s'" % value)


def main(args):
    from german import say, sayByExp
    number = args.number
    if args.googol or args.googolplex:
        number = 10 ** 100
    if args.zeros or args.googolplex:
        # Do not say given number, but the number with that many zeros.
        zeros, zerosLeft = divmod(number, 3)
        zeros *= 3
        ret = ("10" if zerosLeft == 1 else "100") + " " if zerosLeft else ""
        ret += sayByExp(zeros, zerosLeft)
        numeric = "1" + "0" * number if args.numeric else None
    elif args.random:
        # Do not say given number, but a random number with that many digits.
        import random
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
        print locale.format("%d", int(numeric), grouping=args.grouping)
    print ret.decode('latin-1')


def createParser():
    parser = argparse.ArgumentParser(description='Write german names of (very) big numbers.',
                                     epilog="Please report bugs to daniel.marohn@gmail.com.\nFind more information here: http://de.wikipedia.org/wiki/Zahlennamen",
                                     formatter_class=argparse.RawTextHelpFormatter, add_help=False)

    group = parser.add_argument_group("chose one of these").add_mutually_exclusive_group(required=True)
    group.add_argument('number', nargs="?", type=atLeastZero, help='say this number')
    group.add_argument('-G', '--googol', action="store_true", help='say a googol (10^100)')
    group.add_argument('-GG', '--googolplex', action="store_true", help='say a googolplex (10^googol)')

    group = parser.add_argument_group('help')
    group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                       help="show this help message and exit")
    group.add_argument('-e', '--example', action=ExampleAction, dest='example', default=argparse.SUPPRESS,
                       help='show examples and exit')
    group.add_argument('-v', '--version', action='version', version=VERSION)
    group.add_argument('-c', '--licence', action=LicenceAction, default=argparse.SUPPRESS,
                       help="show licence information and exit")
    group.add_argument('-C', '--fullLicence', action=FullLicenceAction, default=argparse.SUPPRESS,
                       help="show licence file and exit; tries to download and save licence, if not available")

    group = parser.add_argument_group('optional arguments')
    group.add_argument('-n', '--numeric', dest='numeric', action='store_true',
                       help="say the number also in numeric form; it is not recommended to use this option with more than 1.000.000 digits")
    group.add_argument('-f', '--force', dest='force', action='store_true',
                       help="ignore size warnings")

    group = parser.add_argument_group('format')
    group.add_argument('-b', '--byLine', dest='byLine', action='store_true',
                       help='write components line by line')
    group.add_argument('-l', '--latinOnly', dest='latinOnly', action='store_true',
                       help='say "123 millionen" instead of "einhundertdreiundzwanzigmillionen"')
    group.add_argument('-g', '--grouping', dest='grouping', action=GroupingAction,
                       help="group thousand blocks; implicit using -n")

    group = parser.add_argument_group('number').add_mutually_exclusive_group()
    group.add_argument('-z', '--zeros', dest='zeros', action='store_true',
                       help='do not say given number, but the number with that many zeros')
    group.add_argument('-r', '--random', dest='random', action='store_true',
                       help='do not say given number, but a random number with that many digits')

    return parser

if __name__ == "__main__":

    parser = createParser()
    args = parser.parse_args()
    if args.numeric:
        number = args.number
        if (args.zeros or args.random) and number > sys.maxint:
            parser.error(message="When using -n/--numeric, together with -z/--zeros or -r/--random, number must be less or equal %d." % sys.maxint)
        if number > 150000 and not args.force:
                parser.error(message="Building and writing the numeric version of such a big number use a lot of time and memory. " +
                                     "Depending on the size, it my take minutes or longer.\n" +
                                     "Delete option -n/--numeric or activate -f/--force, if you know what you are doing.")
    if args.googolplex and (args.zeros or args.random or args.numeric):
        parser.error(message="Sorry... there cannot be ever a computer available, that would be able to print or build a googoleplex in digits.")
    if args.googol and args.random:
        parser.error(message="I cannot append a googol random digits; no computer will EVER be able to do this.")
    try:
        main(args)
    except ValueError as ex:
        print ex.message
        sys.exit(3)
    except Exception as ex:
        print "error, executing command: " + ex.message
        sys.exit(1)
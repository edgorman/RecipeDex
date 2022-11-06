
import sys
import colorama
import argparse

from recipedex.app import App
from recipedex.log import Log
from recipedex import __name__
from recipedex import __version__
from recipedex import __description__

# Initialise coloured text
colorama.init(convert=True)

# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument('urls', nargs="+", help="the urls to parse")
parser.add_argument('--verbose', action='store_true', dest='verbose', help="show extra output", default=False)
parser.add_argument('--version', action='version', version='%(prog)s@' + __version__)
args = parser.parse_args(sys.argv[1:])

# Handle verboseness
if args.verbose:
    Log.verboseness = 1

# Process arguments and run module
App.main(args)

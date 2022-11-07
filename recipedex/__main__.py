
import sys
import logging
import argparse

from recipedex.app import App
from recipedex import __name__
from recipedex import __version__
from recipedex import __description__


# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("urls", nargs="+", help="the urls to parse")
parser.add_argument("--verbose", action="store_true", dest="verbose", help="show logging in output", default=False)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Handle logging
logger = logging.getLogger('recipedex')
if args.verbose:
    logger.setLevel(logging.DEBUG)

# Process arguments and run app
print(App.main(args))

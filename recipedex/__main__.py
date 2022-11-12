
import sys
import argparse
from logging import _levelToName as log_levels

from recipedex import __description__
from recipedex import __version__
from recipedex import __name__
from recipedex.app import App

LOG_LEVELS = list(log_levels.values())[:-1]


# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("urls", nargs="+", help="the urls to parse")
parser.add_argument("--metric", dest="metric", action="store_true", help="force units to be metric")
parser.add_argument("--imperial", dest="imperial", action="store_true", help="force units to be imperial")
parser.add_argument("--log", dest="log", help="the log level", default="WARNING", choices=LOG_LEVELS)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Check metric and imperial flags
if args.metric and args.imperial:
    parser.error("cannot set --metric and --imperial flags at the same time.")

# Process arguments and run app
print(App.main(args))

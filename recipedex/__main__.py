
import sys
import logging
import argparse
from logging import _levelToName as log_levels
LOG_LEVELS = list(log_levels.values())[:-1]

from recipedex.app import App
from recipedex import __name__
from recipedex import __version__
from recipedex import __description__


# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("urls", nargs="+", help="the urls to parse")
parser.add_argument("--log", dest="log", help="the log level", default="WARNING", choices=LOG_LEVELS)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Handle logging
logger = logging.getLogger('recipedex')
logger.setLevel(args.log)

# Process arguments and run app
print(App.main(args))

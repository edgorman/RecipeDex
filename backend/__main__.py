
import sys
import uvicorn
import logging
import argparse
from logging import _levelToName as log_levels

from backend import __description__
from backend import __version__
from backend import __name__

LOG_LEVELS = list(log_levels.values())[:-1]


# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("--port", dest="port", help="the port to serve fastapi on", default="5000", type=int)
parser.add_argument("--reload", action="store_true", dest="reload", help="reload on change (for dev)", default=False)
parser.add_argument("--log", dest="log", help="the log level", default="WARNING", choices=LOG_LEVELS)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Handle logging
logger = logging.getLogger('backend')
logger.setLevel(args.log)

# Process arguments and run app
uvicorn.run("backend.app:app", port=int(args.port), log_level=args.log.lower(), reload=args.reload)

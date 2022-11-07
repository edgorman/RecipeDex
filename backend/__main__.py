
import sys
import uvicorn
import argparse
from uvicorn.config import LOG_LEVELS

from backend import __name__
from backend import __version__
from backend import __description__



# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("--port", dest="port", help="the port to serve fastapi on", default="5000", type=int)
parser.add_argument("--log", dest="log", help="the log level for uvicorn", default="info", choices=LOG_LEVELS.keys())
parser.add_argument("--reload", action="store_true", dest="reload", help="reload on change (for dev)", default=False)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Process arguments and run app
uvicorn.run("backend.app:app", port=int(args.port), log_level=args.log, reload=args.reload)

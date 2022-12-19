import os
import sys
import uvicorn
import logging
import argparse
from dotenv import load_dotenv
from logging import _levelToName as log_levels

from backend import __name__
from backend import __version__
from backend import __description__


LOG_LEVELS = list(log_levels.values())[:-1]


# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("--port", dest="port", help="the port to serve fastapi on", default=5000, type=int)
parser.add_argument("--prod", action="store_true", dest="prod", help="use production environment", default=False)
parser.add_argument("--log", dest="log", help="the log level", default="WARNING", choices=LOG_LEVELS)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Handle logging
logger = logging.getLogger('backend')
logger.setLevel(args.log)

# Handle dev vs prod
if args.prod:
    load_dotenv('backend/.env')
    usn, pwd = os.getenv('db_username'), os.getenv('db_password')
    assert usn is not None and pwd is not None, "Could not load db credentials from 'backend/.env'"

    os.environ['database_url'] = f"mongodb+srv://{usn}:{pwd}@recipedex.0gtcjbb.mongodb.net/?retryWrites=true&w=majority"
    logger.info("Running as production")
else:
    os.environ['database_url'] = "mongodb://127.0.0.1:27017"
    logger.info("Running as developer")

# Process arguments and run app
uvicorn.run("backend.api:api", port=int(args.port), log_level=args.log.lower(), reload=not args.prod, use_colors=False)

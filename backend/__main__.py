
import sys
import uvicorn
import logging
import asyncio
import argparse
from logging import _levelToName as log_levels

from backend import __name__
from backend import __version__
from backend import __description__
from backend.database.database import clear_recipes


LOG_LEVELS = list(log_levels.values())[:-1]
logger = logging.getLogger('backend')


# Parse input arguments
parser = argparse.ArgumentParser(prog=__name__, description=__description__)
parser.add_argument("--port", dest="port", help="the port to serve fastapi on", default=5000, type=int)
parser.add_argument("--reload", action="store_true", dest="reload", help="reload on change (for dev)", default=False)
parser.add_argument("--resetdb", action="store_true", dest="resetdb", help="reset database (for dev)", default=False)
parser.add_argument("--log", dest="log", help="the log level", default="WARNING", choices=LOG_LEVELS)
parser.add_argument("--version", action="version", version="%(prog)s@" + __version__)
args = parser.parse_args(sys.argv[1:])

# Handle logging
logger.setLevel(args.log)

# If flag set, clear database
if args.resetdb:
    async def function(param) -> asyncio.coroutine:
        await param()
    asyncio.run(function(clear_recipes))
    logger.info("Clearing all recipes from database for local dev.")

# Process arguments and run app
uvicorn.run("backend.api:api", port=int(args.port), log_level=args.log.lower(), reload=args.reload, use_colors=False)

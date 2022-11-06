
import sys
import colorama
import argparse

from recipedex.app import App
from recipedex.log import Log
from recipedex.constants import VERSION

if __name__ == '__main__':
    '''
        This script processes input from user and runs the main application.
    '''
    # Initialise coloured text
    colorama.init(convert=True)

    # Parse input arguments
    parser = argparse.ArgumentParser(prog="RecipeDex", description="Automatically parse and extract info from recipes.")
    parser.add_argument('urls', nargs="+", help="the urls to parse")
    parser.add_argument('--verbose', action='store_true', dest='verbose', help="show extra output", default=False)
    parser.add_argument('--version', action='version', version='%(prog)s@' + VERSION)
    args = parser.parse_args(sys.argv[1:])

    # Handle verboseness
    if args.verbose:
        Log.verboseness = 1

    # Process arguments and run module
    App.main(args)

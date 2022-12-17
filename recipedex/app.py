import json
import logging
import argparse

from recipedex.recipe import Recipe


logger = logging.getLogger("recipedex.app")


class App:

    @staticmethod
    def main(args: argparse.Namespace) -> dict:
        '''
            Process the arguments passed from the command line

            Parameters:
                args: Dict of arguments input from the user
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        logger.setLevel(args.log)

        response = []
        for url in args.urls:
            try:
                response.append(Recipe(url, args.serves, args.metric, args.imperial))
                logger.info(f"Successfully parsed url '{url}'")
            except Exception as e:
                logger.warning(f"Could not parse url '{url}': '{str(e)}'")

        logger.info("Outputting response as a JSON encoded string.")
        return json.dumps(response)

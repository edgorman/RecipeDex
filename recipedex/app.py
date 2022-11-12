
import json
import logging
import argparse
import regex as re

from recipedex.ingredient import parse_ingredient
from recipedex.ingredient import convert_to_system
from recipe_scrapers import scrape_me as parse_recipe


logger = logging.getLogger("recipedex.app")


class App:

    @staticmethod
    def parse_urls(urls: list) -> dict:
        '''
            Parse a list of urls and return a dict object of each

            Parameters:
                urls: List of urls input from the user
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        recipes_dict = {}

        for url in urls:
            try:
                recipe = parse_recipe(url)

                recipes_dict[url] = {
                    'host': recipe.host(),
                    'name': recipe.title(),
                    'time': recipe.total_time(),
                    'servings': int(re.search(r"(\d+)", recipe.yields()).group(1)),
                    'ingredients': recipe.ingredients(),
                    'instructions': recipe.instructions_list(),
                    'image_url': recipe.image(),
                    'nutrients': recipe.nutrients(),
                }

                logger.info(f"Extracted recipe for '{recipes_dict[url]['name']}'")
            except Exception as e:
                logger.warning(f"Failed extracting recipe for '{url}': {str(e)}")
                continue

        return recipes_dict

    @staticmethod
    def extract_ingredients(recipes_dict: dict, use_metric: bool = False, use_imperial: bool = False) -> dict:
        '''
            Extract the name, quantity, unit and comment from an ingredient string

            Parameters:
                recipes_dict: Dict of recipe objects where the url is the key
                use_metric: Whether to automatically use metric system
                use_imperial: Whether to automatically use imperial system
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        unit_system = None
        if use_metric: unit_system = "mks"
        if use_imperial: unit_system = "imperial"

        for url, recipe in recipes_dict.items():
            try:
                ingredients_list = []
                for ingredient in recipe["ingredients"]:
                    parsed_ingredient = {}

                    try:
                        parsed_ingredient = parse_ingredient(ingredient)
                    except Exception as e:
                        logger.warning(f"Could not parse line {ingredient}: {str(e)}")

                    ingredients_list.append(parsed_ingredient)
                
                if unit_system is not None:
                    ingredients_list = convert_to_system(ingredients_list, unit_system)

                recipes_dict[url]["ingredients_list"] = ingredients_list
                logger.info(f"Extracted ingredients for '{recipe['name']}'")
            except Exception as e:
                logger.warning(f"Failed extracting ingredients for '{recipe['name']}': {str(e)}")
                continue

        return recipes_dict

    @staticmethod
    def generate_metadata(recipes_dict: dict) -> dict:
        '''
            Generate any additional metadata for the list of recipes.

            Parameters:
                recipes_dict: Dict of recipe objects where the url is the key
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        for _, recipe in recipes_dict.items():
            try:
                # TODO: Generate metadata here, may include
                # * season (?)
                # * tags (title of recipe with keywords removed)
                # * linked recipes (try run parse_recipe on each url in page?)
                # * popularity (ratings/comment counts on the page)
                # * price (need a way to lookup price of individual ingredients)
                # * author (regex search for By: <>)
                # * date last updated (maybe use metadata)

                logger.info(f"Generated metadata for '{recipe['name']}'")
            except Exception as e:
                logger.warning(f"Failed generating metadata for '{recipe['name']}': {str(e)}")
                continue

        return recipes_dict

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

        logger.info(f"Parsing {len(args.urls)} urls with the recipe scraper package.")
        recipes_dict = App.parse_urls(args.urls)

        logger.info("Extracting ingredients to a list of names, preperation, metric and amount.")
        recipes_dict = App.extract_ingredients(recipes_dict, use_metric=args.metric, use_imperial=args.imperial)

        logger.info("Generating additional metdata about each recipe.")
        recipes_dict = App.generate_metadata(recipes_dict)

        logger.info("Outputting response as a JSON encoded string.")
        return json.dumps(recipes_dict)

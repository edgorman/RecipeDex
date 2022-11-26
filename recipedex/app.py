import json
import nltk
import logging
import argparse
import regex as re

from recipedex.ingredient import parse_ingredient
from recipedex.ingredient import convert_to_system
from recipedex.ingredient import scale_to_amount
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
                    'unit': "default",
                    'tags': [],
                }

                logger.info(f"Extracted recipe for '{recipes_dict[url]['name']}'")
            except Exception as e:
                logger.warning(f"Failed extracting recipe for '{url}': {str(e)}")
                continue

        return recipes_dict

    @staticmethod
    def extract_ingredients(recipes_dict: dict, serves: int = 0, metric: bool = False, imperial: bool = False) -> dict:
        '''
            Extract the name, quantity, unit and comment from an ingredient string

            Parameters:
                recipes_dict: Dict of recipe objects where the url is the key
                serves: How much to scale ingredients to (0=don't scale)
                metric: Whether to automatically use metric system
                imperial: Whether to automatically use imperial system
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        # For each recipe being parsed
        for url, recipe in recipes_dict.items():
            try:
                ingredients_list = []

                # For each ingredient in recipe
                for ingredient in recipe["ingredients"]:
                    parsed_ingredient = {}

                    try:
                        # Parse ingredient
                        parsed_ingredient = parse_ingredient(ingredient)
                    except Exception as e:
                        logger.warning(f"Could not parse line {ingredient}: {str(e)}")

                    ingredients_list.append(parsed_ingredient)

                # Convert to new unit system if set
                if metric:
                    recipe["unit"] = "metric"
                    ingredients_list = convert_to_system(ingredients_list, "mks")
                elif imperial:
                    recipe["unit"] = "imperial"
                    ingredients_list = convert_to_system(ingredients_list, "imperial")
                else:
                    recipe["unit"] = "default"

                # Convert to new scale if set
                if serves > 0:
                    ingredients_list = scale_to_amount(ingredients_list, serves / recipe["servings"])
                    recipe["servings"] = serves

                # Update recipe with new recipes list
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
                # Generate tags used in search
                tags = [n.lower() for n in recipe["name"].split()]
                tags.extend([j.lower() for j in sum([i['name'].split() for i in recipe["ingredients_list"]], [])])
                tags.append(recipe["host"].lower())
                tags = [t for t in tags if t not in nltk.corpus.stopwords.words("english") and not t.isnumeric()]
                recipe["tags"] = tags

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
        recipes_dict = App.extract_ingredients(
            recipes_dict,
            serves=args.serves,
            metric=args.metric,
            imperial=args.imperial
        )

        logger.info("Generating additional metdata about each recipe.")
        recipes_dict = App.generate_metadata(recipes_dict)

        logger.info("Outputting response as a JSON encoded string.")
        return json.dumps(recipes_dict)

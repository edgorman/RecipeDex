
import os
import sys
import json
import logging
import argparse

from recipedex.ingredient import parse_ingredient
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
                    'servings': recipe.yields(),
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
    def extract_ingredients(recipes_dict: dict) -> dict:
        '''
            Extract the name, quantity, unit and comment from an ingredient string

            Parameters:
                recipes_dict: Dict of recipe objects where the url is the key
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        def replace_vulgar(v):
            return v.replace(u"¼", "1/4").replace(u"½", "1/2").replace(u"¾", "3/4").replace(u"⅕", "1/5")

        for url, recipe in recipes_dict.items():
            try:
                ingredients_list = []
                for ingredient in recipe["ingredients"]:
                    parsed_ingredient = {}

                    try:
                        parsed_ingredient = parse_ingredient(replace_vulgar(ingredient))
                    except Exception as e:
                        logger.warning(f"Could not parse line {ingredient}: {str(e)}")

                    ingredients_list.append(parsed_ingredient)

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
        recipes_dict = App.extract_ingredients(recipes_dict)

        logger.info("Generating additional metdata about each recipe.")
        recipes_dict = App.generate_metadata(recipes_dict)

        logger.info("Outputting response as a JSON encoded string.")
        return json.dumps(recipes_dict)

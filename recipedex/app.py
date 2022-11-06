
import os
import sys
import json
import argparse
from parse_ingredients import parse_ingredient
from recipe_scrapers import scrape_me as scrape_recipe

from recipedex.log import Log


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
                recipe = scrape_recipe(url)

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

                Log.success(f"Extracted recipe for '{recipes_dict[url]['name']}'")
            except Exception as e:
                Log.error(f"Failed extracting recipe for '{url}': {str(e)}")
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
                sys.stdout = open(os.devnull, 'w')
                ingredients_list = [parse_ingredient(replace_vulgar(i)) for i in recipe["ingredients"]]
                sys.stdout = sys.__stdout__

                recipes_dict[url]["ingredients_list"] = [
                    {
                        "name": i.name,
                        "quantity": i.quantity,
                        "unit": i.unit,
                        "comment": i.comment
                    }
                    for i in ingredients_list
                ]

                Log.success(f"Extracted ingredients for '{recipe['name']}'")
            except Exception as e:
                sys.stdout = sys.__stdout__
                Log.error(f"Failed extracting ingredients for '{recipe['name']}': {str(e)}")
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
        Log.info(f"Starting generating metatadata for {len(recipes_dict)} recipes.")

        for _, recipe in recipes_dict.items():
            try:
                # TODO: Generate metadata here

                Log.success(f"Generated metadata for '{recipe['name']}'")
            except Exception as e:
                Log.error(f"Failed generated metadata for '{recipe['name']}': {str(e)}")
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
        Log.info(f"Parsing {len(args.urls)} urls with the recipe scraper package.")
        recipes_dict = App.parse_urls(args.urls)
        Log.success("Finished parsing urls from the command line.")

        Log.info("Extracting ingredients to a list of names, preperation, metric and amount.")
        recipes_dict = App.extract_ingredients(recipes_dict)
        Log.success("Finished extracting ingredients.")

        Log.info("Generating additional metdata about each recipe.")
        recipes_dict = App.generate_metadata(recipes_dict)
        Log.success("Finished generating metadata for recipes.")

        Log.print(json.dumps(recipes_dict))

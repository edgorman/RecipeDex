
import argparse
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
        Log.info(f"Starting parsing of {len(urls)} urls from the command line.")

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
    def convert_ingredients(recipes_dict: dict) -> dict:
        '''
            Convert ingredients to name and amount, and to metric if necessary

            Parameters:
                recipes_dict: Dict of recipe objects where the url is the key
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''
        Log.info(f"Starting simplifying of ingredients for {len(recipes_dict)} recipes.")

        for _, recipe in recipes_dict.items():
            try:
                # TODO: Simplify ingredients here

                Log.success(f"Simplified ingredients for '{recipe['name']}'")
            except Exception as e:
                Log.error(f"Failed simplifying ingredients for '{recipe['name']}': {str(e)}")
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
        Log.success(f"Finished parsing urls from the command line.")

        Log.info(f"Simplify ingredients list and convert to metric system.")
        recipes_dict = App.convert_ingredients(recipes_dict)
        Log.success(f"Finished simplifying ingredients.")

        Log.info(f"Generating additional metdata about each recipe.")
        recipes_dict = App.generate_metadata(recipes_dict)
        Log.success(f"Finished generating metadata for recipes.")
        
        return recipes_dict

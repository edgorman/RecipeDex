
import json
import nltk
import string
import argparse
from recipe_scrapers import scrape_me as scrape_recipe
from recipedex.log import Log


class App:
    # Install required nltk packages
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

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
    def extract_tokens(tokens: list, idx_range: list) -> str:
        '''
            Extract the tokens at index ranges given

            Parameters:
                tokens: List of tokens from the ingredient string
                idx_range: List of index ranges to include in output
            Returns:
                joined_tokens: String of the extracted tokens joined together
        '''
        tokens_list = [tokens[first:last] for first, last in idx_range]
        tokens_joined = " ".join(" ".join(token for token in tokens) for tokens in tokens_list)
        return tokens_joined.replace("( ", "(").replace(" )", ")")
    
    @staticmethod
    def extract_ingredients(recipes_dict: dict) -> dict:
        '''
            Extract the name, preperation, metric and amount from an ingredient string

            Parameters:
                recipes_dict: Dict of recipe objects where the url is the key
            Returns:
                recipes_dict: Dict of recipe objects where the url is the key
        '''

        for url, recipe in recipes_dict.items():
            try:
                raw_ingredients = recipe["ingredients"]
                pos_ingredients = [(r, nltk.pos_tag(nltk.word_tokenize(r))) for r in raw_ingredients]
                out_ingredients = []

                # For each ingredient sentence
                for raw, tokens in pos_ingredients:
                    preperation_idx, metric_idx, amount_idx = [], [], []
                    
                    # For each token in sentence
                    for i in range(len(tokens)):
                        
                        # Parse amount and metric
                        if len(amount_idx) == 0 and tokens[i][1].startswith("CD") and i + 1 <= len(tokens):
                            # Handle parentheses following number
                            if tokens[i + 1][0].startswith("("):
                                amount_idx.append((0, i + 1))
                                metric_idx.append((i + 1, [t[0] for t in tokens].index(")") + 2))
                            # Else handle normal case
                            elif i + 1 < len(tokens) and tokens[i + 1][1].startswith("NN"):
                                amount_idx.append((0, i + 1))
                                metric_idx.append((i + 1, i + 2))
                        
                        # Parse preperation
                        if tokens[i][1].startswith(",") and i + 1 <= len(tokens) and tokens[i + 1][1].startswith("VB"):
                            preperation_idx.append((i + 1, len(tokens)))
                            break
                    
                    # Generate string representations from indexes
                    preperation_str = App.extract_tokens([t[0] for t in tokens], preperation_idx)
                    metric_str = App.extract_tokens([t[0] for t in tokens], metric_idx)
                    amount_str = App.extract_tokens([t[0] for t in tokens], amount_idx)

                    # Generate ingredient name from removing the rest
                    ingredient_str = raw.replace(metric_str, "").replace(preperation_str, "").replace(amount_str, "")
                    ingredient_str = ingredient_str.strip().translate(str.maketrans('', '', string.punctuation))
                    if len(ingredient_str) == 0:
                        ingredient_str = metric_str
                    
                    # Store parsed ingredients as a tuple
                    out_ingredients.append((ingredient_str, preperation_str, metric_str, amount_str))

                # Ingredients have been successfully converted, updating recipe
                recipes_dict[url]["ingredients_list"] = out_ingredients
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

        Log.info(f"Extracting ingredients to a list of names, preperation, metric and amount.")
        recipes_dict = App.extract_ingredients(recipes_dict)
        Log.success(f"Finished extracting ingredients.")

        Log.info(f"Generating additional metdata about each recipe.")
        recipes_dict = App.generate_metadata(recipes_dict)
        Log.success(f"Finished generating metadata for recipes.")
        
        Log.print(json.dumps(recipes_dict))

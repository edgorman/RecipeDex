import nltk
import logging
import regex as re
from recipe_scrapers import scrape_me as parse_recipe

from recipedex.ingredient import Ingredient


logger = logging.getLogger("recipedex.recipe")


class Recipe:
    nltk.download("stopwords", quiet=True)

    def __init__(self, url: str = None, host: str = None, name: str = None, time: int = 0, unit: str = "default",
                 servings: int = 0, ingredient_strs: list = [], instructions_strs: list = [], image: str = None,
                 nutrients: dict = {}, tags: list = []):
        '''
            Initialise a Recipe object by parsing the URL or by the values passed

            Parameters:
                url: Link to the recipe webpage
                host: Name of the website
                name: Name of the recipe
                time: Time taken to perform recipe
                unit: The measurement system used in recipe
                servings: Number of people this recipe serves
                ingredient_strs: List of ingredients strings from webpage
                instructions_strs: List of instructions string from webpage
                image: Link to an image of the recipe (optional)
                nutrients: Dictionary of nutrient information (optional)
                tags: Keywords used to search for this recipe
            
            Returns:
                None
        '''
        
        # If a url is given, parse the recipe directly
        if url is not None:
            self.url = url

            try:
                # Parse recipe using recipe_scrapers module
                data = parse_recipe(self.url)

                self.host = data.host()
                self.name = data.title()
                self.time = data.total_time()
                self.unit = "default"
                self.servings = int(re.search(r"(\d+)", recipe.yields()).group(1))
                self.ingredients_strs = data.ingredients()
                self.instructions_strs = data.instructions_list()
                self.image = data.image()
                self.nutrients = data.nutrients()
            except Exception as e:
                logger.warning(f"Failed extracting recipe '{self.url}': {str(e)}")

        # Else use the init variables passsed
        else:
            self.url = url
            self.host = host
            self.name = name
            self.time = time
            self.unit = "default"
            self.servings = servings
            self.ingredients_strs = ingredients_strs
            self.instructions_strs = instructions_strs
            self.image = image
            self.nutrients = nutrients
    
        # Extract ingredients to store as objects
        self.ingredient_list = self.extract_ingredients()
        
        # Extract keywords to store in tags list
        self.tags = self.extract_tags()
    
    def extract_ingredients(self, serves, metric, imperial):
        '''
            Extract the ingredients from the ingredient strings

            Parameters:
                None
            Returns:
                ingredients: List of ingredient objects
        '''

        # Parse the ingredients into objects using Pint
        ingredients = [Ingredient(i) for i in self.ingredient_strs]

        # Convert ingredients to unit system if set
        if metric:
            ingredients = [i.convert_to_system("mks") for i in ingredients]
            self.unit = "metric"
        elif imperial:
            ingredients = [i.convert_to_system("imperial") for i in ingredients]
            self.unit = "imperial"

        # Convert ingredients to servings if set
        if serves > 0:
            ingredients = [i.scale_to_amount(serves / self.servings) for i in ingredients]
            self.servings = serves
        
        return ingredients

    def extract_tags(self):
        '''
            Extract the tags from the properties of this recipe

            Parameters:
                None
            
            Returns:
                tags: List of keywords from properties
        '''

        # Extract each word in the name field
        tags = [n.lower() for n in self.name.split()]

        # Extract tags from each ingredient object
        tags.extend(sum([i.extract_tags() for i in self.ingredient_list], []))

        # Extract the host name
        tags.append(self.host.lower())

        # Remove stop words that appear in the tags list
        def is_readable(tag):
            return not tag.isnumeric() and tag not in nltk.corpus.stopwords.words("english")
        tags = list(filter(is_readable, tags))

        return tags

import json
import nltk
import logging
import regex as re
from recipe_scrapers import scrape_me as parse_recipe

from recipedex.ingredient import Ingredient

nltk.download("stopwords", quiet=True)


logger = logging.getLogger("recipedex.recipe")


class Recipe(dict):

    def __init__(self, url: str = None, host: str = None, name: str = None, time: int = 0, unit: str = "default",
                 servings: int = 0, ingredient_strs: list = [], instruction_strs: list = [], image: str = None,
                 nutrients: dict = {}):
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
                instruction_strs: List of instructions string from webpage
                image: Link to an image of the recipe (optional)
                nutrients: Dictionary of nutrient information (optional)
            
            Returns:
                None
        '''
        super(Recipe, self).__init__(
            url=url, host=host, name=name, time=time, unit=unit, servings=servings, ingredient_strs=ingredient_strs,
            instruction_strs=instruction_strs, image=image, nutrients=nutrients, ingredients_list=[], tags=[]
        )
        
        # If a url is given, parse the recipe directly
        if url is not None:
            self["url"] = url

            try:
                # Parse recipe using recipe_scrapers module
                data = parse_recipe(self["url"])

                self["host"] = data.host()
                self["name"] = data.title()
                self["time"] = data.total_time()
                self["unit"] = unit
                self["servings"] = int(re.search(r"(\d+)", data.yields()).group(1))
                self["ingredient_strs"] = data.ingredients()
                self["instruction_strs"] = data.instructions_list()
                self["image"] = data.image()
                self["nutrients"] = data.nutrients()
            except Exception as e:
                raise Exception(f"Failed extracting recipe '{self['url']}': {str(e)}")
    
        # Extract ingredients to store as objects
        self["ingredient_list"] = self.extract_ingredients(self["servings"], False, False)
        
        # Extract keywords to store in tags list
        self["tags"] = self.extract_tags()
    
    def extract_ingredients(self, serves, metric, imperial):
        '''
            Extract the ingredients from the ingredient strings

            Parameters:
                None
            Returns:
                ingredients: List of ingredient objects
        '''

        # Parse the ingredients into objects using Pint
        ingredients = [Ingredient(i) for i in self["ingredient_strs"]]

        # Convert ingredients to unit system if set
        if metric:
            ingredients = [i.to_system("mks") for i in ingredients]
            self["unit"] = "metric"
        elif imperial:
            ingredients = [i.to_system("imperial") for i in ingredients]
            self["unit"] = "imperial"

        # Convert ingredients to servings if set
        if serves != self["servings"] and serves > 0:
            ingredients = [i.to_scale(serves / self["servings"]) for i in ingredients]
            self["servings"] = serves
        
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
        tags = [n.lower() for n in self["name"].split()]

        # Extract tags from each ingredient object
        tags.extend(sum([i.extract_tags() for i in self["ingredient_list"]], []))

        # Extract the host name
        tags.append(self["host"].lower())

        # Remove stop words that appear in the tags list
        def is_readable(tag):
            return not tag.isnumeric() and tag not in nltk.corpus.stopwords.words("english")
        tags = list(filter(is_readable, tags))

        return tags

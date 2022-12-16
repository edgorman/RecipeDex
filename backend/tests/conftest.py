import pytest
from httpx import AsyncClient

from backend.api import api


@pytest.fixture(autouse=True, scope="function")
def client():
    return AsyncClient(app=api, base_url="http://test")


@pytest.fixture(autouse=True, scope="function")
def mock_index():
    return [
        {"url": "test", "name": "this"},
        {"url": "lorem", "name": "ipsum"},
    ]


@pytest.fixture(autouse=True, scope="function")
def mock_recipe():
    return {
        "url": "https://www.bbcgoodfood.com/recipes/pizza-margherita-4-easy-steps",
        "host": "bbcgoodfood.com",
        "name": "Pizza Margherita in 4 easy steps",
        "time": 35,
        "unit": "default",
        "servings": 2,
        "ingredient_strs": [
            "300g strong bread flour", "1 tsp instant yeast (from a sachet or a tub)", "1 tsp salt",
            "1 tbsp olive oil, plus extra for drizzling", "100ml passata", "handful fresh basil or 1 tsp dried",
            "1 garlic clove, crushed", "125g ball mozzarella, sliced",
            "handful grated or shaved parmesan (or vegetarian alternative)", "handful of cherry tomatoes, halved",
            "handful of basil leaves (optional)"
        ],
        "instruction_strs": [
            "Make the base: Put the flour into a large bowl, then stir in the yeast and salt. Make a well, pour"
            " in 200ml warm water and the olive oil and bring together with a wooden spoon until you have a"
            " soft, fairly wet dough. Turn onto a lightly floured surface and knead for 5 mins until smooth."
            " Cover with a tea towel and set aside. You can leave the dough to rise if you like, but it’s not"
            " essential for a thin crust.",
            "Make the sauce: Mix the passata, basil and crushed garlic together, then season to taste. Leave to"
            " stand at room temperature while you get on with shaping the base.",
            "Roll out the dough: if you’ve let the dough rise, give it a quick knead, then split into two"
            " balls. On a floured surface, roll out the dough into large rounds, about 25cm across, using a"
            " rolling pin. The dough needs to be very thin as it will rise in the oven. Lift the rounds onto"
            " two floured baking sheets.",
            "Top and bake: heat the oven to 240C/220C fan/gas 8. Put another baking sheet or an upturned"
            " baking tray in the oven on the top shelf. Smooth sauce over bases with the back of a spoon."
            " Scatter with cheese and tomatoes, drizzle with olive oil and season. Put one pizza, still on its"
            " baking sheet, on top of the preheated sheet or tray. Bake for 8-10 mins until crisp. Serve with a"
            " little more olive oil, and basil leaves if using. Repeat step for remaining pizza."
        ],
        "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/recipe-image-legacy-id-"
                 "51643_11-2f4a2cc.jpg?resize=768,574",
        "nutrients": {
            "calories": "431 calories",
            "fatContent": "15 grams fat",
            "saturatedFatContent": "7 grams saturated fat",
            "carbohydrateContent": "59 grams carbohydrates",
            "sugarContent": "2 grams sugar",
            "fiberContent": "3 grams fiber",
            "proteinContent": "19 grams protein",
            "sodiumContent": "1.9 milligram of sodium"
        },
        "tags": [
            "pizza", "margherita", "easy", "steps", "strong", "bread", "flour", "instant", "yeast", "salt", "olive",
            "oil", "passata", "fresh", "basil", "clove", "ball", "mozzarella", "grated", "cherry", "tomatoes", "basil",
            "leaves", "bbcgoodfood.com"
        ],
        "ingredient_list": [
            {"name": "Strong bread flour", "unit": "g", "quantity": "300", "comment": "", "optional": False}, 
            {"name": "Instant yeast", "unit": "tsp", "quantity": "1", "comment": "from a sachet or a tub", "optional":
             False},
            {"name": "Salt", "unit": "tsp", "quantity": "1", "comment": "", "optional": False},
            {"name": "Olive oil", "unit": "tbsp", "quantity": "1", "comment": "plus extra for drizzling", "optional":
             False},
            {"name": "Passata", "unit": "ml", "quantity": "100", "comment": "", "optional": False},
            {"name": "Fresh basil", "unit": "handful", "quantity": "1", "comment": "or 1 tsp dried", "optional": False},
            {"name": "Clove", "unit": "garlic", "quantity": "1", "comment": "crushed", "optional": False},
            {"name": "Ball mozzarella", "unit": "g", "quantity": "125", "comment": "sliced", "optional": False},
            {"name": "Grated", "unit": "handful", "quantity": "1", "comment": 
             "or shaved parmesan or vegetarian alternative", "optional": False},
            {"name": "Cherry tomatoes", "unit": "handful", "quantity": "1", "comment": "halved", "optional": False},
            {"name": "Basil leaves", "unit": "handful", "quantity": "1", "comment": "", "optional": True}
        ]
    }


@pytest.fixture(autouse=True, scope="function")
def mock_tags():
    return [
        {
            "tag": "chicken",
            "recipe_ids": [
                "63753dcc352382d88723cb90",
                "63753dcc352382d88723cb91",
            ]
        },
        {
            "tag": "beef",
            "recipe_ids": [
                "63753dcc352382d88723cb90",
                "63753dcc352382d88723cb91",
            ]
        },
    ]

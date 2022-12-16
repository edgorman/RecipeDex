import pytest

from recipedex.recipe import Recipe
from recipedex.ingredient import Ingredient


@pytest.mark.parametrize("url,expected", [
    (
        "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/",
        {
            "host": "allrecipes.com",
            "name": "Spinach and Feta Turkey Burgers",
            "time": 35,
            "unit": "default",
            "servings": 8,
            "ingredient_strs": [
                "cooking spray", "2 pounds ground turkey",
                "1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry", "4 ounces feta cheese",
                "2 large eggs, beaten", "2 cloves garlic, minced"
            ],
            "instruction_strs": [
                "Preheat an outdoor grill for medium-high heat and lightly oil the grate.",
                "Mix together turkey, spinach, feta, eggs, and garlic in a large bowl until well combined; form "
                "into 8 patties.", "Cook patties on the preheated grill on both sides until no longer pink in "
                "the center, 15 to 20 minutes. An instant-read thermometer inserted into the center of patties should "
                "read at least 165 degrees F (74 degrees C)."
            ],
            "image": "https://www.allrecipes.com/thmb/cpf6Rics5oHGq1TZ1df5fEaImwM=/1500x0/filters:no_upscale():"
            "max_bytes(150000):strip_icc()/1360550-582be362ee99424bb4f363c2274a9d0d.jpg",
            "nutrients": {
                "calories": "233 kcal",
                "carbohydrateContent": "2 g",
                "cholesterolContent": "143 mg",
                "fiberContent": "1 g",
                "proteinContent": "27 g",
                "saturatedFatContent": "5 g",
                "sodiumContent": "266 mg",
                "sugarContent": "1 g",
                "fatContent": "13 g",
                "unsaturatedFatContent": "0 g"
            },
            "ingredient_list": [
                Ingredient("cooking spray"),
                Ingredient("2 pounds ground turkey"),
                Ingredient("1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry"),
                Ingredient("4 ounces feta cheese"),
                Ingredient("2 large eggs, beaten"),
                Ingredient("2 cloves garlic, minced")
            ],
            "tags": [
                "spinach", "feta", "turkey", "burgers", "cooking", "spray", "ground", "turkey", "box", "frozen",
                "chopped", "spinach", "feta", "cheese", "eggs", "garlic", "allrecipes.com"
            ],
        }
    ),
    (
        "https://www.bbcgoodfood.com/recipes/chicken-pasta-bake",
        {
            "host": "bbcgoodfood.com",
            "name": "Chicken pasta bake",
            "time": 75,
            "unit": "default",
            "servings": 6,
            "ingredient_strs": [
                "4 tbsp olive oil", "1 onion , finely chopped", "2 garlic cloves , crushed", "¼ tsp chilli flakes",
                "2 x 400g cans chopped tomatoes", "1 tsp caster sugar", "6 tbsp mascarpone",
                "4 skinless chicken breasts, sliced into strips", "300g penne", "70g mature cheddar , grated",
                "50g grated mozzarella", "½ small bunch of parsley , finely chopped"
            ],
            "instruction_strs": [
                "Heat 2 tbsp of the oil in a pan over a medium heat and fry the onion gently for 10-12 mins. Add "
                "the garlic and chilli flakes and cook for 1 min. Tip in the tomatoes and sugar and season to "
                "taste. Simmer uncovered for 20 mins or until thickened, then stir through the mascarpone.",
                "Heat 1 tbsp of oil in a non-stick frying pan. Season the chicken and fry for 5-7 mins or until "
                "the chicken is cooked through.",
                "Heat the oven to 220C/200C fan/gas 7. Cook the penne following pack instructions. Drain and toss "
                "with the remaining oil. Tip the pasta into a medium sized ovenproof dish. Stir in the chicken and "
                "pour over the sauce. Top with the cheddar, mozzarella and parsley. Bake for 20 mins or until "
                "golden brown and bubbling."
            ],
            "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chicken_pasta_bake"
            "-06fe2d6.jpg?resize=768,574",
            "nutrients": {
                "calories": "575 calories", "fatContent": "30 grams fat",
                "saturatedFatContent": "14 grams saturated fat", "carbohydrateContent": "41 grams carbohydrates",
                "sugarContent": "9 grams sugar", "fiberContent": "5 grams fiber",
                "proteinContent": "33 grams protein", "sodiumContent": "0.5 milligram of sodium"
            },
            "ingredient_list": [
                Ingredient("4 tbsp olive oil"),
                Ingredient("1 onion , finely chopped"),
                Ingredient("2 garlic cloves , crushed"),
                Ingredient("¼ tsp chilli flakes"),
                Ingredient("2 x 400g cans chopped tomatoes"),
                Ingredient("1 tsp caster sugar"),
                Ingredient("6 tbsp mascarpone"),
                Ingredient("4 skinless chicken breasts, sliced into strips"),
                Ingredient("300g penne"),
                Ingredient("70g mature cheddar , grated"),
                Ingredient("50g grated mozzarella"),
                Ingredient("½ small bunch of parsley , finely chopped")
            ],
            "tags": [
                "chicken", "pasta", "bake", "olive", "oil", "onion", "cloves", "tsp", "chilli", "flakes", "cans",
                "chopped", "tomatoes", "caster", "sugar", "mascarpone", "chicken", "breasts", "penne", "mature",
                "cheddar", "grated", "mozzarella", "parsley", "bbcgoodfood.com"
            ],
        }
    ),
])
def test_initialize(url, expected):
    result = Recipe(url)

    for key, value in expected.items():
        assert result[key] == value, f"'{key}' contains '{result[key]}' value, expected '{value}'"

@pytest.mark.parametrize("kwargs,expected", [
    (
        {
            "host": "allrecipes.com",
            "name": "Spinach and Feta Turkey Burgers",
            "time": 35,
            "unit": "default",
            "servings": 8,
            "ingredient_strs": [
                "cooking spray", "2 pounds ground turkey",
                "1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry", "4 ounces feta cheese",
                "2 large eggs, beaten", "2 cloves garlic, minced"
            ],
            "instruction_strs": [
                "Preheat an outdoor grill for medium-high heat and lightly oil the grate.",
                "Mix together turkey, spinach, feta, eggs, and garlic in a large bowl until well combined; form "
                "into 8 patties.", "Cook patties on the preheated grill on both sides until no longer pink in "
                "the center, 15 to 20 minutes. An instant-read thermometer inserted into the center of patties should "
                "read at least 165 degrees F (74 degrees C)."
            ],
            "image": "https://www.allrecipes.com/thmb/cpf6Rics5oHGq1TZ1df5fEaImwM=/1500x0/filters:no_upscale():"
            "max_bytes(150000):strip_icc()/1360550-582be362ee99424bb4f363c2274a9d0d.jpg",
            "nutrients": {
                "calories": "233 kcal",
                "carbohydrateContent": "2 g",
                "cholesterolContent": "143 mg",
                "fiberContent": "1 g",
                "proteinContent": "27 g",
                "saturatedFatContent": "5 g",
                "sodiumContent": "266 mg",
                "sugarContent": "1 g",
                "fatContent": "13 g",
                "unsaturatedFatContent": "0 g"
            }
        },
        {
            "host": "allrecipes.com",
            "name": "Spinach and Feta Turkey Burgers",
            "time": 35,
            "unit": "default",
            "servings": 8,
            "ingredient_strs": [
                "cooking spray", "2 pounds ground turkey",
                "1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry", "4 ounces feta cheese",
                "2 large eggs, beaten", "2 cloves garlic, minced"
            ],
            "instruction_strs": [
                "Preheat an outdoor grill for medium-high heat and lightly oil the grate.",
                "Mix together turkey, spinach, feta, eggs, and garlic in a large bowl until well combined; form "
                "into 8 patties.", "Cook patties on the preheated grill on both sides until no longer pink in "
                "the center, 15 to 20 minutes. An instant-read thermometer inserted into the center of patties should "
                "read at least 165 degrees F (74 degrees C)."
            ],
            "image": "https://www.allrecipes.com/thmb/cpf6Rics5oHGq1TZ1df5fEaImwM=/1500x0/filters:no_upscale():"
            "max_bytes(150000):strip_icc()/1360550-582be362ee99424bb4f363c2274a9d0d.jpg",
            "nutrients": {
                "calories": "233 kcal",
                "carbohydrateContent": "2 g",
                "cholesterolContent": "143 mg",
                "fiberContent": "1 g",
                "proteinContent": "27 g",
                "saturatedFatContent": "5 g",
                "sodiumContent": "266 mg",
                "sugarContent": "1 g",
                "fatContent": "13 g",
                "unsaturatedFatContent": "0 g"
            },
            "ingredient_list": [
                Ingredient("cooking spray"),
                Ingredient("2 pounds ground turkey"),
                Ingredient("1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry"),
                Ingredient("4 ounces feta cheese"),
                Ingredient("2 large eggs, beaten"),
                Ingredient("2 cloves garlic, minced")
            ],
            "tags": [
                "spinach", "feta", "turkey", "burgers", "cooking", "spray", "ground", "turkey", "box", "frozen",
                "chopped", "spinach", "feta", "cheese", "eggs", "garlic", "allrecipes.com"
            ],
        }
    ),
    (
        {
            "host": "bbcgoodfood.com",
            "name": "Chicken pasta bake",
            "time": 75,
            "unit": "default",
            "servings": 6,
            "ingredient_strs": [
                "4 tbsp olive oil", "1 onion , finely chopped", "2 garlic cloves , crushed", "¼ tsp chilli flakes",
                "2 x 400g cans chopped tomatoes", "1 tsp caster sugar", "6 tbsp mascarpone",
                "4 skinless chicken breasts, sliced into strips", "300g penne", "70g mature cheddar , grated",
                "50g grated mozzarella", "½ small bunch of parsley , finely chopped"
            ],
            "instruction_strs": [
                "Heat 2 tbsp of the oil in a pan over a medium heat and fry the onion gently for 10-12 mins. Add "
                "the garlic and chilli flakes and cook for 1 min. Tip in the tomatoes and sugar and season to "
                "taste. Simmer uncovered for 20 mins or until thickened, then stir through the mascarpone.",
                "Heat 1 tbsp of oil in a non-stick frying pan. Season the chicken and fry for 5-7 mins or until "
                "the chicken is cooked through.",
                "Heat the oven to 220C/200C fan/gas 7. Cook the penne following pack instructions. Drain and toss "
                "with the remaining oil. Tip the pasta into a medium sized ovenproof dish. Stir in the chicken and "
                "pour over the sauce. Top with the cheddar, mozzarella and parsley. Bake for 20 mins or until "
                "golden brown and bubbling."
            ],
            "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chicken_pasta_bake"
            "-06fe2d6.jpg?resize=768,574",
            "nutrients": {
                "calories": "575 calories", "fatContent": "30 grams fat",
                "saturatedFatContent": "14 grams saturated fat", "carbohydrateContent": "41 grams carbohydrates",
                "sugarContent": "9 grams sugar", "fiberContent": "5 grams fiber",
                "proteinContent": "33 grams protein", "sodiumContent": "0.5 milligram of sodium"
            }
        },
        {
            "host": "bbcgoodfood.com",
            "name": "Chicken pasta bake",
            "time": 75,
            "unit": "default",
            "servings": 6,
            "ingredient_strs": [
                "4 tbsp olive oil", "1 onion , finely chopped", "2 garlic cloves , crushed", "¼ tsp chilli flakes",
                "2 x 400g cans chopped tomatoes", "1 tsp caster sugar", "6 tbsp mascarpone",
                "4 skinless chicken breasts, sliced into strips", "300g penne", "70g mature cheddar , grated",
                "50g grated mozzarella", "½ small bunch of parsley , finely chopped"
            ],
            "instruction_strs": [
                "Heat 2 tbsp of the oil in a pan over a medium heat and fry the onion gently for 10-12 mins. Add "
                "the garlic and chilli flakes and cook for 1 min. Tip in the tomatoes and sugar and season to "
                "taste. Simmer uncovered for 20 mins or until thickened, then stir through the mascarpone.",
                "Heat 1 tbsp of oil in a non-stick frying pan. Season the chicken and fry for 5-7 mins or until "
                "the chicken is cooked through.",
                "Heat the oven to 220C/200C fan/gas 7. Cook the penne following pack instructions. Drain and toss "
                "with the remaining oil. Tip the pasta into a medium sized ovenproof dish. Stir in the chicken and "
                "pour over the sauce. Top with the cheddar, mozzarella and parsley. Bake for 20 mins or until "
                "golden brown and bubbling."
            ],
            "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chicken_pasta_bake"
            "-06fe2d6.jpg?resize=768,574",
            "nutrients": {
                "calories": "575 calories", "fatContent": "30 grams fat",
                "saturatedFatContent": "14 grams saturated fat", "carbohydrateContent": "41 grams carbohydrates",
                "sugarContent": "9 grams sugar", "fiberContent": "5 grams fiber",
                "proteinContent": "33 grams protein", "sodiumContent": "0.5 milligram of sodium"
            },
            "ingredient_list": [
                Ingredient("4 tbsp olive oil"),
                Ingredient("1 onion , finely chopped"),
                Ingredient("2 garlic cloves , crushed"),
                Ingredient("¼ tsp chilli flakes"),
                Ingredient("2 x 400g cans chopped tomatoes"),
                Ingredient("1 tsp caster sugar"),
                Ingredient("6 tbsp mascarpone"),
                Ingredient("4 skinless chicken breasts, sliced into strips"),
                Ingredient("300g penne"),
                Ingredient("70g mature cheddar , grated"),
                Ingredient("50g grated mozzarella"),
                Ingredient("½ small bunch of parsley , finely chopped")
            ],
            "tags": [
                "chicken", "pasta", "bake", "olive", "oil", "onion", "cloves", "tsp", "chilli", "flakes", "cans",
                "chopped", "tomatoes", "caster", "sugar", "mascarpone", "chicken", "breasts", "penne", "mature",
                "cheddar", "grated", "mozzarella", "parsley", "bbcgoodfood.com"
            ],
        }
    ),
])
def test_initialize_with_kwargs(kwargs, expected):
    result = Recipe("whatever.com", **kwargs)

    for key, value in expected.items():
        assert result[key] == value, f"'{key}' contains '{result[key]}' value, expected '{value}'"


@pytest.mark.parametrize("url", [
    (
        "https://www.allrecipes.com/reicpe/"
    ),
    (
        "https://google.com/"
    ),
])
def test_error_on_initialize(url):
    with pytest.raises(Exception):
        Recipe(url)

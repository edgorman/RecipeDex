
import pytest
from recipedex.app import App


@pytest.mark.parametrize("url_list,expected", [
    (
        [
            "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/",
        ],
        {
            "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/": {
                "host": "allrecipes.com",
                "name": "Spinach and Feta Turkey Burgers",
                "time": 35,
                "servings": "8 servings",
                "ingredients": [
                    "2 eggs, beaten", "2 cloves garlic, minced", "4 ounces feta cheese",
                    "1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry", "2 pounds ground turkey"
                ],
                "instructions": [
                    "Preheat an outdoor grill for medium-high heat and lightly oil grate.",
                    "While the grill is preheating, mix together eggs, garlic, feta cheese, spinach, and turkey in a "
                    "large bowl until well combined; form into 8 patties.",
                    "Cook on preheated grill until no longer pink in the center, 15 to 20 minutes."
                ],
                "image_url": "https://www.allrecipes.com/thmb/cpf6Rics5oHGq1TZ1df5fEaImwM=/1500x0/filters:no_upscale():"
                "max_bytes(150000):strip_icc()/1360550-582be362ee99424bb4f363c2274a9d0d.jpg",
                "nutrients": {
                    "calories": "233 kcal", "carbohydrateContent": "2 g", "cholesterolContent": "143 mg",
                    "fatContent": "13 g", "fiberContent": "1 g", "proteinContent": "27 g",
                    "saturatedFatContent": "5 g", "sodiumContent": "266 mg", "sugarContent": "1 g",
                    "unsaturatedFatContent": "0 g"
                },
            }
        }
    ),
    (
        [
            "https://www.bbcgoodfood.com/recipes/chicken-pasta-bake",
        ],
        {
            "https://www.bbcgoodfood.com/recipes/chicken-pasta-bake": {
                "host": "bbcgoodfood.com",
                "name": "Chicken pasta bake",
                "time": 75,
                "servings": "6 servings",
                "ingredients": [
                    "4 tbsp olive oil", "1 onion , finely chopped", "2 garlic cloves , crushed", "¼ tsp chilli flakes",
                    "2 x 400g cans chopped tomatoes", "1 tsp caster sugar", "6 tbsp mascarpone",
                    "4 skinless chicken breasts, sliced into strips", "300g penne", "70g mature cheddar , grated",
                    "50g grated mozzarella", "½ small bunch of parsley , finely chopped"
                ],
                "instructions": [
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
                "image_url": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chicken_pasta_bake"
                "-06fe2d6.jpg?resize=768,574",
                "nutrients": {
                    "calories": "575 calories", "fatContent": "30 grams fat",
                    "saturatedFatContent": "14 grams saturated fat", "carbohydrateContent": "41 grams carbohydrates",
                    "sugarContent": "9 grams sugar", "fiberContent": "5 grams fiber",
                    "proteinContent": "33 grams protein", "sodiumContent": "0.5 milligram of sodium"
                }
            }
        }
    )
])
def test_parse_urls_successful(url_list, expected):
    assert App.parse_urls(url_list) == expected


def test_parse_urls_error_handling():
    url_list = [
        "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/",
        "https://www.allrecipes.com/reicpe/",
        "https://google.com/"
    ]

    assert len(App.parse_urls(url_list)) == 1


@pytest.mark.parametrize("ingredients,expected", [
    (
        [
            "2 eggs, beaten", "2 cloves garlic, minced", "4 ounces feta cheese",
            "1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry", "2 pounds ground turkey"
        ],
        [
            {"name": "eggs", "quantity": 2.0, "unit": "", "comment": "beaten"},
            {"name": "garlic", "quantity": 2.0, "unit": "clove", "comment": "minced"},
            {"name": "feta cheese", "quantity": 4.0, "unit": "oz", "comment": ""},
            {"name": "box frozen chopped spinach", "quantity": 1.0,
                "unit": "", "comment": "(10 ounce)  thawed and squeezed dry"},
            {"name": "ground turkey", "quantity": 2.0, "unit": "lb", "comment": ""}
        ]
    ),
    (
        [
            "4 tbsp olive oil", "1 onion , finely chopped", "2 garlic cloves , crushed", "1/4 tsp chilli flakes",
            "2 x 400g cans chopped tomatoes", "1 tsp caster sugar", "6 tbsp mascarpone",
            "4 skinless chicken breasts, sliced into strips", "300g penne", "70g mature cheddar , grated",
            "50g grated mozzarella", "1/2 small bunch of parsley , finely chopped"
        ],
        [
            {"name": "olive oil", "quantity": 4.0, "unit": "tbsp", "comment": ""},
            {"name": "onion", "quantity": 1.0, "unit": "", "comment": "finely chopped"},
            {"name": "garlic cloves", "quantity": 2.0, "unit": "", "comment": "crushed"},
            {"name": "chilli flakes", "quantity": 2.5, "unit": "tsp", "comment": ""},
            {"name": "x 400g cans chopped tomatoes", "quantity": 2.0, "unit": "", "comment": ""},
            {"name": "caster sugar", "quantity": 1.0, "unit": "tsp", "comment": ""},
            {"name": "mascarpone", "quantity": 6.0, "unit": "tbsp", "comment": ""},
            {"name": "skinless chicken breasts", "quantity": 4.0, "unit": "", "comment": "sliced into strips"},
            {"name": "penne", "quantity": 300.0, "unit": "g", "comment": ""},
            {"name": "mature cheddar", "quantity": 70.0, "unit": "g", "comment": "grated"},
            {"name": "grated mozzarella", "quantity": 50.0, "unit": "g", "comment": ""},
            {"name": "small bunch of parsley", "quantity": 1.5, "unit": "", "comment": "finely chopped"}
        ]
    )
])
def test_extract_ingredients(ingredients, expected):
    recipes_dict = {
        "url": {
            "name": "name",
            "ingredients": ingredients
        }
    }

    assert App.extract_ingredients(recipes_dict)["url"]["ingredients_list"] == expected

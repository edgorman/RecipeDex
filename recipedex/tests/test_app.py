
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
                    '2 eggs, beaten', '2 cloves garlic, minced', '4 ounces feta cheese',
                    '1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry', '2 pounds ground turkey'
                ],
                "instructions": [
                    'Preheat an outdoor grill for medium-high heat and lightly oil grate.',
                    'While the grill is preheating, mix together eggs, garlic, feta cheese, spinach, and turkey in a large bowl until well combined; form into 8 patties.', 
                    'Cook on preheated grill until no longer pink in the center, 15 to 20 minutes.'
                ],
                "image_url": "https://www.allrecipes.com/thmb/cpf6Rics5oHGq1TZ1df5fEaImwM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/1360550-582be362ee99424bb4f363c2274a9d0d.jpg",
                "nutrients": {
                    'calories': '233 kcal', 'carbohydrateContent': '2 g', 'cholesterolContent': '143 mg',
                    'fatContent': '13 g', 'fiberContent': '1 g', 'proteinContent': '27 g', 
                    'saturatedFatContent': '5 g', 'sodiumContent': '266 mg', 'sugarContent': '1 g',
                    'unsaturatedFatContent': '0 g'
                },
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

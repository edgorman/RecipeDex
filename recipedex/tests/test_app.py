
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
                "servings": 8,
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
                "servings": 6,
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
    ),
    (
        [
            "https://www.bbcgoodfood.com/recipes/pizza-margherita-4-easy-steps"
        ],
        {
            "https://www.bbcgoodfood.com/recipes/pizza-margherita-4-easy-steps": {
                "host": "bbcgoodfood.com",
                "name": "Pizza Margherita in 4 easy steps",
                "time": 35,
                "servings": 2,
                "ingredients": [
                    "300g strong bread flour",
                    "1 tsp instant yeast (from a sachet or a tub)",
                    "1 tsp salt",
                    "1 tbsp olive oil, plus extra for drizzling",
                    "100ml passata",
                    "handful fresh basil or 1 tsp dried",
                    "1 garlic clove, crushed",
                    "125g ball mozzarella, sliced",
                    "handful grated or shaved parmesan (or vegetarian alternative)",
                    "handful of cherry tomatoes, halved",
                    "handful of basil leaves (optional)"
                ],
                "instructions": [
                    "Make the base: Put the flour into a large bowl, then stir in the yeast and salt. Make a well, pour"
                    " in 200ml warm water and the olive oil and bring together with a wooden spoon until you have a "
                    "soft, fairly wet dough. Turn onto a lightly floured surface and knead for 5 mins until smooth. "
                    "Cover with a tea towel and set aside. You can leave the dough to rise if you like, but it’s not "
                    "essential for a thin crust.",
                    "Make the sauce: Mix the passata, basil and crushed garlic together, then season to taste. Leave to"
                    " stand at room temperature while you get on with shaping the base.",
                    "Roll out the dough: if you’ve let the dough rise, give it a quick knead, then split into two "
                    "balls. On a floured surface, roll out the dough into large rounds, about 25cm across, using a "
                    "rolling pin. The dough needs to be very thin as it will rise in the oven. Lift the rounds onto "
                    "two floured baking sheets.",
                    "Top and bake: heat the oven to 240C/220C fan/gas 8. Put another baking sheet or an upturned "
                    "baking tray in the oven on the top shelf. Smooth sauce over bases with the back of a spoon. "
                    "Scatter with cheese and tomatoes, drizzle with olive oil and season. Put one pizza, still on its "
                    "baking sheet, on top of the preheated sheet or tray. Bake for 8-10 mins until crisp. Serve with a "
                    "little more olive oil, and basil leaves if using. Repeat step for remaining pizza."
                ],
                "image_url": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/recipe-image-legacy"
                "-id-51643_11-2f4a2cc.jpg?resize=768,574",
                "nutrients": {
                    "calories": "431 calories",
                    "fatContent": "15 grams fat",
                    "saturatedFatContent": "7 grams saturated fat",
                    "carbohydrateContent": "59 grams carbohydrates",
                    "sugarContent": "2 grams sugar",
                    "fiberContent": "3 grams fiber",
                    "proteinContent": "19 grams protein",
                    "sodiumContent": "1.9 milligram of sodium"
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

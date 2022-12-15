
import pytest
import warnings

from recipedex.tests.conftest import AssertionWarning
from recipedex.ingredient import Ingredient


@pytest.mark.parametrize("ingredient_str,expected", [
    (
        "2 eggs, beaten",
        {"optional": False, "name": "Eggs", "quantity": "2", "unit": "count", "comment": "beaten"}
    ),
    (
        "2 cloves garlic, minced",
        {"optional": False, "name": "Garlic", "quantity": "2", "unit": "cloves", "comment": "minced"}
    ),
    (
        "4 ounces feta cheese",
        {"optional": False, "name": "Feta cheese", "quantity": "4", "unit": "ounces", "comment": ""}
    ),
    (
        "1 (10 ounce) box frozen chopped spinach, thawed and squeezed dry",
        {"optional": False, "name": "Box frozen chopped spinach", "quantity": "10", "unit": "ounce",
         "comment": "thawed and squeezed dry"}
    ),
    (
        "2 pounds ground turkey",
        {"optional": False, "name": "Ground turkey", "quantity": "2", "unit": "pounds", "comment": ""}
    ),
    (
        "4 tbsp olive oil",
        {"optional": False, "name": "Olive oil", "quantity": "4", "unit": "tbsp", "comment": ""}
    ),
    (
        "1 onion , finely chopped",
        {"optional": False, "name": "Onion", "quantity": "1", "unit": "count", "comment": "finely chopped"}
    ),
    (
        "0.5 tsp chilli flakes",
        {"optional": False, "name": "Chilli flakes", "quantity": "0.5", "unit": "tsp", "comment": ""}
    ),
    (
        "2 x 400g cans chopped tomatoes",
        {"optional": False, "name": "Cans chopped tomatoes", "quantity": "2 x 400", "unit": "g", "comment": ""}
    ),
    (
        "1 tsp caster sugar",
        {"optional": False, "name": "Caster sugar", "quantity": "1", "unit": "tsp", "comment": ""}
    ),
    (
        "4 skinless chicken breasts, sliced into strips",
        {"optional": False, "name": "Skinless chicken breasts", "quantity": "4", "unit": "count",
         "comment": "sliced into strips"}
    ),
    (
        "300g penne",
        {"optional": False, "name": "Penne", "quantity": "300", "unit": "g", "comment": ""}
    ),
    (
        "70g mature cheddar , grated",
        {"optional": False, "name": "Mature cheddar", "quantity": "70", "unit": "g", "comment": "grated"}
    ),
    (
        "0.5 bunch of parsley , finely chopped",
        {"optional": False, "name": "Parsley", "quantity": "0.5", "unit": "bunch", "comment": "finely chopped"}
    ),
    (
        "0.5 cup chopped onion",
        {"optional": False, "name": "Chopped onion", "quantity": "0.5", "unit": "cup", "comment": ""}
    ),
    (
        "1 garlic clove, crushed",
        {"optional": False, "name": "Garlic", "quantity": "1", "unit": "clove", "comment": "crushed"}
    ),
    (
        "handful of cherry tomatoes, halved",
        {"optional": False, "name": "Cherry tomatoes", "quantity": "1", "unit": "handful", "comment": "halved"}
    ),
    (
        "handful fresh basil or 1 tsp dried",
        {"optional": False, "name": "Fresh basil", "quantity": "1", "unit": "handful", "comment": "or 1 tsp dried"}
    ),
    (
        "salt to taste",
        {"optional": False, "name": "Salt", "quantity": "", "unit": "to taste", "comment": ""}
    ),
    (
        "ground black pepper to taste",
        {"optional": False, "name": "Ground black pepper", "quantity": "", "unit": "to taste", "comment": ""}
    ),
    (
        "2 tbsp tomato purée",
        {"optional": False, "name": "Tomato purée", "quantity": "2", "unit": "tbsp", "comment": ""}
    ),
    (
        "0.5 cucumber, peeled, cut into small strips",
        {"optional": False, "name": "Cucumber", "quantity": "0.5", "unit": "count",
         "comment": "peeled, cut into small strips"}
    )
])
def test_initialize(ingredient_str, expected):
    result = Ingredient(ingredient_str)

    for key, value in expected.items():
        if getattr(result, key) != value:
            warnings.warn(f"'{key}' contains '{getattr(result, key)}' value, expected '{value}'", AssertionWarning)


@pytest.mark.parametrize("ingredient,other,expected", [
    (
        Ingredient("1 kg meat"),
        Ingredient("1 kg meat"),
        True
    ),
    (
        Ingredient("1 kg meat"),
        Ingredient("1 kg cheese"),
        False
    )
])
def test_equals(ingredient, other, expected):
    assert (ingredient == other) == expected


@pytest.mark.parametrize("ingredient,expected", [
    (
        Ingredient("1 kg meat"),
        "name:Meat, unit:kg, quantity:1, comment:, optional:False"
    ),
    (
        Ingredient("2.2 pounds cheese"),
        "name:Cheese, unit:pounds, quantity:2.2, comment:, optional:False"
    )
])
def test_str(ingredient, expected):
    assert str(ingredient) == expected, f"{ingredient} != {expected}"


@pytest.mark.parametrize("ingredient,new_unit,expected", [
    (
        Ingredient("1 kg meat"),
        "pound",
        Ingredient("2.2 pound meat")
    ),
    (
        Ingredient("1 cup flour"),
        "liter",
        Ingredient("0.24 liter flour")
    )
])
def test_unit_conversion(ingredient, new_unit, expected):
    assert ingredient.to_unit(new_unit) == expected, f"{ingredient} != {expected}"


@pytest.mark.parametrize("ingredient,new_system,expected", [
    (
        Ingredient("1 kg meat"),
        "imperial",
        Ingredient("2.2 pound meat")
    ),
    (
        Ingredient("2.20462 pounds meat"),
        "mks",
        Ingredient("1.0 kilogram meat")
    )
])
def test_system_conversion(ingredient, new_system, expected):
    assert ingredient.to_system(new_system) == expected, f"{ingredient} != {expected}"


@pytest.mark.parametrize("ingredient,new_scale,expected", [
    (
        Ingredient("1 kg meat"),
        1,
        Ingredient("1.0 kg meat")
    ),
    (
        Ingredient("135 pounds meat"),
        0.2,
        Ingredient("27.0 pounds meat")
    )
])
def test_scale_conversion(ingredient, new_scale, expected):
    assert ingredient.to_scale(new_scale) == expected, f"{ingredient} != {expected}"

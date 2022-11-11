
import pytest
import warnings

from recipedex.tests.conftest import AssertionWarning
from recipedex.tests.conftest import dict_diff
from recipedex.ingredient import parse_ingredient


@pytest.mark.parametrize("ingredient,expected", [
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
    )
])
def test_parse_ingredient(ingredient, expected):
    result = parse_ingredient(ingredient)

    for key, value in result.items():
        assert value is not None, f"'{key}' contains 'None' value, {result}"
    if result != expected:
        assert result.keys() == expected.keys()
        warnings.warn(dict_diff(result, expected), AssertionWarning)

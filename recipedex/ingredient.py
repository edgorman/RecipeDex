
import nltk
import regex as re
from pint import UnitRegistry
nltk.download('stopwords')


MANUAL_UNITS = [
    "pinch",
    "envelope",
    "dash",
    "can",
    "whole",
    "head",
    "clove",
    "bunch",
    "handful",
    "piece",
    "strip",
    "splash",
    "stick"
]
STOP_WORDS = nltk.corpus.stopwords.words('english') + [
    "small",
    "medium",
    "large"
]


def parse_ingredient(ingredient: str) -> dict:
    '''
        Parse the string on an ingredient into its principal components

        Parameters:
            ingredient: string version of the ingredient

        Returns:
            ingredient_dict: dictionary version of the ingredient
    '''
    name = None
    unit = None
    quantity = None
    comment = None
    optional = False

    # Search for optional text and remove from string
    optional = "option" in ingredient
    ingredient = re.sub(r"(\S*option\S*)", "", ingredient)

    # Find comment and remove from string
    comment = ", ".join(
        re.sub(r"(\(|\)|^,\s*)", "", i)
        for i in re.findall(r"(, (?:.+)|\((?:.+)\)|(?:or .+))", ingredient)
    )
    ingredient = re.sub(r"(, .+)|(\(.*\))|(or .*)", "", ingredient)

    # Find qunatity and unit by
    try:
        # Quantity followed by unit
        quantity, unit = re.search(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", ingredient).groups()
        ingredient = re.sub(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", "", ingredient)
    except:  # noqa: E722
        try:
            # Manual unit with no number
            quantity, unit = "1", re.search(r"(" + "|".join(MANUAL_UNITS) + r")\w*\s", ingredient).group(1)
            ingredient = re.sub(r"(" + "|".join(MANUAL_UNITS) + r")\w*\s", "", ingredient)
        except:  # noqa: E722
            try:
                # Check comment contains number
                quantity, unit = re.search(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", comment).groups()
                comment = re.sub(r"(, )?(" + quantity + r") ?(" + unit + r")(, )?", "", comment)
            except:  # noqa: E722
                quantity, unit = "", ""

    # Crop quantity decimals that are longer than two
    quantity = re.sub(r"(\d+\.\d{3,})", lambda q: re.search(r"(\d+\.\d{0,2})", q.group()).group(), quantity)

    # Parse rest of ingredient
    ingredient = ingredient.strip()
    if len(ingredient) > 0:
        # Unique case where string contains "to taste"
        if "to taste" in ingredient and len(unit) == 0:
            name = re.sub(r"(\s?to taste)", "", ingredient)
            unit = "to taste"
        # Else, remove stop words, numbers, and punctuation
        else:
            name = " ".join([i for i in re.findall(r"([^\W\d_]+)", ingredient, re.UNICODE) if i not in STOP_WORDS])
    else:
        # Unit must actually be the name (e.g. 2 eggs)
        name, unit = unit, "count"

    # Return ingredient as a dictionary object
    return {
        "name": name.lower().capitalize(),
        "unit": unit,
        "quantity": quantity,
        "comment": comment.lower(),
        "optional": optional
    }


def convert_to_unit(ingredient: dict, new_unit: str) -> dict:
    '''
        Convert the ingredient to the new unit, updating the quantity if necessary

        Parameters:
            ingredient: dictionary containing ingredient unit and quantity
            new_unit: the new unit to change the ingredient to
        
        Returns:
            ingredient: new dictionary with updated unit and quantity
    '''
    # Parse current ingredient using Pint package
    ureg = UnitRegistry()
    curr = ureg.Quantity(float(ingredient["quantity"]), ingredient["unit"])

    # Check if new unit can convert the old unit
    assert curr.check(new_unit), f"Cannot convert from '{str(curr.units)}' to '{new_unit}'."
    curr = curr.to(new_unit)

    # Update dictionary and return with conversion
    ingredient.update({
        "quantity": str(round(curr.magnitude, 2)),
        "unit": str(curr.units)
    })
    return ingredient


def convert_to_system(ingredient: dict, new_system: str) -> dict:
    '''
        Convert the ingredient to the new unit system, updating the quantity if necessary

        Parameters:
            ingredient: dictionary containing ingredient unit and quantity
            new_system: the new unit system to change the ingredient to
        
        Returns:
            ingredient: new dictionary with updated unit and quantity
    '''
    # Parse current ingredient using Pint package
    ureg = UnitRegistry()
    curr = ureg.Quantity(float(ingredient["quantity"]), ingredient["unit"])

    # Change to new unit system
    ureg.default_system = new_system
    curr = curr.to_base_units().to_compact()

    # Update dictionary and return with conversion
    ingredient.update({
        "quantity": str(round(curr.magnitude, 2)),
        "unit": str(curr.units)
    })
    return ingredient

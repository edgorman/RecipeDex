import nltk
import logging
import regex as re
from pint import UnitRegistry


logger = logging.getLogger("recipedex.ingredient")

MANUAL_UNITS = "|".join([
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
])
STOP_WORDS = nltk.corpus.stopwords.words('english') + [
    "small",
    "medium",
    "large"
]


class Ingredient:
    nltk.download("stopwords", quiet=True)
    self.ureg = UnitRegistry()

    def __init__(self, value: str):
        '''
            Initialise an Ingredient object by parsing the value string

            Parameters:
                value: String version of ingredients
            Returns:
                None
        '''

        self.name = ""
        self.unit = ""
        self.quantity = ""
        self.comment = ""
        self.optional = False

        # Search for optional text and remove from string
        self.optional = "option" in value
        value = re.sub(r"(\S*option\S*)", "", value)

        # Find comment and remove from string
        self.comment = ", ".join(
            re.sub(r"(\(|\)|^,\s*)", "", i)
            for i in re.findall(r"(, (?:.+)|\((?:.+)\)|(?:or .+))", value)
        )
        value = re.sub(r"(, .+)|(\(.*\))|(or .*)", "", value)

        # Find qunatity and unit by
        try:
            # Quantity followed by unit
            self.quantity, self.unit = re.search(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", value).groups()
            value = re.sub(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", "", value)
        except:  # noqa: E722
            try:
                # Manual unit with no number
                self.quantity, self.unit = "1", re.search(r"(" + MANUAL_UNITS + r")\w*\s", value).group(1)
                value = re.sub(r"(" + MANUAL_UNITS + r")\w*\s", "", value)
            except:  # noqa: E722
                try:
                    # Check comment contains number
                    self.quantity, self.unit = re.search(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", self.comment).groups()
                    self.comment = re.sub(
                        r"(, )?(" + self.quantity + r") ?(" + self.unit + r")(, )?", "", self.comment
                    )
                except:  # noqa: E722
                    self.quantity, self.unit = "", ""

        # Crop quantity decimals that are longer than two
        self.quantity = re.sub(
            r"(\d+\.\d{3,})", lambda q: re.search(r"(\d+\.\d{0,2})", q.group()).group(), self.quantity
        )

        # Parse rest of ingredient
        value = value.strip()
        if len(value) > 0:
            # Unique case where string contains "to taste"
            if "to taste" in value and len(self.unit) == 0:
                self.name = re.sub(r"(\s?to taste)", "", value)
                self.unit = "to taste"
            # Else, remove stop words, numbers, and punctuation
            else:
                self.name = " ".join([i for i in re.findall(r"([^\W\d_]+)", value, re.UNICODE) if i not in STOP_WORDS])
        else:
            # Unit must actually be the name (e.g. 2 eggs)
            self.name, self.unit = self.unit, "count"

        # Final operations on class variables
        self.name = self.name.lower().capitalize()
        self.comment = self.comment.lower()


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


def convert_to_system(ingredients: list, system: str) -> list:
    '''
        Convert the list of ingredients to the new unit system, updating the quantity if necessary

        Parameters:
            ingredients: list containing ingredients with unit and quantity
            system: the new unit system to change the ingredients to

        Returns:
            ingredients: new list with updated units and quantities
    '''
    # Set new default unit system using pint package
    ureg.default_system = system

    for i in range(len(ingredients)):
        try:
            # Convert ingredient
            curr = ureg.Quantity(float(ingredients[i]["quantity"]), ingredients[i]["unit"])
            curr = curr.to_base_units().to_reduced_units()

            # Update ingredient dictionary
            ingredients[i].update({
                "quantity": str(round(curr.magnitude, 2)),
                "unit": str(curr.units)
            })
        except Exception as e:
            logger.warning(f"Could not convert ingredient {ingredients[i]} to unit system {system}: {str(e)}")

    return ingredients


def scale_to_amount(ingredients: list, scale: float) -> list:
    '''
        Scale the list of ingredients by a factor of 'scale', updating the quantity if necessary

        Parameters:
            ingredients: list containing ingredients with unit and quantity
            scale: the amount to scale the quantities by

        Returns:
            ingredients: new list with updated units and quantities
    '''
    for i in range(len(ingredients)):
        try:
            # Update ingredient dictionary
            ingredients[i].update({
                "quantity": str(float(ingredients[i]["quantity"]) * scale)
            })
        except Exception as e:
            logger.warning(f"Could not scale ingredient {ingredients[i]} by a factor of {scale}: {str(e)}")

    return ingredients

import json
import nltk
import logging
import regex as re
from pint import UnitRegistry

nltk.download("stopwords", quiet=True)


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
UREG = UnitRegistry()


class Ingredient(dict):

    def __init__(self, value: str):
        '''
            Initialise an Ingredient object by parsing the value string

            Parameters:
                value: String version of ingredients
            Returns:
                None
        '''
        super(Ingredient, self).__init__(name="", unit="", quantity="", comment="", optional=False)

        # Search for optional text and remove from string
        self["optional"] = "option" in value
        value = re.sub(r"(\S*option\S*)", "", value)

        # Find comment and remove from string
        self["comment"] = ", ".join(
            re.sub(r"(\(|\)|^,\s*)", "", i)
            for i in re.findall(r"(, (?:.+)|\((?:.+)\)|(?:or .+))", value)
        )
        value = re.sub(r"(, .+)|(\(.*\))|(or .*)", "", value)

        # Find qunatity and unit by
        try:
            # Quantity followed by unit
            self["quantity"], self["unit"] = re.search(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", value).groups()
            value = re.sub(r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", "", value)
        except:  # noqa: E722
            try:
                # Manual unit with no number
                self["quantity"], self["unit"] = "1", re.search(r"(" + MANUAL_UNITS + r")\w*\s", value).group(1)
                value = re.sub(r"(" + MANUAL_UNITS + r")\w*\s", "", value)
            except:  # noqa: E722
                try:
                    # Check comment contains number
                    self["quantity"], self["unit"] = re.search(
                        r"(\d\s*x\s*\d+|\d*\.\d+|\d+) ?(\w+)", self["comment"]
                    ).groups()
                    self["comment"] = re.sub(
                        r"(, )?(" + self["quantity"] + r") ?(" + self["unit"] + r")(, )?", "", self["comment"]
                    )
                except:  # noqa: E722
                    self["quantity"], self["unit"] = "", ""

        # Crop quantity decimals that are longer than two
        self["quantity"] = re.sub(
            r"(\d+\.\d{3,})", lambda q: re.search(r"(\d+\.\d{0,2})", q.group()).group(), self["quantity"]
        )

        # Parse rest of ingredient
        value = value.strip()
        if len(value) > 0:
            # Unique case where string contains "to taste"
            if "to taste" in value and len(self["unit"]) == 0:
                self["name"] = re.sub(r"(\s?to taste)", "", value)
                self["unit"] = "to taste"
            # Else, remove stop words, numbers, and punctuation
            else:
                self["name"] = " ".join([
                    i for i in re.findall(r"([^\W\d_]+)", value, re.UNICODE) if i not in STOP_WORDS
                ])
        else:
            # Unit must actually be the name (e.g. 2 eggs)
            self["name"], self["unit"] = self["unit"], "count"

        # Final operations on class variables
        self["name"] = self["name"].lower().capitalize()
        self["comment"] = self["comment"].lower()
    
    def to_unit(self, unit: str):
        '''
            Convert to the new unit, updating the quantity if necessary

            Parameters:
                unit: name of the unit to convert to

            Returns:
                None
        '''

        # Parse current ingredient using Pint package
        quantity = UREG.Quantity(float(self["quantity"]), self["unit"])

        # Assert new unit can convert from old unit
        assert quantity.check(unit), f"Cannot convert from '{str(quantity.units)}' to '{unit}'."
        quantity = quantity.to(unit)

        # Update this object's variables
        self["quantity"] = str(round(quantity.magnitude, 2))
        self["unit"] = str(quantity.units)

        return self
    
    def to_system(self, system: str):
        '''
            Convert to the new unit system, updating the quantity if necessary

            Parameters:
                system: name of the unit system to convert to

            Returns:
                None
        '''

        # Set new default unit system using pint package
        UREG.default_system = system
        
        # Convert this ingredient to the new system
        quantity = UREG.Quantity(float(self["quantity"]), self["unit"])
        quantity = quantity.to_base_units().to_reduced_units()

        # Update this object's variables
        self["quantity"] = str(round(quantity.magnitude, 2))
        self["unit"] = str(quantity.units)

        return self
    
    def to_scale(self, scale: float):
        '''
            Adjust quantity to the new scale, updating the unit if necessary

            Parameters:
                scale: amount to scale the quantity by

            Returns:
                None
        '''

        # Scale this ingredient and update this object's variables
        self["quantity"] = str(round(float(self["quantity"]) * scale, 2))

        return self

    def extract_tags(self):
        '''
            Extract the tags from the properties of this ingredient

            Parameters:
                None
            
            Returns:
                tags: List of keywords from properties
        '''

        # Extract each word in the name field
        tags = [n.lower() for n in self["name"].split()]

        # Remove stop words that appear in the tags list
        def is_readable(tag):
            return not tag.isnumeric() and tag not in nltk.corpus.stopwords.words("english")
        tags = list(filter(is_readable, tags))

        return tags

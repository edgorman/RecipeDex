
import nltk
import regex as re
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
    "piece"
]
FRACTIONS = "\u00BC-\u00BE\u2150-\u215E"
STOP_WORDS = nltk.corpus.stopwords.words('english')

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
        re.findall(r", (.+)", ingredient) + 
        re.findall(r"\((.+)\)", ingredient) + 
        re.findall(r"(or .+)", ingredient)
    )
    ingredient = re.sub(r"(, .+)|(\(.*\))|(or .*)", "", ingredient)

    try:
        # Find quantity followed by unit
        quantity, unit = re.search(r"(\d\s*x\s*\d+|\d/\d|\d+|[" + FRACTIONS + r"]) ?(\w+)", ingredient).groups()
        ingredient = re.sub(r"(\d\s*x\s*\d+|\d/\d|\d+|[" + FRACTIONS + r"]) ?(\w+)", "", ingredient)
    except:
        try:
            # Find manual unit (assumes quantity is 1)
            quantity, unit = "1", re.search(r"("+ "|".join(MANUAL_UNITS) + r")\w*\s", ingredient).group(1)
            ingredient = re.sub(r"("+ "|".join(MANUAL_UNITS) + r")\w*\s", "", ingredient)
        except:
            try:
                # Check comment contains quantity and unit
                quantity, unit = re.search(r"(\d\s*x\s*\d+|\d/\d|\d+|[" + FRACTIONS + r"]) ?(\w+)", comment).groups()
                comment = re.sub(r"(, )?("+quantity+r") ?("+unit+r")", "", comment)
            except:
                # Not found, set each as empty strings
                quantity, unit = "", ""
    
    # Parse rest of ingredient
    ingredient = ingredient.strip()

    if len(ingredient) > 0:
        if "to taste" in ingredient:
            name = ingredient
        else:
            # Remove stop words, numbers and punctuation from string
            name = " ".join([i for i in re.findall(r"([a-zA-Z]+)", ingredient) if i not in STOP_WORDS])
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

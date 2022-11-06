# RecipeDex - Module
This is the python module that performs the parsing and manipulates the recipes using natural langauge processing (NLP) techniques. This README assumes you have set up the developer environment as detailed in the base directory of this repository.

## Installation

Install the required python packages (in parent directory since it includes backend packages):

```
python -m pip install -r requirements.txt
```

## Usage

```
usage: RecipeDex [-h] [-verbose] [-version] url

Automatically parse and extract info from recipes.

positional arguments:
  url         the url to parse

options:
  -h, --help  show this help message and exit
  -verbose    show extra output
  -version    show program's version number and exit
```

Examples:

```
python -m recipedex https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/ --verbose
```

If python packages are added, update the requirements.txt:

```
python -m pip freeze > requirements.txt
```

## Testing

Run the testing scripts in the base directory:

```
python -m autopep8 . --in-place --aggressive --recursive --max-line-length 120
python -m flake8 . --max-line-length=120
python -m pytest -vv recipedex/tests/ --disable-pytest-warnings --cov=recipedex --cov-config=recipedex/tests/.coveragerc
```

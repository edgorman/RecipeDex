# RecipeDex - Module
This is the python module that performs recipe and ingredient parsing using the [Recipe Scraper](https://github.com/hhursev/recipe-scrapers) and the [Parse Ingredients](https://github.com/MichielMag/parse-ingredients) packages. This README assumes you have set up the developer environment as detailed in the base directory of this repository.

## Installation

Install the required python packages:

```
python -m pip install recipedex/.
```

If you're developing this package a handy line to reinstall is:
```
python -m pip uninstall recipedex -y; python -m pip install recipedex/.
```

## Usage

```
usage: recipedex [-h] [--metric] [--imperial] [--log {CRITICAL,ERROR,WARNING,INFO,DEBUG}] [--version] urls [urls ...]

Automatically parse and extract info from recipes.

positional arguments:
  urls                  the urls to parse

options:
  -h, --help            show this help message and exit
  --metric              force units to be metric
  --imperial            force units to be imperial
  --log {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        the log level
  --version             show program's version number and exit
```

Example:

```
python -m recipedex https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/ --log DEBUG
```

## Testing

Run the testing scripts in the base directory:

```
python -m autopep8 recipedex/ --in-place --aggressive --recursive --max-line-length 120
python -m flake8 recipedex/ --max-line-length=120
python -m pytest -svv recipedex/tests/
```

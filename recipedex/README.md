# RecipeDex - Module
This is the python module that performs the parsing and manipulates the recipes using natural langauge processing (NLP) techniques. This README assumes you have set up the developer environment as detailed in the base directory of this repository.

[![.github/workflows/pipeline.yml](https://github.com/edgorman/RecipeDex/actions/workflows/pipeline.yml/badge.svg)](https://github.com/edgorman/RecipeDex/actions/workflows/pipeline.yml)

## Installation

Install the required python packages:

```
python -m pip install recipedex/.
```

If you're developing this package a handy line to reinstall is:
```
python -m pip uninstall recipedex -y; python -m pip install recipedex/.
```

If python packages are added, update the setup.py file by using the following:

```
python -m pip freeze
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

Example:

```
python -m recipedex https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/ --verbose
```

## Testing

Run the testing scripts in the base directory:

```
python -m autopep8 . --in-place --aggressive --recursive --max-line-length 120
python -m flake8 . --max-line-length=120
python -m pytest -svv recipedex/tests/ --disable-pytest-warnings --cov=recipedex --cov-config=recipedex/tests/.coveragerc
```

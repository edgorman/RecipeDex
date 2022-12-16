from setuptools import setup
from setuptools import find_packages

setup(
    name='recipedex',
    version='1.0.0',
    description='Automatically parse and extract info from recipes.',
    author='Edward Gorman',
    author_email='',
    packages=find_packages('.'),
    install_requires=[
        "autopep8",
        "beautifulsoup4",
        "coverage",
        "regex",
        "flake8",
        "nltk",
        "pint",
        "numpy",
        "parse-ingredients",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-mock",
        "recipe-scrapers"
    ]
)

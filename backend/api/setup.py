from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='api',
    version='0.0.1',
    author='edgorman',
    author_email='ejgorman@gmail.com',
    packages=find_packages('.'),
    install_requires=required_packages
)

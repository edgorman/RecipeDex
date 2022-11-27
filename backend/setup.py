from setuptools import setup
from setuptools import find_packages

setup(
    name='backend',
    version='1.0.0',
    description='Host the FastAPI and MongoDB backend for recipedex.',
    author='Edward Gorman',
    author_email='',
    packages=find_packages('.'),
    install_requires=[
        "recipedex",
        "fastapi",
        "slowapi",
        "uvicorn",
        "motor",
        "pylru",
    ]
)

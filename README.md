# RecipeDex
A Software as a Service (SAAS) application for storing, indexing, and searching recipes from most recipes on the internet. A full-stack web application based on the FARM stack including [FastAPI](https://fastapi.tiangolo.com/), [React](https://reactjs.org/), and [MongoDB](https://www.mongodb.com/). Planned deployment to the [Google Cloud Platform](https://cloud.google.com/) coming 2023.

[![.github/workflows/pipeline.yml](https://github.com/edgorman/RecipeDex/actions/workflows/pipeline.yml/badge.svg)](https://github.com/edgorman/RecipeDex/actions/workflows/pipeline.yml)

## Description

All too often recipes are listed on websites that contain many burdensome ads as well as long paragraphs that are irrelevant to the task at hand. This will not be the first website to extract a recipe from a given URL, but it does aim to be one that gives a greater experience in regards to search functionality and ability to manipulate ingredients quickly and easily.

But more importantly this project is for me to learn a new tech stack so don't expect years of maintenance for free. There will be some useful documentation in the `\docs` folder containing instructions for developers to set up their [developer environments](docs/developer.md) as well as documents detailing the planned future sprints of development.

## Structure

The codebase is divided into three primary folders:

`recipedex`: This is the python module where the heavy-lifting website crawling is implemented using the [Recipe Scraper](https://github.com/hhursev/recipe-scrapers) and [Parse Ingredient](https://github.com/MichielMag/parse-ingredients) modules. There will also be some additional extraction of metadata and other useful features from the web page where available.

`backend`: Another python module that serves as the apps API via [FastAPI](https://fastapi.tiangolo.com/) and data storage via [MongoDB](https://www.mongodb.com/). The service is not planned to store all data scraped from recipes but will save the minimum required for indexing and searching functions to execute rapidly.

`frontend`: This section uses the javascript libraries [Node.js](https://nodejs.org/en/) and [React](https://reactjs.org/) to implement the web facing aspect of the service. The aim is for this service to support both mobile and desktop devices, prioritising user experience in regards to ease of use and response times.

## License

TODO

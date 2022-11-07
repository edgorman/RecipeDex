# RecipeDex
A Software as a Service (SAAS) application for storing, indexing and searching recipes from all across the web. The Python module uses the [Recipe Scraper](https://github.com/hhursev/recipe-scrapers) and the [Parse Ingredients](https://github.com/MichielMag/parse-ingredients) packages. Web application based on the FARM stack ([FastAPI](https://fastapi.tiangolo.com/), [React](https://reactjs.org/), [MongoDB](https://www.mongodb.com/)). Planned deployment to the [Google Cloud Platform](https://cloud.google.com/) coming 2023.

This README contains instructions for setting up the developer environment, for more specific instruction on setting up the backend/frontend/recipedex module see the README's within those folders.

[![.github/workflows/pipeline.yml](https://github.com/edgorman/RecipeDex/actions/workflows/pipeline.yml/badge.svg)](https://github.com/edgorman/RecipeDex/actions/workflows/pipeline.yml)

## Installation

Install Vagrant and VirtualBox to your machine:

```
Vagrant 2.2.19
VirtualBox 6.1
```

Use the following commands to clone the repository:

```
cd your/repo/directory
git clone https://github.com/edgorman/RecipeDex
```

Start and provision the dev virtual machine (this may take ~5 minutes):

```
cd RecipeDex
vagrant up
```

(Optional) Get the ssh credentials and store in your ssh config file:

```
vagrant ssh-config
~/.ssh/config <- copy and paste into here
```

(Optional) Set up VSCode to use remote dev vm for development:

```
Install Remote Explorer from extensions
Add the SSH Target from your ssh config file
```

Once SSH'd in, configure git with your email and name:
```
git config --global user.email "email@example.com"
git config --global user.name "firstname lastname"
```

## Usage

TODO

## Deployment

TODO

# License

TODO

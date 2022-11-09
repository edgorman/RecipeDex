# Developer

This README contains instructions for setting up the developer environment, for more specific instruction on setting up the backend/frontend/recipedex module see the README's within those folders.

## Structure

The codebase is divided into three primary folders:

`recipedex`: This is the python module where the heavy-lifting website crawling is implemented using the [Recipe Scraper](https://github.com/hhursev/recipe-scrapers) and [Parse Ingredient](https://github.com/MichielMag/parse-ingredients) modules. There will also be some additional extraction of metadata and other useful features from the web page where available.

`backend`: Another python module that serves as the apps API via [FastAPI](https://fastapi.tiangolo.com/) and data storage via [MongoDB](https://www.mongodb.com/). The service is not planned to store all data scraped from recipes but will save the minimum required for indexing and searching functions to execute rapidly.

`frontend`: This section uses the javascript libraries [Node.js](https://nodejs.org/en/) and [React](https://reactjs.org/) to implement the web facing aspect of the service. The aim is for this service to support both mobile and desktop devices, prioritising user experience in regards to ease of use and response times.

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

## Deployment

TODO

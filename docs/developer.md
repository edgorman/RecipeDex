# Developer

This README contains instructions for setting up the developer environment, and is organised into three core folders which contain the following:

## Structure

`recipedex`: This is the python module where the heavy-lifting website crawling is implemented using the [Recipe Scraper](https://github.com/hhursev/recipe-scrapers) and [Parse Ingredient](https://github.com/MichielMag/parse-ingredients) modules. There will also be some additional extraction of metadata and other useful features from the web page where available.

`backend`: Another python module that serves as the apps API via [FastAPI](https://fastapi.tiangolo.com/) and data storage via [MongoDB](https://www.mongodb.com/). The service is not planned to store all data scraped from recipes but will save the minimum required for indexing and searching functions to execute rapidly.

`frontend`: This section uses the javascript libraries [Node.js](https://nodejs.org/en/) and [React](https://reactjs.org/) to implement the web facing aspect of the service. The aim is for this service to support both mobile and desktop devices, prioritising user experience in regards to ease of use and response times.

## UML Diagrams

![uml diagram](images/uml%20diagram.png "UML diagram of the Database")

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
vagrant plugin install vagrant-vbguest
vagrant up
```

SSH in and configure git with your email and name:
```
vagrant ssh
git config --global user.email "email@example.com"
git config --global user.name "firstname lastname"
```

(Optional) Get the ssh credentials and store in your ssh config file:

```
exit (if you are in the SSH session)
vagrant ssh-config
~/.ssh/config <- copy and paste creds into here
```

(Optional) Set up VSCode to use remote dev vm for development:

```
Install Remote Explorer from extensions
Add the SSH Target from your ssh config file
```

## Deployment

To deploy the service locally read both __README.md__ files in `frontend` and `backend`.

To deploy the service in production you must setup a free account with mongodb to use their cloud database. Once complete, enter the following information into `backend/.env`

```
db_username: <database username>
db_password: <database password>
```

TODO: May need to update gcp app.yaml with user credentials.

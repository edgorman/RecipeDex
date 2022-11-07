# RecipeDex
A Software as a Service (SAAS) application for storing, indexing and searching recipes from all across the web. Makes use of the [Recipe Scraper Package](https://github.com/hhursev/recipe-scrapers) combined with bespoke NLP. Back-end developed in [FastAPI](https://fastapi.tiangolo.com/) and [MongoDB](https://www.mongodb.com/), front-end developed in [React](https://reactjs.org/). Planned deployment as a service in the cloud coming 2023.

This README contains instructions for setting up the developer environment, for more specific instruction on setting up the backend/frontend/recipedex module see the README's within those folders.

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

SSH in and configure git with your email and name:
```
vagrant ssh
git config --global user.email "email@example.com"
git config --global user.name "firstname lastname"
```

## Usage

See each subfolder for instructions on installation and usage.

## Deployment

TODO

# License

TBD

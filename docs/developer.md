# Developer

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

# Developer

These are the developer instructions for setting up this repo for local and cloud deployments.

## Table of Contents

* [Installation](#installation)
    * [Pre-requisites](#pre-requisites)
    * [Repository](#repository)
* [Deployment](#deployment)
    * [Local](#local)
    * [Cloud](#cloud)
* [Development](#development)
    * [Linting](#linting)
    * [Testing](#testing)

---

## Installation

### Pre-requisites

Please install the following:

1. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Python](https://www.python.org/downloads/)
3. [Node](https://nodejs.org/en/download)
4. [Docker](https://www.docker.com/)
5. [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Repository

Clone the repository:

```bash
git clone https://github.com/edgorman/RecipeDex
cd RecipeDex
```

Update script folder permissions:

```bash
chmod +x -R scripts/.
```

Create a python environment for backend development:

```bash
python -m venv .env
source .env/bin/activate
cd RecipeDex
python -m pip install requirements.txt
cd ..
```

Install the npm packages for frontend development:

```bash
npm install --prefix frontend
```

## Deployment

### Local

To create the docker containers and volumes, run:

```bash
./scripts/create.sh
```

To start the project, run:

```bash
./scripts/start.sh
```

To stop the project, run:

```bash
./scripts/stop.sh
```

To destroy the docker containers and volumes, run:

```bash
./scripts/destroy.sh
```

### Cloud

To deploy the project manually, run:

```bash
./scripts/deploy.sh
```

## Development

### Linting

To run linting on the project, run:

```bash
./scripts/lint.sh
```

### Testing

To run testing on the project, run:

```bash
./scripts/test.sh
```

# RecipeDex - Backend
This is the [FastAPI](https://fastapi.tiangolo.com/) and [MongoDB](https://www.mongodb.com/) backend that performs the API routing and data storage/indexing. 

## Installation

Install the required python packages:

```
python -m pip install recipedex/.
python -m pip install backend/.
```

If you're developing this package a handy line to reinstall is:
```
python -m pip uninstall backend -y; python -m pip install backend/.
```

## Usage

```
usage: backend [-h] [--port PORT] [--reload] [--resetdb] [--log {CRITICAL,ERROR,WARNING,INFO,DEBUG}] [--version]

Host the FastAPI and MongoDB backend for recipedex.

options:
  -h, --help            show this help message and exit
  --port PORT           the port to serve fastapi on
  --reload              reload on change (for dev)
  --resetdb             reset database (for dev)
  --log {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        the log level
  --version             show program's version number and exit
```

Example:

```
python -m backend --port 5000 --reload --resetdb --log DEBUG
```

## Testing

Run the testing scripts in the base directory:

```
python -m autopep8 backend/ --in-place --aggressive --recursive --max-line-length 120
python -m flake8 backend/ --max-line-length=120
python -m pytest -svv backend/tests/
```

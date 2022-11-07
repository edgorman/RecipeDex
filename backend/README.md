# RecipeDex - Backend
This is the FastAPI and MongoDB backend that performs the API routing and data storage/indexing. This README assumes you have set up a GCP account as well as a MongoDB account (either may require a form of payment to deploy this app).

## Installation

Install the required python packages:

```
python -m pip install backend/.
```

If you're developing this package a handy line to reinstall is:
```
python -m pip uninstall backend -y; python -m pip install backend/.
```

If python packages are added, update the setup.py file by using the following:

```
python -m pip freeze
```

## Usage

```
usage: backend [-h] [--port PORT] [--log {critical,error,warning,info,debug,trace}] [--reload] [--version]

Host the FastAPI and MongoDB backend for recipedex.

options:
  -h, --help            show this help message and exit
  --port PORT           the port to serve fastapi on
  --log {critical,error,warning,info,debug,trace}
                        the log level for uvicorn
  --reload              reload on change (for dev)
  --version             show program's version number and exit
```

Example:

```
python -m backend --port 5000 --log info --reload
```

## Testing

Run the testing scripts in the base directory:

```
python -m autopep8 backend/ --in-place --aggressive --recursive --max-line-length 120
python -m flake8 backend/ --max-line-length=120
python -m pytest -svv backend/tests/ --disable-pytest-warnings --cov=backend --cov-config=backend/tests/.coveragerc
```

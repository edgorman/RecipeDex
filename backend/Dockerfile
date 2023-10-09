FROM python:3.10 as backend

WORKDIR /backend
ADD . /backend/

RUN python -m pip install -r requirements.txt

FROM backend as test

CMD ["python", "-m", "pytest", "/backend/tests/", "-svv"]

FROM backend as lint

CMD ["python", "-m", "flake8", "/backend", "--v"]

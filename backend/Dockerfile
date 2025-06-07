FROM python:3.13.4-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . ./

RUN adduser -D appuser
USER appuser

CMD exec uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1

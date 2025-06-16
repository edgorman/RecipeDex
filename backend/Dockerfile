FROM python:3.13.4-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir --upgrade pip

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install -e . \
    && apk del .build-deps

RUN adduser -D appuser
USER appuser

ARG SERVICE_ALLOWED_ORIGIN
ENV SERVICE_ALLOWED_ORIGIN=${SERVICE_ALLOWED_ORIGIN}

CMD ["python", "commands/service.py", "run"]

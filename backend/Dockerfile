FROM python:3.13.4-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.7.13-python3.13-alpine /usr/local/bin/uv /bin/uv
COPY . ./

RUN uv sync

ARG SERVICE_ALLOWED_ORIGIN
ENV SERVICE_ALLOWED_ORIGIN=${SERVICE_ALLOWED_ORIGIN}

CMD ["uv", "run", "commands/service.py", "run"]

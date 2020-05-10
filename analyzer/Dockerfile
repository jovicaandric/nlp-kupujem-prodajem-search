FROM python:3.7-slim

RUN apt-get update && apt-get install build-essential -y

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.5

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /opt/kp

COPY poetry.lock pyproject.toml /opt/kp/

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev --no-interaction --no-ansi

RUN mkdir -p /opt/kp/{models,analyzer}

COPY models/ads.category.100.bin /opt/kp/models/
COPY analyzer /opt/kp/analyzer/

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "analyzer.wsgi:app"]

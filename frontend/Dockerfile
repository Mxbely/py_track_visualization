FROM python:3.12-slim as base

RUN pip install --upgrade pip && \
    pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY frontend/ /app/frontend/

EXPOSE 8050

CMD ["poetry", "run", "python", "frontend/main.py"]

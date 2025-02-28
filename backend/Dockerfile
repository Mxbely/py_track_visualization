FROM python:3.12-slim as base

RUN pip install --upgrade pip && \
    pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY backend/ /app/backend/

EXPOSE 8000

CMD ["poetry", "run", "python", "backend/manage.py", "runserver", "0.0.0.0:8000"]

# Використовуємо офіційний Python образ
FROM python:3.12-slim as base

# Встановлюємо Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл pyproject.toml і poetry.lock для всіх залежностей
COPY pyproject.toml poetry.lock /app/

# Встановлюємо всі залежності
RUN poetry install --no-root

# Копіюємо код Dash
COPY frontend/ /app/frontend/

# Відкриваємо порт для Dash
EXPOSE 8050

# Стартуємо Dash додаток
CMD ["poetry", "run", "python", "frontend/main.py"]

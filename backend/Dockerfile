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

# Копіюємо код Django
COPY backend/ /app/backend/

# Відкриваємо порт для Django
EXPOSE 8000

# CMD [ "poetry", "run", "python", "backend/manage.py", "makemigrations" ]
# Стартуємо сервер для Django
CMD ["poetry", "run", "python", "backend/manage.py", "runserver", "0.0.0.0:8000"]

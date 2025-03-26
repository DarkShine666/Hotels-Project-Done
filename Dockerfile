FROM python:3.12-slim

# Установить Poetry
RUN pip install --no-cache-dir poetry

# Установить рабочую директорию
WORKDIR /app

# Копировать файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Установить зависимости через Poetry без создания виртуального окружения
RUN poetry config virtualenvs.create false && poetry install --no-root

# Копировать весь проект
COPY . /app

# Запустить приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

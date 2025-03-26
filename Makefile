# Установка зависимостей
install:
	poetry install

# Запуск тестов
test:
	poetry run pytest

# Запуск линтера
lint:
	poetry run ruff src/ tests/

# Запуск форматирования кода
format:
	poetry run black src/ tests/

# Запуск приложения локально
run:
	poetry run uvicorn src.main:app --host $(APP_HOST) --port $(APP_PORT)

# Остановить и удалить контейнеры с томами
down:
	docker-compose down -v

# Запустить сервисы db и app в фоновом режиме
up:
	docker-compose up -d db app

#Запустить тестовую бд

test_bd:
	docker-compose up -d test_db

# Очистка томов Docker
clean:
	docker volume prune -f

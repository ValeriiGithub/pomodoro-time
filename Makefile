.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8001
ENV_FILE ?= .local.env
REVISION ?= -1    ## Или идентификатор версии (например, `123456789abc`) base - вернуть базу данных в начальное состояние

## Poetry

run: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn main:app --host $(HOST) --port $(PORT) --reload --env-file $(ENV_FILE)

install:  ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

## Alembic

migrate-create: ## Migrate a dependency using alembic
	@echo "Create migration $(MIGRATION)"
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply: ## Migrate a dependency using alembic
	alembic upgrade head

migrate-downgrade: ## Откат миграции alembic
	alembic downgrade $(REVISION)

## docker

docker-postgres-run: ## Docker a dependency using
	docker-compose up -d	## Запуск postgres в тихом режиме

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands: "
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'



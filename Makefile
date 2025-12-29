# Variables
COMPOSE_FILE=docker-compose.yaml

.PHONY: help up down restart logs ps

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

up: ## Start the environment in detached mode
	docker-compose -f $(COMPOSE_FILE) up -d

down: ## Stop and remove containers, networks, and volumes
	docker-compose -f $(COMPOSE_FILE) down

restart: ## Restart all services
	docker-compose -f $(COMPOSE_FILE) restart

logs: ## Follow logs of all containers
	docker-compose -f $(COMPOSE_FILE) logs -f

ps: ## List running containers
	docker-compose -f $(COMPOSE_FILE) ps
all:
	@echo "1. make setup  # Installe l'environnement"
	@echo "2. make up     # Démarre PostgreSQL et pgAdmin"
	@echo "3. make clean  # Arrête/supprime l'environnement"

setup:
	@echo "make config"
	@echo "python3 -m venv myenv"
	@echo "source myenv/bin/activate"
	@echo "make requirements"

config:
	@./config/setup.sh

requirements:
	@pip install --upgrade pip
	@pip install -r ./config/requirements.txt

up:
	@docker compose -f ./config/docker-compose.yml up -d --build

down:
	@docker compose -f ./config/docker-compose.yml down

remove_containers:
	@docker stop $$(docker ps -qa)
	@docker rm -f $$(docker ps -aq)
	@docker rmi $$(docker images -aq)

remove_myenv:
	@rm -rf myenv
	@rm -rf ./src/__pycache__

remove_config:
	@rm -f ./config/.env
	@rm -f ./config/database.init

clean: remove_config remove_myenv remove_containers

.PHONY: all setup config requirements up down remove_containers remove_myenv remove_config clean

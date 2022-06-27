all: build up

build:
	@mkdir -p ai_cartasur_db
	@docker compose build

shell: up_dettached
	docker compose exec ai_cartasur bash

testshell: up_dettached
	docker compose run ai_cartasur bash

up:
	docker compose up

up_dettached:
	docker compose up -d

psql:
	docker compose exec ai_cartasur_db psql -U admin ai_cartasur_db

clean:
	@echo "To drop the database use 'make drop'"

down:
	docker compose down

db_create:
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/create_clientes.sql
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/create_creditos.sql
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/create_cuotas.sql
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/create_pagos.sql

db_delete:
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/delete_pagos.sql
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/delete_cuotas.sql
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/delete_creditos.sql
	docker compose exec -T ai_cartasur_db psql -U admin ai_cartasur_db < ./sql/delete_clientes.sql

db_load: db_delete db_create
	docker compose run -T ai_cartasur ./scripts/load_clientes.py
	docker compose run -T ai_cartasur ./scripts/load_creditos.py
	docker compose run -T ai_cartasur ./scripts/load_cuotas.py
	docker compose run -T ai_cartasur ./scripts/load_pagos.py

dbshell:
	docker compose exec ai_cartasur_db bash

drop_database:
	rm -rf ai_cartasur_db

macos_docker_up:
	open -a Docker

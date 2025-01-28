default: 
	@echo "Comandos disponíveis"
	@echo "make build           - Cria containers caso não os tenha, ou caso modifique .env.dev"
	@echo "make makemigrations  - Cria migrations"
	@echo "make migrate         - Executa migrations"
	@echo "make createsuperuser - Criar um usuario"
	@echo "make start           - Inicializa container, e executa serviço Django"
	@echo "make stop            - Encerra execução dos containers BD e Django"
	@echo "make test            - Fazer teste com o pytest"
	@echo "make lint            - Organiza o codigo"
	@echo "make black           - Black é um formatador de código Python que segue a PEP 8,"
	@echo "make isort           - Classifica automaticamente as importações em um arquivo de código Python"
	@echo "make flake8          - O Flake8 é um linter de código Python que verifica o estilo e a qualidade do código"
	@echo "make pre             - Pre analise do codigo antes do commit, Isort, Black Flake8 e um teste de coverage"

build:
ifeq ("$(wildcard .env.dev)","") 
	cp .env.dev-example .env.dev
	@echo "#####____________________________________________________________________Novo arquivo .env.dev criado" 
endif
	docker-compose -f docker-compose-dev.yaml --env-file=.env.dev up -d --build
	@echo "#####____________________________________________________________________Configurando banco de dados"
	docker exec -ti db_api_wl_dev psql -U postgres -c "ALTER USER postgres CREATEDB;"
	docker exec -ti db_api_wl_dev psql -U postgres -c "CREATE DATABASE test_postgres;" || echo "Banco de dados de teste já existe."
	docker exec -ti web_api_wl_dev python manage.py makemigrations
	docker exec -ti web_api_wl_dev python manage.py migrate


makemigrations:
	docker exec -ti web_api_wl_dev python manage.py makemigrations

migrate:
	docker exec -ti web_api_wl_dev python manage.py migrate

createsuperuser:
	docker exec -ti web_api_wl_dev python manage.py createsuperuser

collectstatic:
	docker exec -ti web_api_wl_dev python manage.py collectstatic

start:
	docker-compose -f docker-compose-dev.yaml start
	# Espera até que o banco de dados esteja acessível
	docker exec -ti web_api_wl_dev wait-for-it db_api_wl:5435 --timeout=30 -- echo "Banco de dados pronto!"
	docker exec -ti web_api_wl_dev python manage.py runserver 0.0.0.0:8000

stop:
	docker-compose -f docker-compose-dev.yaml stop 

test:
	docker exec -ti web_api_wl_dev pytest . 

coverage:
	docker exec -ti web_api_wl_dev coverage run manage.py test
	docker exec -ti web_api_wl_dev coverage report

lint:
	@echo "\n########## Runs isort, black and flake8. Organizing and linting code. ###########\n"
	@echo "############################### Running isort ###################################\n"
	docker exec -ti web_api_wl_dev isort .
	docker exec -ti -u root web_api_wl_dev chown -R app:app /app 
	@echo "\n################################# Running black #################################\n"
	docker exec -ti web_api_wl_dev black .
	docker exec -ti -u root web_api_wl_dev chown -R app:app /app 
	@echo "\n################################ Running flake8. ################################\n"
	docker exec -ti web_api_wl_dev flake8 .
	docker exec -ti -u root web_api_wl_dev chown -R app:app /app 

pre: 
	make lint
	make test

isort:
	@echo "############################### Running isort ###################################\n"
	docker exec -ti web_api_wl_dev isort .
	docker exec -ti -u root web_api_wl_dev chown -R app:app /app 

black:
	@echo "\n################################# Running black #################################\n"
	docker exec -ti web_api_wl_dev black .
	docker exec -ti -u root web_api_wl_dev chown -R app:app /app 

flake8:
	@echo "\n################################ Running flake8. ################################\n"
	docker exec -ti web_api_wl_dev flake8 .
	docker exec -ti -u root web_api_wl_dev chown -R app:app /app 

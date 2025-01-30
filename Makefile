# Exibe os comandos disponíveis
default: 
	@echo "Comandos disponíveis"
	@echo "make build           - Cria containers caso não os tenha, ou caso modifique .env.dev"
	@echo "make makemigrations  - Cria migrations"
	@echo "make migrate         - Executa migrations"
	@echo "make createsuperuser - Criar um usuário Django"
	@echo "make start           - Inicializa container e executa serviço Django"
	@echo "make stop            - Encerra execução dos containers BD e Django"
	@echo "make test            - Executa testes com pytest"
	@echo "make lint            - Organiza e verifica código"
	@echo "make pre             - Pré-análise do código antes do commit (Isort, Black, Flake8 e testes)"
	@echo "make shell           - Acessa o shell do Django"
	@echo "make coverage        - Executa testes e exibe cobertura de código"
	@echo "make isort           - Organiza imports"
	@echo "make black           - Formata o código com Black"
	@echo "make flake8          - Verifica o código com Flake8"
	@echo "make populate        - Popula o banco de dados com dados de teste"

# Construção do ambiente
build:
ifeq ("$(wildcard .env.dev)","") 
	cp .env.dev-example .env.dev
	@echo "#####____________________________________________________________________Novo arquivo .env.dev criado" 
endif
	docker-compose -f docker-compose-dev.yaml --env-file=.env.dev up -d --build
	@echo "#####____________________________________________________________________Esperando o banco de dados ficar pronto..."
	# Aguarde o banco estar pronto antes de executar comandos
	until docker exec -ti db_api_wl_dev pg_isready -h db_api_wl -p 5432 -U postgres; do sleep 1; done
	@echo "#####____________________________________________________________________Banco de dados pronto!"
	docker exec -ti db_api_wl_dev psql -U postgres -c "ALTER USER postgres CREATEDB;"
	docker exec -ti db_api_wl_dev psql -U postgres -c "CREATE DATABASE test_postgres;" || echo "Banco de dados de teste já existe."
	docker exec -ti web_api_wl_dev python manage.py makemigrations
	docker exec -ti web_api_wl_dev python manage.py migrate
	@echo "#####____________________________________________________________________Configuração finalizada!"

# Comandos Django
makemigrations:
	docker exec -ti web_api_wl_dev python manage.py makemigrations

migrate:
	docker exec -ti web_api_wl_dev python manage.py migrate

createsuperuser:
	docker exec -ti web_api_wl_dev python manage.py createsuperuser

collectstatic:
	docker exec -ti web_api_wl_dev python manage.py collectstatic --noinput

shell:
	docker exec -ti web_api_wl_dev python manage.py shell

# Inicialização e parada dos containers
start:
	docker-compose -f docker-compose-dev.yaml start
	# Aguarda até que o banco de dados esteja acessível
	docker exec -ti web_api_wl_dev wait-for-it db_api_wl:5435 --timeout=30 -- echo "Banco de dados pronto!"
	docker exec -ti web_api_wl_dev python manage.py runserver 0.0.0.0:8000

stop:
	docker-compose -f docker-compose-dev.yaml stop 

# Testes e cobertura de código
test:
	docker exec -ti web_api_wl_dev pytest . 

coverage:
	docker exec -ti web_api_wl_dev coverage run manage.py test
	docker exec -ti web_api_wl_dev coverage report

# Linter e formatação do código
lint:
	@echo "\n########## Organizando e verificando código ###########\n"
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

# Formatação individual
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

populate:
	docker exec -it web_api_wl_dev python manage.py populate_db
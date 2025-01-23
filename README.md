# API Authentication :rocket:

## Descrição do Projeto :book:

API para gestão de carteiras digitais e transações financeiras, permitindo autenticação de usuários, consulta e adição de saldo, transferência entre carteiras e listagem de transações com filtros opcionais por período.

## Tecnologias Utilizadas :computer:

- **Docker**: Para criação de containers e gerenciamento do ambiente de desenvolvimento.
- **Python**: Linguagem principal utilizada no backend.
- **Django**: Framework para desenvolvimento web e criação da API.
- **Django Rest Framework (DRF)**: Extensão do Django que facilita a construção de APIs RESTful, fornecendo ferramentas robustas para serialização, autenticação, permissões e endpoints eficientes.
- **Git**: Controle de versão do código.
- **Makefile**: Para automação de comandos do projeto.
- **Swagger**: Documentação da API.

## Pré-requisitos :warning:

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas: Docker, Docker Compose, Git e uma IDE.

### Checando a instalação do Docker :warning:

`docker-compose --version`

`docker --version`

#### Caso não retorne uma versão é necessário instalar essas dependências, antes de continuar e rodar o projeto

____________________________________________________________________________________________________________________

## Como Rodar o Projeto :arrows_counterclockwise:

### Executando o projeto com o Makefile

As etapas de build, execução, e alguns atalhos foram incorporados num script Makefile. Basta que tenha os pré-requisitos instalados.

**Para executar os comandos, na raiz do projeto em linha de comando:**

- **Cria containers e o arquivo .env.dev:**
    `make setup`

- **Cria migrations:**
    `make makemigrations`

- **Executa migrations:**
    `make migrate`

- **Inicializa container, e executa serviço Django:**
    `make start`

- **Encerra execução dos containers BD e Django:**
    `make stop`

- **Executa todos os linters e flake8:**
    `make lint`

- **Executa apenas um teste de coverage e pytest:**
    `make test`

- **Pre commit. Executa os linters e executa um teste de coverage e pytest:**
    `make pre`

____________________________________________________________________________________________________________________

## Breve comentário sobre as variáveis de ambiente :computer:

Geralmente utilizamos o arquivo .env em produção e o arquivo .env.dev para ambiente de desenvolvimento local, isso para isolar senhas e constantes utilizadas em desenvolvimento e em produção.

Uma das variáveis utilizadas neste projeto é a SECRET_KEY do Django. Por padrão ela vem criada automaticamente no arquivo settings.py. A chave secreta (secret key) do Django é uma parte fundamental da segurança da sua aplicação. Para se acostumar com boas práticas redefina a SECRET_KEY por algo mais seguro, editando o arquivo .env.dev do passo anterior. Em desenvolvimento esse passo pode ser descartado, mas é bom se familiarizar com esse conceito.

[Link para Post explicando como criar uma SECRET_KEY segura](https://ohmycode.com.br/como-gerar-uma-secret_key-do-django/)

Também é uma boa prática utilizar uma boa senha para o Postgres, que está na variável DB_PASSWD do arquivo .env.dev example.

____________________________________________________________________________________________________________________

## Build do container :construction:

O build é o processo de criar os contêiners Docker conforme definido no arquivo docker-compose.yaml. É preciso fazê-lo somente na primeira execução do projeto, quando modificamos alguma variável de ambiente ou para recriar os contêiners.

Nesse projeto você não precisa instalar Postgres em seu computador, nem mesmo ter um ambiente virtual local. Tudo estará "conteinerizado" e com um grau de isolamento do seu computador host. Uma das principais vantagens de ter contêineres é evitar o "mas funciona aqui no meu computador", permitindo que desenvolvedores de diferentes times e até em produção tenhamos um ambiente homogêneo.

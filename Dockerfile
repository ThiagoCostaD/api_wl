# Use uma imagem oficial de Python como base
FROM python:3.11.11-alpine3.21

# Define o diretório de trabalho
WORKDIR /app

# Cria um grupo e usuário para a aplicação
RUN addgroup -S app && adduser -S app -G app

# Define as variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala as dependências do PostgreSQL e GCC
RUN apk update \
  && apk add --no-cache postgresql-dev gcc musl-dev

# Atualiza o pip
RUN pip install --upgrade pip

# Copia o arquivo de requerimentos e instala as dependências
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copia o projeto
COPY . /app

# Altera o usuário para o usuário não-root
USER app
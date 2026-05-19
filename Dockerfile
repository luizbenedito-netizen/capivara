# Base image
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências
RUN apt-get update && apt-get install -y \
    nginx \
    curl \
    sudo \
    gnupg \
    build-essential \
    gcc \
    libcairo2-dev \
    pkg-config \
    libffi-dev \
    libdbus-1-dev \
    libglib2.0-dev \
    libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala cloudflared
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb \
    && dpkg -i cloudflared.deb \
    && rm cloudflared.deb

# Cria diretório da aplicação
RUN mkdir /app
WORKDIR /app

# Atualiza pip e ferramentas
RUN pip install --upgrade pip setuptools wheel

# Instala requirements se existir
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia entrypoint
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

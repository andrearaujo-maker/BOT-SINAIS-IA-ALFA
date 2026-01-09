# Dockerfile para Bots Python do Telegram
FROM python:3.11-slim

# Configura timezone para São Paulo
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    tzdata \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivo de dependências primeiro (otimização de cache)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o resto do código (incluindo .env se existir)
COPY . .

# Cria arquivo .env vazio se não foi copiado (evita erro do Dokploy)
RUN if [ ! -f /app/.env ]; then \
        echo "# Arquivo .env vazio - configurações estão no main.py" > /app/.env && \
        echo "# Este arquivo existe apenas para evitar erro do Dokploy" >> /app/.env; \
    fi

# Cria diretório para logs (se necessário)
RUN mkdir -p /app/logs

# Expõe porta (se necessário para webhooks)
EXPOSE 8000

# Comando para iniciar o bot
CMD ["python", "main.py"]

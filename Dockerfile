FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema e timezone
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY main.py .

# Variáveis de ambiente (serão sobrescritas pelo Dokploy)
ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHAT_ID=""
ENV TZ=America/Sao_Paulo

# Comando para executar o bot
CMD ["python", "main.py"]

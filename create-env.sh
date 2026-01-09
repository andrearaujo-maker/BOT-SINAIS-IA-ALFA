#!/bin/bash
# Script para criar .env vazio (necessário para Dokploy)
# Este arquivo é executado automaticamente ou pode ser executado manualmente

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "# Arquivo .env vazio - configurações estão no main.py" > "$ENV_FILE"
    echo "# Este arquivo existe apenas para evitar erro do Dokploy" >> "$ENV_FILE"
    chmod 644 "$ENV_FILE"
    echo "✅ Arquivo .env criado"
else
    echo "✅ Arquivo .env já existe"
fi


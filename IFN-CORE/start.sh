#!/usr/bin/env bash

# 1. Ejecuta todas las migraciones para crear las tablas en Supabase
echo "Ejecutando Alembic upgrade head..."
alembic upgrade head

# 2. Inicia el servidor FastAPI. 
# Si tu app está en src/main.py y el objeto principal es 'app', 
# el comando es src.main:app
echo "Iniciando Uvicorn..."
uvicorn src.main:app --host 0.0.0.0 --port $PORT
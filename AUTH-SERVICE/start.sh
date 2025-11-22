#!/usr/bin/env bash

# Inicia el servidor FastAPI de autenticación
# AJUSTAR la ruta si el archivo no es main.py o si está dentro de una carpeta 'src'
echo "Iniciando Uvicorn para AUTH-SERVICE..."
uvicorn src.main:app --host 0.0.0.0 --port $PORT

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Infrastructure.Api.autenticacion_router import router as auth_router
from src.Infrastructure.Core.firebase_config import inicializar_firebase



app = FastAPI(title="AUTH-SERVICE")

# --- Configuración CORS ---
app.add_middleware(
	CORSMiddleware,
	allow_origins=["https://ifnfrontend-fgfxukz0p-brayan-lizcanos-projects.vercel.app"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Inicialización opcional de servicios core (mock en esta versión)
inicializar_firebase()

# Routers
app.include_router(auth_router)

# Endpoint raíz para verificación
@app.get("/")
def read_root():
	return {"message": "AUTH-SERVICE is running"}

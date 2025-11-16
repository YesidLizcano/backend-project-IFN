from fastapi import FastAPI
from src.Infrastructure.Api.autenticacion_router import router as auth_router
from src.Infrastructure.Core.firebase_config import inicializar_firebase

app = FastAPI(title="AUTH-SERVICE")

# Inicialización opcional de servicios core (mock en esta versión)
inicializar_firebase()

# Routers
app.include_router(auth_router)

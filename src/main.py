from fastapi import FastAPI
from sqlmodel import Session

from src.Shared.Infrastructure.Api import departamento_router, municipio_router
from src.Modules.Conglomerados.Infrastructure.Api import conglomerado_router
from src.Shared.Infrastructure.Persistence.database import create_all_tables
    
app = FastAPI(lifespan=create_all_tables)
app.include_router(conglomerado_router.router)
app.include_router(departamento_router.router)
app.include_router(municipio_router.router)



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.Modules.Brigadas.Infrastructure.Api import brigada_router, integrante_router, integranteBrigada_router
from src.Modules.Ubicacion.Infrastructure.Api import departamento_router, municipio_router
from src.Modules.Conglomerados.Infrastructure.Api import conglomerado_router
from src.Modules.MaterialEquipo.Infrastructure.Api import controlEquipo_router, materialEquipo_router
from src.Shared.database import create_all_tables
    
app = FastAPI(lifespan=create_all_tables)

# --- Configuración CORS ---
app.add_middleware(
	CORSMiddleware,
	allow_origins=["https://ifnfrontend.vercel.app/"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.include_router(conglomerado_router.router)
app.include_router(departamento_router.router)
app.include_router(municipio_router.router)
app.include_router(integrante_router.router)
app.include_router(brigada_router.router)
app.include_router(integranteBrigada_router.router)
app.include_router(materialEquipo_router.router)
app.include_router(controlEquipo_router.router)

# Endpoint raíz para verificación
@app.get("/")
def read_root():
	return {"message": "IFN-CORE is running"}


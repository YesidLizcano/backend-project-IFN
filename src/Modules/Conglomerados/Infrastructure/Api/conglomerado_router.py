from fastapi import APIRouter, HTTPException, status

from fastapi import Depends

from src.Modules.Conglomerados.Domain.conglomerado import Conglomerado, ConglomeradoCrear, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository
from src.Modules.Conglomerados.Application.conglomerado_crear import CrearConglomerado
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.DBMunicipioRepository import (
    get_municipio_repository,
)

router = APIRouter(tags=["conglomerados"])


@router.post(
    "/conglomerados/{municipio_id}",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_conglomerado(
    municipio_id: int,
    conglomerado_data: ConglomeradoCrear,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository)
):
    try:
        creator = CrearConglomerado(conglomerado_repo, municipio_repo)
        saved_conglomerado = creator.execute(conglomerado_data, municipio_id)
        return saved_conglomerado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

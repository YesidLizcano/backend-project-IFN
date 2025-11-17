from fastapi import APIRouter, Depends, status, HTTPException

from src.Modules.Brigadas.Application.brigada_crear import CrearBrigada
from src.Modules.Brigadas.Application.brigada_eliminar import EliminarBrigada
from src.Modules.Brigadas.Domain.brigada import BrigadaCrear, BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository


router = APIRouter(tags=["brigadas"])


@router.post(
    "/brigadas/{conglomerado_id}",
    response_model=BrigadaSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_brigada(
    conglomerado_id: int,
    brigada_data: BrigadaCrear,
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository)
):
    try:
        creator = CrearBrigada(brigada_repo, conglomerado_repo)
        saved_brigada = creator.execute(brigada_data, conglomerado_id)
        return saved_brigada
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/brigadas/{brigada_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def eliminar_brigada(
    brigada_id: int,
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
):
    """Elimina una brigada existente por su identificador."""
    try:
        eliminador = EliminarBrigada(
            brigada_repository=brigada_repo,
            conglomerado_repository=conglomerado_repo,
        )
        eliminador.execute(brigada_id)
    except ValueError as e:
        msg = str(e)
        status_code = (
            status.HTTP_409_CONFLICT
            if "ya inició" in msg.lower()
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=msg)
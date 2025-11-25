from sqlmodel import Session

from src.Modules.Brigadas.Domain.brigada import AsignacionIntegrante, Brigada, BrigadaCrear, BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository


class CrearBrigada:
    def __init__(
        self,
        brigada_repository: BrigadaRepository,
        conglomerado_repository: ConglomeradoRepository,
        integrante_repository: IntegranteRepository,
        integrante_brigada_repository: IntegranteBrigadaRepository,
        session: Session,
    ):
        self.brigada_repository = brigada_repository
        self.conglomerado_repository = conglomerado_repository
        self.integrante_repository = integrante_repository
        self.integrante_brigada_repository = integrante_brigada_repository
        self.session = session



    def execute(self, brigada: BrigadaCrear, conglomerado_id: int) -> BrigadaSalida:
        transaction = self.session.begin()
        try:
            conglomerado = self.conglomerado_repository.buscar_por_id(conglomerado_id)
            if not conglomerado:
                raise ValueError("Conglomerado no encontrado")

            if self.brigada_repository.buscar_por_conglomerado_id(conglomerado_id):
                raise ValueError(f"El conglomerado {conglomerado_id} ya tiene una brigada asignada")

            self._validar_asignaciones(brigada.integrantes_asignados)

            self.conglomerado_repository.actualizar_fechas(
                conglomerado_id=conglomerado_id,
                fecha_inicio=brigada.fechaInicio,
                fecha_fin_aprox=brigada.fechaFinAprox,
                commit=False,
            )

            brigada_data = brigada.model_dump(
                exclude={"integrantes_asignados", "fechaInicio", "fechaFinAprox"}
            )
            brigada_entidad = Brigada(
                **brigada_data,
                conglomerado_id=conglomerado_id,
            )

            brigada_creada = self.brigada_repository.guardar(brigada_entidad, commit=False)

            for asignacion in brigada.integrantes_asignados:
                self._validar_integrante(asignacion.integrante_id)
                relacion = IntegranteBrigada(
                    id_brigada=brigada_creada.id,
                    id_integrante=asignacion.integrante_id,
                    rol=asignacion.rol_asignado,
                )
                self.integrante_brigada_repository.guardar(relacion, commit=False)

            transaction.commit()
        except Exception:
            self.session.rollback()
            raise

        brigada_resultado = (
            self.brigada_repository.buscar_por_id(brigada_creada.id) or brigada_creada
        )
        integrantes = self.integrante_repository.listar_por_brigada(brigada_creada.id)
        return brigada_resultado.model_copy(update={"integrantes": integrantes})

    def _validar_asignaciones(self, asignaciones: list[AsignacionIntegrante]) -> None:
        integrantes_registrados: set[int] = set()
        for asignacion in asignaciones:
            if asignacion.integrante_id in integrantes_registrados:
                raise ValueError(
                    f"Integrante con ID {asignacion.integrante_id} duplicado en la solicitud"
                )
            integrantes_registrados.add(asignacion.integrante_id)

    def _validar_integrante(self, integrante_id: int) -> None:
        if not self.integrante_repository.buscar_por_id(integrante_id):
            raise ValueError(f"Integrante con ID {integrante_id} no encontrado")
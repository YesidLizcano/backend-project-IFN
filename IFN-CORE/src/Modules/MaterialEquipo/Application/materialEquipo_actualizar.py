from src.Modules.MaterialEquipo.Domain.materialEquipo import (
    MaterialEquipoActualizar,
    MaterialEquipoSalida,
)
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Shared.Domain.departamento_repository import DepartamentoRepository


class ActualizarMaterialEquipo:
    """Caso de uso para actualización parcial de MaterialEquipo."""

    def __init__(
        self,
        material_equipo_repository: MaterialEquipoRepository,
        departamento_repository: DepartamentoRepository,
    ) -> None:
        self.material_equipo_repository = material_equipo_repository
        self.departamento_repository = departamento_repository

    def execute(
        self, material_equipo_id: int, cambios: MaterialEquipoActualizar
    ) -> MaterialEquipoSalida:
        # Validar que el material exista (repositorio lanzará si no existe, pero lo usamos para 404 temprana o side-effects)
        actual = self.material_equipo_repository.buscar_por_id(material_equipo_id)
        if actual is None:
            raise ValueError("Material no encontrado")

        # Validar departamento si viene en el payload
        if cambios.departamento_id is not None:
            depto = self.departamento_repository.buscar_por_id(cambios.departamento_id)
            if depto is None:
                raise ValueError("Departamento no encontrado")

        # Delegar actualización parcial al repositorio
        return self.material_equipo_repository.actualizar(material_equipo_id, cambios)

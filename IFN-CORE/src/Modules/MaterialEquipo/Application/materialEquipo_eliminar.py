from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository


class EliminarMaterialEquipo:
    """Caso de uso para eliminar un Material/Equipo.

    Reglas:
    - Debe existir el material a eliminar.
    - No se permite eliminar si hay unidades asignadas desde hoy en adelante.
    """

    def __init__(
        self,
        material_equipo_repository: MaterialEquipoRepository,
        control_equipo_repository: ControlEquipoRepository,
    ) -> None:
        self.material_equipo_repository = material_equipo_repository
        self.control_equipo_repository = control_equipo_repository

    def execute(self, material_equipo_id: int) -> None:
        """Ejecuta la eliminación validando asignaciones activas.

        Levanta ValueError si no existe el material o si hay asignaciones activas.
        """
        existente = self.material_equipo_repository.buscar_por_id(material_equipo_id)
        if existente is None:
            raise ValueError("Material/Equipo no encontrado")

        asignado = self.control_equipo_repository.contar_asignado_desde_hoy(
            material_equipo_id
        )
        if asignado > 0:
            raise ValueError(
                "No se puede eliminar: existen unidades asignadas actualmente"
            )

        self.material_equipo_repository.eliminar(material_equipo_id)

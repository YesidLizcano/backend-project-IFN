from src.Modules.MaterialEquipo.Domain.materialEquipo import (
    MaterialEquipoActualizar,
    MaterialEquipoSalida,
)
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository


class ActualizarMaterialEquipo:
    """Caso de uso para actualización parcial de MaterialEquipo."""

    def __init__(
        self,
        material_equipo_repository: MaterialEquipoRepository,
        departamento_repository: DepartamentoRepository,
        control_equipo_repository: ControlEquipoRepository,
    ) -> None:
        self.material_equipo_repository = material_equipo_repository
        self.departamento_repository = departamento_repository
        self.control_equipo_repository = control_equipo_repository

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

        # Si se actualiza la cantidad, aquí la interpretamos como delta (positivo suma, negativo resta).
        # Validamos que la cantidad resultante no sea negativa y que no quede por debajo
        # de las unidades ya asignadas desde hoy.
        if cambios.cantidad is not None:
            try:
                delta = int(cambios.cantidad)
            except Exception:
                raise ValueError("El campo 'cantidad' debe ser un número entero")

            nueva_cantidad = actual.cantidad + delta
            if nueva_cantidad < 0:
                raise ValueError("La cantidad resultante no puede ser negativa")

            asignado_hoy = self.control_equipo_repository.contar_asignado_desde_hoy(
                material_equipo_id
            )
            if nueva_cantidad < asignado_hoy:
                raise ValueError(
                    f"No se puede reducir la cantidad por debajo de las unidades asignadas actualmente (asignadas: {asignado_hoy})."
                )

        # Delegar actualización parcial al repositorio
        return self.material_equipo_repository.actualizar(material_equipo_id, cambios)

from src.Modules.MaterialEquipo.Domain.materialEquipo import MaterialEquipo, MaterialEquipoCrear, MaterialEquipoSalida
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository


class CrearMaterialEquipo:
    def __init__(
        self,
        material_equipo_repository: MaterialEquipoRepository,
        departamento_repository: DepartamentoRepository,
    ):
        self.material_equipo_repository = material_equipo_repository
        self.departamento_repository = departamento_repository

    def execute(self, material_equipo: MaterialEquipoCrear, departamento_id: int) -> MaterialEquipoSalida:
        if not self.departamento_repository.buscar_por_id(departamento_id):
            raise ValueError("Departamento no encontrado")

        if self.material_equipo_repository.buscar_por_nombre_y_departamento(
            material_equipo.nombre, departamento_id
        ):
            raise ValueError(f"El material '{material_equipo.nombre}' ya existe en este departamento")

        material_equipo_salida = MaterialEquipo(
            **material_equipo.model_dump(),  # Datos del body
            departamento_id=departamento_id # Asigna el ID de la URL
        )

        return self.material_equipo_repository.guardar(material_equipo_salida)
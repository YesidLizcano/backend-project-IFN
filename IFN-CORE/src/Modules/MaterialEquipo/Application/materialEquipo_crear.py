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
        # Nota: buscar_por_nombre_y_departamento fue reemplazado por buscar_por_nombre_y_nombre_departamento
        # en la interfaz, pero aquí seguimos usando departamento_id.
        # Para mantener consistencia sin romper este caso de uso (que usa ID),
        # deberíamos tener ambos métodos o resolver el nombre del departamento aquí.
        # Por ahora, asumimos que el repositorio mantiene compatibilidad o ajustamos la llamada.
        
        # Ajuste temporal: obtener nombre del departamento para validar duplicado
        depto = self.departamento_repository.buscar_por_id(departamento_id)
        if not depto:
             raise ValueError("Departamento no encontrado")

        if self.material_equipo_repository.buscar_por_nombre_y_nombre_departamento(
            material_equipo.nombre, depto.nombre
        ):
            raise ValueError(f"El material '{material_equipo.nombre}' ya existe en este departamento")

        material_equipo_salida = MaterialEquipo(
            **material_equipo.model_dump(),  # Datos del body
            departamento_id=departamento_id # Asigna el ID de la URL
        )

        return self.material_equipo_repository.guardar(material_equipo_salida)
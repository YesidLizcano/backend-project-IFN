from src.Modules.MaterialEquipo.Domain.controlEquipo import ControlEquipo, ControlEquipoCrear, ControlEquipoGuardar
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository


class CrearControlEquipo:
    def __init__(
        self,
        control_equipo_repository: ControlEquipoRepository,
        brigada_repository: BrigadaRepository,
        material_equipo_repository: MaterialEquipoRepository,
        conglomerado_repository: ConglomeradoRepository,
    ):
        self.control_equipo_repository = control_equipo_repository
        self.brigada_repository = brigada_repository
        self.material_equipo_repository = material_equipo_repository
        self.conglomerado_repository = conglomerado_repository

    def execute(self, controlEquipo: ControlEquipoCrear, brigada_id: int, material_equipo_id: int) -> ControlEquipo:
        # Validar que la cantidad asignada sea mayor a 0
        if controlEquipo.cantidad_asignada <= 0:
            raise ValueError("La cantidad asignada debe ser mayor a 0")
        
        # Validar que la brigada existe
        brigada = self.brigada_repository.buscar_por_id(brigada_id)
        if not brigada:
            raise ValueError("Brigada no encontrada")
        
        # Obtener fechas del conglomerado para validar disponibilidad
        conglomerado = self.conglomerado_repository.buscar_por_id(brigada.conglomerado_id)
        if not conglomerado:
            raise ValueError("Conglomerado asociado a la brigada no encontrado")
        
        if not conglomerado.fechaInicio:
             raise ValueError("El conglomerado no tiene fecha de inicio definida")

        # Validar que el material/equipo existe
        material_equipo = self.material_equipo_repository.buscar_por_id(material_equipo_id)
        if not material_equipo:
            raise ValueError("Material/Equipo no encontrado")
        
        # Calcular disponibilidad en la fecha de inicio del conglomerado
        disponibilidad = self.control_equipo_repository.calcular_disponibilidad(
            nombre_equipo=material_equipo.nombre,
            brigada_id=brigada_id,
            fecha_inicio=str(conglomerado.fechaInicio)
        )
        
        # Validar que hay suficiente disponibilidad
        if disponibilidad < controlEquipo.cantidad_asignada:
            raise ValueError(
                f"No hay suficiente disponibilidad. Disponible: {disponibilidad}, Solicitado: {controlEquipo.cantidad_asignada}"
            )

        # Crear el DTO con los IDs agregados
        control_equipo_guardar = ControlEquipoGuardar(
            **controlEquipo.model_dump(),
            id_brigada=brigada_id,
            id_material_equipo=material_equipo_id
        )

        return self.control_equipo_repository.guardar(control_equipo_guardar)

from datetime import date
from typing import List, Tuple, Dict

from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.MaterialEquipo.Domain.controlEquipo import ControlEquipoGuardar, ControlEquipo


DEFAULT_ITEMS: List[Tuple[str, int]] = [
    ("Baterías GPS", 2),
    ("Baterías hipsómetro", 2),
    ("Baterías pie de rey", 2),
    ("Botiquín de primeros auxilios", 1),
    ("Brújula", 1),
    ("Cámara digital", 1),
    ("Cinta diamétrica", 1),
    ("Cinta métrica de 30 m", 2),
    ("Clinómetro", 1),
    ("Flexómetro", 1),
    ("GPS", 1),
    ("Juego de formatos", 1),
    ("Lápices", 4),
    ("Lima afilar", 1),
    ("Machete", 1),
    ("Pie de rey manual", 1),
    ("Plástico de 4 m por 5 m", 1),
    ("Pintura asfáltica de trafico amarilla", 1),
    ("Plomada", 1),
    ("Placas para marcar árboles de referencia en subparcelas", 15),
    ("Rollo de cinta reflectiva", 1),
    ("Rollo de 750 m de cuerda de polipropileno amarilla", 1),
    ("Cuadros de pendientes", 2),
    ("Cuadros para formatos", 2),
    ("Varillas de hierro de 50 cm de ¼ de pulgada", 10),
]


class AsignarMaterialesPorDefectoABrigada:
    """Asigna un set por defecto de materiales/equipos a una brigada.

    Usa las fechas del conglomerado asociado (fechaInicio, fechaFinAprox).
    Busca los materiales por nombre dentro del departamento del municipio del
    conglomerado. Omite los que no existan y devuelve un resumen.
    """

    def __init__(
        self,
        control_equipo_repo: ControlEquipoRepository,
        material_equipo_repo: MaterialEquipoRepository,
        brigada_repo: BrigadaRepository,
        conglomerado_repo: ConglomeradoRepository,
        municipio_repo: MunicipioRepository,
    ) -> None:
        self.control_equipo_repo = control_equipo_repo
        self.material_equipo_repo = material_equipo_repo
        self.brigada_repo = brigada_repo
        self.conglomerado_repo = conglomerado_repo
        self.municipio_repo = municipio_repo

    def execute(self, brigada_id: int) -> Dict:
        brigada = self.brigada_repo.buscar_por_id(brigada_id)
        if brigada is None:
            raise ValueError("Brigada no encontrada")

        conglomerado = self.conglomerado_repo.buscar_por_id(brigada.conglomerado_id)
        if conglomerado is None:
            raise ValueError("Conglomerado asociado no encontrado")

        if not conglomerado.fechaInicio or not conglomerado.fechaFinAprox:
            raise ValueError("El conglomerado no tiene fechas definidas")

        municipio = self.municipio_repo.buscar_por_id(conglomerado.municipio_id)
        if municipio is None:
            raise ValueError("Municipio asociado no encontrado")

        depto_id = municipio.departamento_id

        creados: List[ControlEquipo] = []
        no_encontrados: List[str] = []
        sin_disponibilidad: List[str] = []
        asignaciones_parciales: List[Dict] = []

        # Primera pasada: validar TODOS los ítems (existencia y disponibilidad)
        candidatos: List[Dict] = []
        for nombre, cantidad in DEFAULT_ITEMS:
            material = self.material_equipo_repo.buscar_por_nombre_y_departamento(
                nombre=nombre, departamento_id=depto_id
            )
            if material is None:
                no_encontrados.append(nombre)
                continue

            disponible = self.control_equipo_repo.calcular_disponibilidad(
                nombre_equipo=nombre,
                brigada_id=brigada_id,
                fecha_inicio=conglomerado.fechaInicio,
            )
            if disponible <= 0:
                sin_disponibilidad.append(nombre)
                continue

            candidatos.append(
                {
                    "material": material,
                    "nombre": nombre,
                    "solicitado": cantidad,
                    "disponible": disponible,
                }
            )

        # Si hay problemas, no crear nada y reportar
        if no_encontrados or sin_disponibilidad:
            raise ValueError(
                "No se puede asignar por defecto: materiales no encontrados: "
                f"{no_encontrados} / sin disponibilidad: {sin_disponibilidad}"
            )

        # Segunda pasada: crear asignaciones (permitiendo parcial si corresponde)
        for item in candidatos:
            material = item["material"]
            nombre = item["nombre"]
            cantidad = item["solicitado"]
            disponible = item["disponible"]

            asignar = cantidad if disponible >= cantidad else disponible

            ce = ControlEquipoGuardar(
                id_brigada=brigada_id,
                id_material_equipo=material.id,
                cantidad_asignada=asignar,
                fecha_Inicio_Asignacion=conglomerado.fechaInicio,
                fecha_Fin_Asignacion=conglomerado.fechaFinAprox,
            )
            creado = self.control_equipo_repo.guardar(ce)
            creados.append(creado)

            if asignar < cantidad:
                asignaciones_parciales.append(
                    {
                        "nombre": nombre,
                        "solicitado": cantidad,
                        "asignado": asignar,
                        "faltante": cantidad - asignar,
                    }
                )

        return {
            "brigada_id": brigada_id,
            "asignaciones_creadas": len(creados),
            "materiales_no_encontrados": no_encontrados,
            "sin_disponibilidad": sin_disponibilidad,
            "asignaciones_parciales": asignaciones_parciales,
            "detalle": [
                {
                    "control_equipo_id": c.id,
                    "material_equipo_id": c.id_material_equipo,
                    "cantidad": c.cantidad_asignada,
                }
                for c in creados
            ],
        }

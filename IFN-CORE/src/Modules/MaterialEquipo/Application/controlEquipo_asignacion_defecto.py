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
    """Simula la asignación por defecto de materiales/equipos.

    Usa fechas y departamento provistos para calcular disponibilidad.
    Busca los materiales por nombre dentro del departamento.
    """

    def __init__(
        self,
        control_equipo_repo: ControlEquipoRepository,
        material_equipo_repo: MaterialEquipoRepository,
    ) -> None:
        self.control_equipo_repo = control_equipo_repo
        self.material_equipo_repo = material_equipo_repo

    def execute(self, nombre_departamento: str, fecha_inicio: date, fecha_fin_aprox: date) -> Dict:
        no_encontrados: List[str] = []
        sin_disponibilidad: List[str] = []

        # Primera pasada: validar TODOS los ítems (existencia y disponibilidad)
        candidatos: List[Dict] = []
        for nombre, cantidad in DEFAULT_ITEMS:
            material = self.material_equipo_repo.buscar_por_nombre_y_nombre_departamento(
                nombre=nombre, nombre_departamento=nombre_departamento
            )
            if material is None:
                no_encontrados.append(nombre)
                continue

            disponible = self.control_equipo_repo.calcular_disponibilidad_por_nombre_departamento(
                nombre_equipo=nombre,
                nombre_departamento=nombre_departamento,
                fecha_inicio=fecha_inicio,
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

        # Segunda pasada: clasificar en completa e incompleta
        asignacion_completa = []
        asignacion_incompleta = []

        for item in candidatos:
            material = item["material"]
            nombre = item["nombre"]
            cantidad = item["solicitado"]
            disponible = item["disponible"]

            detalle_item = {
                "material_equipo_id": material.id,
                "nombre": nombre,
                "cantidad_solicitada": cantidad,
                "cantidad_disponible": disponible,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin_aprox,
            }

            if disponible < cantidad:
                detalle_item["faltante"] = cantidad - disponible
                asignacion_incompleta.append(detalle_item)
            else:
                asignacion_completa.append(detalle_item)

        # Tercera parte: Buscar materiales NO obligatorios (extras)
        otros_materiales = []
        todos_los_materiales = self.material_equipo_repo.listar_materiales_equipo(nombre_departamento)
        nombres_obligatorios = {item[0] for item in DEFAULT_ITEMS}

        for material in todos_los_materiales:
            if material.nombre not in nombres_obligatorios:
                disponible = self.control_equipo_repo.calcular_disponibilidad_por_nombre_departamento(
                    nombre_equipo=material.nombre,
                    nombre_departamento=nombre_departamento,
                    fecha_inicio=fecha_inicio,
                )
                otros_materiales.append({
                    "material_equipo_id": material.id,
                    "nombre": material.nombre,
                    "cantidad_total": material.cantidad,
                    "cantidad_disponible": disponible,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin_aprox,
                })

        return {
            "nombre_departamento": nombre_departamento,
            "asignacion_completa": asignacion_completa,
            "asignacion_incompleta": asignacion_incompleta,
            "otros_materiales": otros_materiales,
            "materiales_no_encontrados": no_encontrados,
            "sin_disponibilidad": sin_disponibilidad,
        }

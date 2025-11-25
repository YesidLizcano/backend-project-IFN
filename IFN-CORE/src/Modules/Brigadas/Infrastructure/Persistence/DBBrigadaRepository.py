import unicodedata

from fastapi import Depends
from sqlmodel import Session, select, delete
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from src.Modules.Brigadas.Domain.brigada import Brigada, BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB
from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB
from src.Shared.database import get_session


class DBBrigadaRepository(BrigadaRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, brigada: Brigada, *, commit: bool = True) -> BrigadaSalida:
        db_brigada = BrigadaDB(**brigada.model_dump())
        self.db.add(db_brigada)
        self.db.flush()
        if commit:
            self.db.commit()
        self.db.refresh(db_brigada)
        return BrigadaSalida.model_validate(db_brigada)
    
    def buscar_por_id(self, brigada_id: int) -> BrigadaSalida | None:
        db_brigada = self.db.get(BrigadaDB, brigada_id)
        return BrigadaSalida.model_validate(db_brigada) if db_brigada else None

    def buscar_por_conglomerado_id(self, conglomerado_id: int) -> BrigadaSalida | None:
        db_brigada = self.db.exec(
            select(BrigadaDB).where(BrigadaDB.conglomerado_id == conglomerado_id)
        ).first()
        return BrigadaSalida.model_validate(db_brigada) if db_brigada else None

    def verificar_minimos(self, brigada_id: int) -> dict:
        """Valida que la brigada tenga los roles mínimos requeridos."""
        requeridos = {
            "jefeBrigada": 1,
            "botanico": 1,
            "auxiliar": 1,
            "coinvestigador": 2,
        }

        conteos = {rol: 0 for rol in requeridos}

        stmt = (
            select(IntegranteBrigadaDB.rol, func.count())
            .where(IntegranteBrigadaDB.id_brigada == brigada_id)
            .group_by(IntegranteBrigadaDB.rol)
        )

        for rol, cantidad in self.db.exec(stmt).all():
            if rol in conteos:
                conteos[rol] = cantidad

        detalle = {
            rol: conteos[rol] >= minimo for rol, minimo in requeridos.items()
        }

        return {
            "brigada_id": brigada_id,
            "conteos": conteos,
            "requeridos": requeridos,
            "detalle": detalle,
            "cumple": all(detalle.values()),
        }

    def eliminar(self, brigada_id: int) -> None:
        """Elimina la brigada y limpia las dependencias relacionadas."""
        try:
            self.db.exec(
                delete(IntegranteBrigadaDB).where(
                    IntegranteBrigadaDB.id_brigada == brigada_id
                )
            )
            self.db.exec(
                delete(ControlEquipoDB).where(ControlEquipoDB.id_brigada == brigada_id)
            )
            self.db.exec(
                delete(BrigadaDB).where(BrigadaDB.id == brigada_id)
            )

            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def listar_brigadas(self) -> list[BrigadaSalida]:
        """Lista todas las brigadas con un resumen de sus integrantes.

        Returns:
            list[BrigadaSalida]: Colección de brigadas con resumen de integrantes.
        """
        stmt = select(BrigadaDB).options(
            selectinload(BrigadaDB.integrantes).selectinload(IntegranteBrigadaDB.integrante)
        )
        brigadas_db = self.db.exec(stmt).all()

        brigadas_salida = []
        for b_db in brigadas_db:
            # Crear el DTO de salida a partir de los datos de la BD
            # Usamos model_dump() para evitar conflicto de tipos en 'integrantes'
            # y añadimos 'integrantes' vacío para pasar la validación inicial
            data = b_db.model_dump()
            data["integrantes"] = []
            b_salida = BrigadaSalida.model_validate(data)

            total_integrantes = len(b_db.integrantes)

            # Contar roles clave para el resumen
            roles_destacados = {
                "jefeBrigada": ("Jefe", "Jefes"),
                "botanico": ("Botánico", "Botánicos"),
                "auxiliar": ("Auxiliar", "Auxiliares"),
                "coinvestigador": ("Coinvestigador", "Coinvestigadores"),
            }
            roles_counts: dict[str, int] = {rol: 0 for rol in roles_destacados}

            def _normalizar_rol(raw: str | None) -> str:
                if not raw:
                    return ""
                normalizado = unicodedata.normalize("NFKD", raw)
                ascii_only = normalizado.encode("ascii", "ignore").decode("ascii")
                clave = ascii_only.lower().replace(" ", "").replace("-", "").replace("_", "")
                equivalencias = {
                    "jefebrigada": "jefeBrigada",
                    "jefe": "jefeBrigada",
                    "jefedebrigada": "jefeBrigada",
                    "botanico": "botanico",
                    "botanica": "botanico",
                    "botanicos": "botanico",
                    "botanic": "botanico",
                    "auxiliar": "auxiliar",
                    "coinvestigador": "coinvestigador",
                    "coinvestigadora": "coinvestigador",
                    "coinvestigadores": "coinvestigador",
                }
                return equivalencias.get(clave, "")

            for relacion in b_db.integrantes:
                rol_canonico = _normalizar_rol(relacion.rol)
                if rol_canonico:
                    roles_counts[rol_canonico] += 1
                    continue

                integrante = getattr(relacion, "integrante", None)
                if not integrante:
                    continue
                if getattr(integrante, "jefeBrigada", False):
                    roles_counts["jefeBrigada"] += 1
                elif getattr(integrante, "botanico", False):
                    roles_counts["botanico"] += 1
                elif getattr(integrante, "auxiliar", False):
                    roles_counts["auxiliar"] += 1
                elif getattr(integrante, "coinvestigador", False):
                    roles_counts["coinvestigador"] += 1

            resumen_partes: list[str] = []
            for rol, conteo in roles_counts.items():
                singular, plural = roles_destacados[rol]
                etiqueta = singular if conteo == 1 else plural
                resumen_partes.append(f"{conteo} {etiqueta}")

            resumen_roles = " | ".join(resumen_partes)
            resumen_texto = f"Integrantes ({total_integrantes}) | {resumen_roles}" if resumen_roles else f"Integrantes ({total_integrantes})"

            # Asignar el resumen final al campo 'integrantes'
            b_salida.integrantes = resumen_texto
            brigadas_salida.append(b_salida)

        return brigadas_salida

    
def get_brigada_repository(
    session: Session = Depends(get_session),
) -> BrigadaRepository:
    return DBBrigadaRepository(session)
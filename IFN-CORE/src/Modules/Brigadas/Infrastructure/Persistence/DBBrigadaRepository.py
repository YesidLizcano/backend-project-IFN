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
        stmt = select(BrigadaDB).options(selectinload(BrigadaDB.integrantes))
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

            for relacion in b_db.integrantes:
                rol = relacion.rol or ""
                if rol in roles_counts:
                    roles_counts[rol] += 1

            resumen_partes: list[str] = []
            for rol, conteo in roles_counts.items():
                if conteo <= 0:
                    continue

                singular, plural = roles_destacados[rol]
                if conteo == 1:
                    resumen_partes.append(singular)
                else:
                    resumen_partes.append(f"{conteo} {plural}")

            if resumen_partes:
                if len(resumen_partes) == 1:
                    resumen_roles = resumen_partes[0]
                elif len(resumen_partes) == 2:
                    resumen_roles = " y ".join(resumen_partes)
                else:
                    resumen_roles = ", ".join(resumen_partes[:-1]) + f" y {resumen_partes[-1]}"
                resumen_texto = f"Integrantes ({total_integrantes}) | {resumen_roles}"
            else:
                resumen_texto = f"Integrantes ({total_integrantes})"

            # Asignar el resumen final al campo 'integrantes'
            b_salida.integrantes = resumen_texto
            brigadas_salida.append(b_salida)

        return brigadas_salida

    
def get_brigada_repository(
    session: Session = Depends(get_session),
) -> BrigadaRepository:
    return DBBrigadaRepository(session)
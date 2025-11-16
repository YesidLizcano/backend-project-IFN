from fastapi import Depends
from sqlmodel import Session, select
from typing import List
from datetime import date
from sqlalchemy import exists, and_
from src.Modules.Brigadas.Domain.integrante import Integrante, IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.integrante_db import IntegranteDB
from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB
from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
from src.Shared.Infrastructure.Persistence.municipio_db import MunicipioDB
from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB
from src.Shared.Infrastructure.Persistence.database import get_session


class DBIntegranteRepository(IntegranteRepository):

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, integrante: Integrante) -> IntegranteSalida:
        db_integrante = IntegranteDB(**integrante.model_dump())
        self.db.add(db_integrante)
        self.db.commit()
        self.db.refresh(db_integrante)
        return IntegranteSalida.model_validate(db_integrante)
    
    def buscar_por_id(self, integrante_id: int) -> IntegranteSalida | None:
        db_integrante = self.db.get(IntegranteDB, integrante_id)
        return IntegranteSalida.model_validate(db_integrante) if db_integrante else None
    
    def listar_por_region(self, ids_departamentos: List[int], fecha_inicio: date, fecha_fin_aprox: date, rol: str) -> List[IntegranteSalida]:
        try:
            if not ids_departamentos:
                return []
            
            # Subconsulta: existe asignación con fechas que se solapan con el rango solicitado
            overlapping_assignments = (
                exists()
                .where(
                    and_(
                        IntegranteBrigadaDB.id_integrante == IntegranteDB.id,
                        IntegranteBrigadaDB.id_brigada == BrigadaDB.id,
                        BrigadaDB.conglomerado_id == ConglomeradoDB.id,
                        ConglomeradoDB.fechaInicio <= fecha_fin_aprox,
                        ConglomeradoDB.fechaFinAprox >= fecha_inicio,
                    )
                )
            )

            # Mapeo de rol a campo booleano en IntegranteDB
            rol_field_map = {
                'jefeBrigada': IntegranteDB.jefeBrigada,
                'botanico': IntegranteDB.botanico,
                'auxiliar': IntegranteDB.auxiliar,
                'coinvestigador': IntegranteDB.coinvestigador
            }

            # Obtener el campo booleano correspondiente al rol
            rol_field = rol_field_map.get(rol)
            if rol_field is None:
                # Si el rol no es válido, retornar lista vacía
                return []

            # Buscar integrantes de municipios en los departamentos dados y que NO tengan traslape de fechas
            stmt = (
                select(IntegranteDB)
                .join(MunicipioDB, IntegranteDB.municipio_id == MunicipioDB.id)
                .where(MunicipioDB.departamento_id.in_(ids_departamentos))
                .where(IntegranteDB.estado == 'Activo')
                .where(~overlapping_assignments)
                .where(rol_field == True)  # Verificar que el campo booleano del rol sea True
            )
            
            integrantes_db = self.db.exec(stmt).all()
            
            # Convertir a IntegranteSalida usando model_validate
            integrantes_salida = [
                IntegranteSalida.model_validate(integrante) 
                for integrante in integrantes_db
            ]
                
            return integrantes_salida
            
        except Exception as e:
            print(f"Error al listar integrantes por región: {e}")
            return []


def get_integrante_repository(
    session: Session = Depends(get_session),
) -> IntegranteRepository:
    return DBIntegranteRepository(session)
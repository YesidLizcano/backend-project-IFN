from fastapi import Depends
from sqlmodel import Session, select
from typing import List
from datetime import date
from sqlalchemy import exists, and_
from sqlalchemy.sql.elements import ColumnElement
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

    def buscar_asignaciones_superpuestas(
        self,
        integrante_id,
        fecha_inicio: date,
        fecha_fin_aprox: date,
        excluir_brigada_id: int | None = None,
    ):
        condiciones = [
            IntegranteBrigadaDB.id_integrante == integrante_id,
            ConglomeradoDB.fechaInicio <= fecha_fin_aprox,
            ConglomeradoDB.fechaFinAprox >= fecha_inicio,
            IntegranteBrigadaDB.id_brigada == BrigadaDB.id,
            BrigadaDB.conglomerado_id == ConglomeradoDB.id,
        ]

        # Evitar marcar como conflicto la misma brigada
        if excluir_brigada_id is not None:
            condiciones.append(IntegranteBrigadaDB.id_brigada != excluir_brigada_id)

        return exists().where(and_(*condiciones))
    
    def buscar_por_id(self, integrante_id: int) -> IntegranteSalida | None:
        db_integrante = self.db.get(IntegranteDB, integrante_id)
        return IntegranteSalida.model_validate(db_integrante) if db_integrante else None
    
    def listar_por_region(self, ids_departamentos: List[int], fecha_inicio: date, fecha_fin_aprox: date, rol: str) -> List[IntegranteSalida]:
        try:
            if not ids_departamentos:
                return []
            
            # Subconsulta reutilizable: traslape de fechas con conglomerados asignados
            asignaciones_superpuestas = self.buscar_asignaciones_superpuestas(
                IntegranteDB.id, fecha_inicio, fecha_fin_aprox
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
                .where(~asignaciones_superpuestas)
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

    def listar_por_brigada(self, brigada_id: int) -> List[IntegranteSalida]:
        try:
            stmt = (
                select(IntegranteDB)
                .join(IntegranteBrigadaDB, IntegranteBrigadaDB.id_integrante == IntegranteDB.id)
                .where(IntegranteBrigadaDB.id_brigada == brigada_id)
            )
            integrantes_db = self.db.exec(stmt).all()
            return [IntegranteSalida.model_validate(i) for i in integrantes_db]
        except Exception as e:
            print(f"Error al listar integrantes por brigada {brigada_id}: {e}")
            return []

    def listar_integrantes_con_y_sin_solapamiento(
        self,
        brigada_id: int,
        fecha_inicio: date,
        fecha_fin_aprox: date,
    ) -> dict:
        """
        Retorna dos listas:
        - integrantes_con_solapamiento
        - integrantes_sin_solapamiento

        Para una brigada dada y un rango de fechas nuevo.
        """
        try:
            # 1) Reutilizar listado base de integrantes de la brigada
            integrantes_brigada: List[IntegranteSalida] = self.listar_por_brigada(brigada_id)

            # 2) Construir expresión de solapamiento con otras brigadas (excluyendo la misma)
            solapamiento_expresion = self.buscar_asignaciones_superpuestas(
                integrante_id=IntegranteDB.id,
                fecha_inicio=fecha_inicio,
                fecha_fin_aprox=fecha_fin_aprox,
                excluir_brigada_id=brigada_id,
            )

            # 3) Obtener IDs de integrantes con solapamiento mediante una consulta
            query_solapados = (
                select(IntegranteDB)
                .join(
                    IntegranteBrigadaDB,
                    IntegranteBrigadaDB.id_integrante == IntegranteDB.id,
                )
                .where(IntegranteBrigadaDB.id_brigada == brigada_id)
                .where(solapamiento_expresion)
            )
            integrantes_con_db = self.db.exec(query_solapados).all()
            ids_solapados = {i.id for i in integrantes_con_db}

            # 4) Particionar la lista reutilizada en con/sin solapamiento
            con_solapamiento = [i for i in integrantes_brigada if i.id in ids_solapados]
            sin_solapamiento = [i for i in integrantes_brigada if i.id not in ids_solapados]

            return {
                "con_solapamiento": con_solapamiento,
                "sin_solapamiento": sin_solapamiento,
            }

        except Exception as e:
            print("Error al listar integrantes con/sin solapamiento:", e)
            return {
                "con_solapamiento": [],
                "sin_solapamiento": []
            }



def get_integrante_repository(
    session: Session = Depends(get_session),
) -> IntegranteRepository:
    return DBIntegranteRepository(session)
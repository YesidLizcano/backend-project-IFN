from fastapi import FastAPI
from typing import Annotated

from fastapi import Depends
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, SQLModel
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- VALIDACIÓN CRÍTICA ---
if not DATABASE_URL:
    raise ValueError(
        "FATAL: DATABASE_URL no está definida. "
        "Asegúrate de que existe en el archivo .env y que este se carga correctamente."
    )


class DatabaseManager:
    """Clase que encapsula la gestión de la base de datos."""
    
    _engine = create_engine(DATABASE_URL)
    
    @classmethod
    def get_engine(cls):
        """Obtiene el engine de la base de datos."""
        return cls._engine
    
    @classmethod
    def create_all_tables(cls, app: FastAPI):
        """Crea todas las tablas en la base de datos."""
        SQLModel.metadata.create_all(cls._engine)
        yield
    
    @classmethod
    def get_session(cls):
        """Proporciona una sesión de base de datos."""
        with Session(cls._engine) as session:
            yield session


# Alias para compatibilidad con código existente
engine = DatabaseManager.get_engine()
create_all_tables = DatabaseManager.create_all_tables
get_session = DatabaseManager.get_session
SessionDep = Annotated[Session, Depends(get_session)]
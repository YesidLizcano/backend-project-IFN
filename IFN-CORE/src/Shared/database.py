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

engine = create_engine(DATABASE_URL)



def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
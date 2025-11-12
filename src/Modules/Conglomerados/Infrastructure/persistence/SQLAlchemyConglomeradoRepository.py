from sqlmodel import Session, select
from fastapi import Depends

# --- Importaciones de Dominio ---
# (Ajusta las rutas si es necesario)
from src.Modules.Conglomerados.Domain.conglomerado import Conglomerado, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.subparcela import Subparcela
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository

# --- Importaciones de Infraestructura ---
from src.Modules.Conglomerados.Infrastructure.persistence.conglomerado_db import ConglomeradoDB
from src.Modules.Conglomerados.Infrastructure.persistence.subparcela_db import SubparcelaDB
from src.Shared.Infrastructure.Persistence.database import get_session


class SQLAlchemyConglomeradoRepository(ConglomeradoRepository):
    """
    Implementación concreta del repositorio de conglomerados usando SQLAlchemy/SQLModel.
    Maneja el Conglomerado como la raíz de un agregado, incluyendo sus Subparcelas.
    """
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, conglomerado: Conglomerado, subparcelas: list[Subparcela]) -> ConglomeradoSalida:
        """
        Guarda un nuevo conglomerado y sus subparcelas asociadas
        en una única transacción atómica.
        """
        
        # 1. Mapear el Conglomerado (Dominio) a ConglomeradoDB (Infraestructura)
        db_conglomerado = ConglomeradoDB(**conglomerado.model_dump())

        # 2. Mapear la lista de Subparcela (Dominio) a SubparcelaDB (Infraestructura)
        # Excluimos 'conglomerado_id' porque aún no existe y el ORM lo manejará.
        db_subparcelas = [
            SubparcelaDB(**sp.model_dump(exclude={"conglomerado_id"}))
            for sp in subparcelas
        ]

        # 3. ¡La magia del ORM!
        # Vinculamos los hijos al padre en memoria.
        # SQLAlchemy/SQLModel es lo suficientemente inteligente para entender
        # que debe insertar al padre, obtener su ID, y luego usar ese ID
        # para insertar a los hijos, todo dentro del 'commit()'.
        db_conglomerado.subparcelas = db_subparcelas

        try:
            # 4. Agregar el padre a la sesión.
            # Los hijos se añaden automáticamente gracias a la relación (cascade).
            self.db.add(db_conglomerado)
            
            # 5. Ejecutar la transacción (UNA SOLA VEZ)
            self.db.commit()
            
            # 6. Refrescar el objeto padre para obtener el ID generado por la BD
            # y cargar las relaciones que acabamos de crear.
            self.db.refresh(db_conglomerado)
            
        except Exception as e:
            # 7. Si algo falla (ej. restricción de BD), deshacer todo.
            self.db.rollback()
            raise e  # Relanzar el error para que el caso de uso lo maneje

        # 8. Mapear el objeto de BD (ya con ID) al DTO de Salida
        return ConglomeradoSalida.model_validate(db_conglomerado)

    def buscar_por_id(self, conglomerado_id: int) -> Conglomerado | None:
        """
        Busca un conglomerado por su ID.
        Devuelve el modelo de Dominio 'Conglomerado'.
        """
        db_conglomerado = self.db.get(ConglomeradoDB, conglomerado_id)
        
        if db_conglomerado:
            # Asumiendo que tu Pydantic model 'Conglomerado'
            # tiene 'Config.from_attributes = True'
            return Conglomerado.model_validate(db_conglomerado)
        return None

    def listar_conglomerados(self) -> list[ConglomeradoSalida]:
        """
        Devuelve una lista de todos los conglomerados como DTOs de Salida.
        """
        db_conglomerados = self.db.exec(select(ConglomeradoDB)).all()
        
        # Mapear cada objeto de BD al DTO de Salida
        return [ConglomeradoSalida.model_validate(db_c) for db_c in db_conglomerados]


def get_conglomerado_repository(session: Session = Depends(get_session)) -> ConglomeradoRepository:
    """
    Proveedor de dependencias de FastAPI para inyectar el repositorio
    de conglomerados en los endpoints/casos de uso.
    """
    return SQLAlchemyConglomeradoRepository(session)
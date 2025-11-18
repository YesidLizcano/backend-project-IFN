from abc import ABC, abstractmethod
from typing import Any, Optional

class AutenticacionRepository(ABC):
    """Interfaz (Contrato) para la capa de persistencia de autenticación."""
    @abstractmethod
    def _buscar_documento_usuario(self, user_email: str) -> Optional[Any]:
        """
        Busca el documento del usuario en la fuente de datos por email.

        Retorna un objeto documento de la fuente de datos o None si no existe.
        (La implementación concreta define el tipo de documento, p.ej. Firestore.)
        """
        pass

    @abstractmethod
    def obtener_datos_usuario(self, email: str) -> dict:
        """
        Busca datos del usuario y su hash de contraseña.

                Retorna un diccionario con los datos del usuario más el hash:
                {
                    'uid': str,
                    'email': str,
                    'name': str,
                    'password_hash': str
                }
        """
        pass
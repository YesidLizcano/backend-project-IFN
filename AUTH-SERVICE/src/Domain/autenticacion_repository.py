from abc import ABC, abstractmethod

class AutenticacionRepository(ABC):
    """Interfaz (Contrato) para la capa de persistencia de autenticación."""
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
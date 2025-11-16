from src.Domain.autenticacion_repository import AutenticacionRepository
from src.Infrastructure.Core import firebase_config as fb


def buscar_documento_usuario(user_email: str):
    """Busca el documento de usuario en 'users' o 'user' por id = email o por campo 'email'."""
    # Colecciones a intentar: primero 'users' (convención), luego 'user' (por compatibilidad)
    for col in ("users", "user"):
        ref = fb.db.collection(col)

        # 1) Buscar por id de documento = email
        doc = ref.document(user_email).get()
        if doc.exists:
            return doc

        # 2) Buscar por campo 'email' (igualado exacto en minúsculas)
        try:
            stream = ref.where('email', '==', user_email).limit(1).stream()
            found = next(stream, None)
            if found is not None:
                return found
        except Exception:
            # Si la colección no existe o no hay índices aún, continuar al siguiente intento
            pass

    return None


class FirebaseAuthRepository(AutenticacionRepository):
    def obtener_datos_usuario(self, email: str) -> dict:
        """Lee Firestore para obtener datos y hash del usuario.

        Intenta en 'users' y 'user', por docId=email o por campo 'email'.
        Acepta 'name' o 'Nombre' y deriva 'uid' si falta.
        """
        if fb.db is None:
            fb.inicializar_firebase()

        user_email = email.strip().lower()
        doc = buscar_documento_usuario(user_email)
        if doc is None:
            raise Exception("Usuario no encontrado")

        data = doc.to_dict() or {}

        # Mapear posibles llaves: nombre puede venir como 'name' o 'Nombre'
        name = data.get('name') or data.get('Nombre') or data.get('nombre')
        uid = data.get('uid') or doc.id or user_email
        password_hash = (data.get('password_hash') or data.get('passwordHash') or '').strip()

        if not password_hash:
            raise Exception("Datos de usuario incompletos: falta password_hash")

        # Si no hay name, por lo menos usa el local-part del email
        if not name:
            name = user_email.split('@')[0]

        return {
            "uid": uid,
            "email": data.get("email", user_email),
            "name": name,
            "password_hash": password_hash,
        }
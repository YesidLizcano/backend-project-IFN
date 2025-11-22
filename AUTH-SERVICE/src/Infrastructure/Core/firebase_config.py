import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Variable global para almacenar el cliente de Firestore
db = None


def inicializar_firebase():
    """Inicializa la aplicación de Firebase Admin SDK y Firestore.

    Prioriza credenciales desde la variable de entorno
    GOOGLE_APPLICATION_CREDENTIALS_JSON (entornos como Render) y,
    si no existe, hace fallback al archivo indicado por
    GOOGLE_APPLICATION_CREDENTIALS (entorno local).
    """

    global db
    load_dotenv()

    # Solo inicializa si no ha sido inicializado antes
    if not firebase_admin._apps:
        try:
            # 1. Intentar leer credenciales desde variable de entorno JSON
            cred_json_str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

            if cred_json_str:
                # La variable existe: intentar deserializar el JSON
                try:
                    cred_dict = json.loads(cred_json_str)
                except json.JSONDecodeError as e:
                    raise Exception(
                        "El contenido de GOOGLE_APPLICATION_CREDENTIALS_JSON no es un JSON válido."
                    ) from e

                cred = credentials.Certificate(cred_dict)
            else:
                # 2. Fallback: usar ruta de archivo local
                cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
                if not cred_path or not os.path.exists(cred_path):
                    raise FileNotFoundError(
                        "No se encontró GOOGLE_APPLICATION_CREDENTIALS_JSON ni un archivo válido en "
                        "GOOGLE_APPLICATION_CREDENTIALS. Configura una de las dos opciones."
                    )

                cred = credentials.Certificate(cred_path)

            # Inicializa la aplicación de Firebase Admin
            firebase_admin.initialize_app(cred)

            # Inicializa el cliente de Firestore
            db = firestore.client()
            print("✅ Firebase Admin SDK y Firestore inicializados correctamente.")

        except FileNotFoundError as e:
            raise Exception(
                "❌ Error: No se encontraron credenciales de Firebase. "
                "Configura GOOGLE_APPLICATION_CREDENTIALS_JSON o un archivo en GOOGLE_APPLICATION_CREDENTIALS."
            ) from e
        except Exception as e:
            # Captura errores como permisos inválidos o problemas de conexión
            print(f"❌ Error al inicializar Firebase: {e}")
            raise Exception("No se pudo conectar al proyecto de Firebase.")
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Variable global para almacenar el cliente de Firestore
db = None

def inicializar_firebase():
    """Inicializa la aplicación de Firebase Admin SDK y Firestore."""
    global db
    load_dotenv()
    
    # Solo inicializa si no ha sido inicializado antes
    if not firebase_admin._apps:
        try:
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not cred_path or not os.path.exists(cred_path):
                raise FileNotFoundError(
                    "No se encontró GOOGLE_APPLICATION_CREDENTIALS o el archivo no existe. "
                    "Configura la ruta en .env, ej.:\n"
                    "GOOGLE_APPLICATION_CREDENTIALS=/ruta/segura/national-forest-inventory.json"
                )

            # Crea las credenciales a partir del archivo JSON indicado por la variable de entorno
            cred = credentials.Certificate(cred_path)
            
            # Inicializa la aplicación de Firebase Admin
            firebase_admin.initialize_app(cred)
            
            # Inicializa el cliente de Firestore
            db = firestore.client()
            print("✅ Firebase Admin SDK y Firestore inicializados correctamente.")
        
        except FileNotFoundError:
            raise Exception("❌ Error: No se encontró el archivo de credenciales. Revisa GOOGLE_APPLICATIONS_CREDENTIALS en .env.")
        except Exception as e:
            # Captura errores como permisos inválidos o problemas de conexión
            print(f"❌ Error al inicializar Firebase: {e}")
            raise Exception("No se pudo conectar al proyecto de Firebase.")
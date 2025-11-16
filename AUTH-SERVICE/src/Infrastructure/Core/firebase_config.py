import firebase_admin 
from firebase_admin import credentials, firestore
import os

# Define la ruta al archivo de credenciales de servicio (ruta relativa desde este archivo)
# Subimos 3 niveles: core/ -> Infrastructure/ -> src/ -> AUTH-SERVICE/
CRED_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.serviceAccountKey.json')

# Variable global para almacenar el cliente de Firestore
db = None

def inicializar_firebase():
    """Inicializa la aplicación de Firebase Admin SDK y Firestore."""
    global db
    
    # Solo inicializa si no ha sido inicializado antes
    if not firebase_admin._apps:
        try:
            # Crea las credenciales a partir del archivo JSON
            cred = credentials.Certificate(CRED_PATH)
            
            # Inicializa la aplicación de Firebase Admin
            firebase_admin.initialize_app(cred, {
                'projectId': 'national-forest-inventory' # Puedes usar el project_id del JSON
            })
            
            # Inicializa el cliente de Firestore
            db = firestore.client()
            print("✅ Firebase Admin SDK y Firestore inicializados para 'national-forest-inventory'.")
        
        except FileNotFoundError:
            raise Exception(f"❌ Error: No se encontró el archivo de credenciales en {CRED_PATH}. Asegúrate de que existe.")
        except Exception as e:
            # Captura errores como permisos inválidos o problemas de conexión
            print(f"❌ Error al inicializar Firebase: {e}")
            raise Exception("No se pudo conectar al proyecto de Firebase.")
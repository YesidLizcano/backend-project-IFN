# AUTH-SERVICE

Servicio de autenticación (FastAPI) con Firebase/Firestore y JWT.

## Requisitos
- Python 3.10+
- Acceso a un JSON de Service Account de Google Cloud (Firebase Admin)
- Firestore habilitado en el proyecto `national-forest-inventory`

## Puesta en marcha (desarrollador nuevo)

1) Clonar el repositorio y entrar a la carpeta del servicio:
```bash
git clone <URL_DEL_REPO>
cd AUTH-SERVICE
```

2) Crear entorno virtual e instalar dependencias:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Configurar variables de entorno:
- Copia `.env.example` a `.env` y ajusta valores.
- MUY IMPORTANTE: coloca el JSON del Service Account FUERA del repo y apunta su ruta en `GOOGLE_APPLICATION_CREDENTIALS`.
```bash
cp .env.example .env
# Edita .env y actualiza rutas/secretos
```

4) Iniciar la API (puerto 8000 o alternativo si está ocupado):
```bash
uvicorn src.main:app --reload --port 8000
# Si 8000 está ocupado:
# uvicorn src.main:app --reload --port 8001
```

5) Probar en Swagger UI:
- Abre http://localhost:8000/docs (o el puerto que uses).
- `POST /auth/login` con body JSON:
```json
{
  "email": "tu@correo.com",
  "password": "TuPassword"
}
```
- Copia `access_token` y pulsa "Authorize" (esquema HTTP Bearer) para pegar el token.
- Usa `POST /auth/validar-token` para verificar el token.

## Datos de usuario en Firestore
Crea un documento en `users` (o `user`) con estos campos mínimos:
- `email` (string)
- `name` (string) — opcional, se infiere del email si falta
- `password_hash` (string, bcrypt)

Generar un hash bcrypt (ejemplo rápido):
```bash
python - <<'PY'
from passlib.hash import bcrypt
print(bcrypt.hash("TuPassword"))
PY
```

## Seguridad y secretos
- `.env` y archivos de credenciales están ignorados por Git (.gitignore).
- No subas el JSON del Service Account al repo.
- Si un secreto fue expuesto, revoca la clave y genera una nueva en Google Cloud.

## Notas
- Las variables JWT se leen desde `.env` (llave, algoritmo, expiración).
- Firebase Admin se inicializa con `GOOGLE_APPLICATION_CREDENTIALS`.

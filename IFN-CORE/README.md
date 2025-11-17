<div align="center">
  <h1>IFN-CORE</h1>
  <p><strong>Backend FastAPI para Inventario Forestal Nacional</strong></p>
  <p>Gestión de conglomerados, brigadas, integrantes, material y datos geoespaciales.</p>
</div>

---

## 📌 Introducción
IFN-CORE es un servicio backend construido con FastAPI y SQLModel que soporta el flujo operativo del Inventario Forestal Nacional: definición de conglomerados de muestreo, creación de brigadas de campo, asignación y consulta de integrantes, manejo de municipios/departamentos y control de equipo/material. Se integra con PostgreSQL/PostGIS para capacidades espaciales y bibliotecas geo (GeoPandas, GeoAlchemy2, Geopy).

> [!NOTE]
> El proyecto usa Pydantic v2 y SQLModel sobre SQLAlchemy 2.x, por lo que se recomiendan prácticas modernas (async opcional futuro, modelos `from_attributes`).

## ✨ Características Clave
- Conglomerados: creación y actualización de fechas (`fechaInicio`, `fechaFinAprox`).
- Brigadas: asociación 1:1 con conglomerado y gestión de estado.
- Integrantes: filtrado por región (departamentos relacionados) y por brigada.
- Asignaciones Integrante-Brigada con roles (jefeBrigada, botanico, auxiliar, coinvestigador).
- Catálogo territorial: departamentos y municipios.
- Material y control de equipos (estructura base lista para extender).
- Autocreación de tablas al inicio (lifespan FastAPI).
- PostGIS listo vía `docker-compose`.

## 🧱 Arquitectura
> [!TIP]
> Se adopta una organización por módulos con capas Domain / Application / Infrastructure.

| Capa | Responsabilidad |
|------|-----------------|
| Domain | Modelos de dominio, interfaces de repositorios y reglas simples. |
| Application | Casos de uso orquestando lógica (validaciones, secuencia de repos). |
| Infrastructure | Adaptadores: routers FastAPI y persistencia (SQLModel / DB). |

Cada módulo expone su router (API) y sus repos implementan las interfaces abstractas definidas en Domain.

## 📦 Módulos Principales
- Brigadas: `Brigada`, `Integrante`, `IntegranteBrigada` y sus repositorios.
- Conglomerados: definición de conglomerado y subparcelas (base para muestreo forestal).
- Shared: departamentos y municipios (referencia territorial para otros módulos).
- MaterialEquipo: control de material y equipos (en expansión).

## ⚙️ Requisitos
| Componente | Versión sugerida |
|------------|------------------|
| Python | 3.12+ |
| PostgreSQL / PostGIS | Imagen `postgis/postgis:16-3.4` |
| FastAPI | 0.121.1 |
| SQLModel | 0.0.27 |

## 🚀 Puesta en Marcha Rápida
```bash
# 1. Clonar repositorio
git clone <repo-url>
cd IFN-CORE

# 2. Iniciar base de datos PostGIS
docker compose up -d

# 3. Crear entorno virtual
python -m venv venv
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear archivo .env
echo 'DATABASE_URL=postgresql+psycopg2://admin_forest:ifn2025@localhost:5432/inventario_forestal_db' > .env

# 6. Ejecutar servidor (opción 1)
uvicorn src.main:app --reload

# (opción 2) usando fastapi-cli
fastapi run
```

> [!WARNING]
> Si `DATABASE_URL` no está presente en `.env`, el arranque fallará de forma explícita.

## 🔄 Flujo de Datos Básico
1. Crear Departamento → Crear Municipios asociados.
2. Crear Conglomerado (contiene fechas y coordenadas). 
3. Crear Brigada para el Conglomerado (única por conglomerado).
4. Crear Integrantes (asociados a municipios) y consultarlos por región para disponibilidad.
5. Asignar Integrantes a Brigada (crea registros en tabla puente).
6. Consultar Integrantes por Brigada o por Región y Rol.

## 🗂 Estructura Esencial
```
src/
  main.py               # Punto de entrada FastAPI
  Modules/
    Brigadas/           # Brigadas, Integrantes y asignaciones
    Conglomerados/      # Conglomerados y subparcelas
    MaterialEquipo/     # Control equipo y material
    Shared/             # Departamentos y Municipios + DB Commons
```

## 🧪 API (Resumen de Endpoints)
> [!NOTE]
> Para documentación completa visita `/docs` al ejecutar el servidor.

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/departamentos` | Crear departamento |
| GET | `/departamentos` | Listar departamentos |
| POST | `/municipios/{departamento_id}` | Crear municipio |
| GET | `/municipios` | Listar municipios |
| POST | `/conglomerados/{municipio_id}` | Crear conglomerado (ver router real) |
| PATCH | `/conglomerados/{id}/fechas` | Actualizar fechas conglomerado |
| POST | `/brigadas/{conglomerado_id}` | Crear brigada |
| POST | `/integrantes/{municipio_id}` | Crear integrante |
| GET | `/integrantes/region/{departamento_id}` | Listar integrantes disponibles por región y rol |
| GET | `/integrantes/brigada/{brigada_id}` | Listar integrantes asignados a brigada |

### Ejemplos curl
```bash
# Crear departamento
curl -X POST http://localhost:8000/departamentos \
  -H 'Content-Type: application/json' \
  -d '{"nombre":"Amazonas"}'

# Crear municipio
curl -X POST http://localhost:8000/municipios/1 \
  -H 'Content-Type: application/json' \
  -d '{"nombre":"Leticia"}'

# Listar departamentos
curl http://localhost:8000/departamentos

# Listar integrantes por región y rol
curl "http://localhost:8000/integrantes/region/1?fechaInicio=2025-11-20&fechaFinAprox=2025-11-30&rol=botanico"

# Listar integrantes por brigada
curl http://localhost:8000/integrantes/brigada/3
```

## 🛠 Desarrollo
```bash
# Formato y lint (puedes integrar herramientas adicionales)
python -m pip install ruff black isort
ruff check .
black .
isort .
```

> [!TIP]
> Considera añadir tests con Pytest para casos de uso críticos (fechas de conglomerado, disponibilidad de integrantes).

## 🗄 Persistencia
- ORM: SQLModel sobre SQLAlchemy 2.x.
- Relaciones clave:
  - `BrigadaDB` 1:1 `ConglomeradoDB` (campo `conglomerado_id` único).
  - `IntegranteBrigadaDB` tabla puente (PK compuesta: `id_brigada`, `id_integrante`).
- Creación de tablas en `lifespan` (`create_all_tables`).

## 🌍 Geoespacial
- PostGIS habilitado por la imagen Docker.
- Librerías instaladas: GeoAlchemy2, GeoPandas, Geopy (listas para cálculos y transformaciones futuras).

## 🔐 Validaciones Notables
- `DATABASE_URL` obligatorio (error explícito si falta).
- Conglomerado: `fechaInicio <= fechaFinAprox` y reglas adicionales en actualización.
- Integrantes por región: exclusión de asignaciones traslapadas usando subconsulta `exists`.

## 🧩 Extensiones Futuras (Sugerencias)
> [!IMPORTANT]
> Estas ideas no están implementadas todavía pero la arquitectura facilita su incorporación.

- Autenticación / Autorización (JWT / OAuth2).
- Versionado de API (v1, v2...).
- Paginación y filtros avanzados en listados.
- Integración GIS (capas geográficas y buffer de coordenadas).
- Métricas Prometheus y Health Checks.

## 🩺 Troubleshooting
| Problema | Causa Común | Solución |
|----------|-------------|----------|
| Error `DATABASE_URL no está definida` | Falta `.env` | Crear `.env` con cadena correcta |
| 404 al usar endpoints | Ruta incorrecta | Consultar `/docs` y confirmar path |
| No se crean tablas | Motor sin permisos | Verificar conexión y usuario Postgres |
| Dependencias geo fallan | Librerías del sistema faltantes | Instalar `libgeos`, `gdal` según distro |

## 📄 Variables de Entorno
| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | Cadena de conexión completa a Postgres/PostGIS |

Ejemplo:
```
DATABASE_URL=postgresql+psycopg2://admin_forest:ifn2025@localhost:5432/inventario_forestal_db
```

## ✅ Checklist Rápido
- [x] DB levantada (`docker compose up -d`).
- [x] `.env` creado con `DATABASE_URL`.
- [x] Dependencias instaladas (`pip install -r requirements.txt`).
- [x] Servidor iniciado (`uvicorn src.main:app --reload`).
- [x] Endpoints accesibles (`/docs`).

> [!TIP]
> Usa `fastapi run` para un flujo más simplificado en desarrollo con recarga automática.

---

Desarrollado con ❤️ usando FastAPI y PostGIS.

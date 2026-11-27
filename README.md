# CRUD de Notas — FastAPI + SQLite + Jinja2

Proyecto de práctica que implementa un CRUD completo (crear, leer, actualizar y
eliminar) sobre una entidad simple: **notas de texto**.

La interfaz es un único formulario y un listado de textos que se actualiza con
cada operación. No hay JavaScript de framework ni paso de compilación: el HTML
se renderiza en el servidor con Jinja2.

## Tecnologías

| Componente | Uso |
| --- | --- |
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web y enrutamiento |
| [SQLite](https://www.sqlite.org/) | Persistencia de datos (librería estándar) |
| [Jinja2](https://jinja.palletsprojects.com/) | Plantillas HTML |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [pytest](https://docs.pytest.org/) | Pruebas automatizadas |

## Modelo de datos

La aplicación trabaja con una única tabla, `notas`:

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `id` | `INTEGER` | Clave primaria autoincremental |
| `texto` | `TEXT` | Contenido de la nota (obligatorio, máximo 280 caracteres) |
| `creado_en` | `TEXT` | Fecha de creación en formato ISO 8601 (UTC) |
| `actualizado_en` | `TEXT` | Fecha de la última modificación (UTC) |

El archivo de la base de datos se crea automáticamente en `data/crud.db` la
primera vez que se inicia la aplicación. Esa ruta se puede cambiar con la
variable de entorno `CRUD_DB_PATH`.

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
git clone https://github.com/lorf543/crud-fastapi-gitflow.git
cd crud-fastapi-gitflow

python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

La aplicación queda disponible en <http://127.0.0.1:8000> y la documentación
interactiva de la API en <http://127.0.0.1:8000/docs>.

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/` | Página principal con el formulario y el listado |
| POST | `/notas` | Crea una nota con el texto enviado en el formulario |
| GET | `/salud` | Verificación de estado del servicio |

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest
```

## Estructura del proyecto

```
crud-fastapi-gitflow/
├── app/
│   ├── main.py            # Aplicación FastAPI y rutas
│   ├── templates/         # Plantillas Jinja2
│   └── static/            # Hoja de estilos
├── tests/                 # Pruebas automatizadas
├── requirements.txt
└── requirements-dev.txt
```

## Flujo de trabajo con Git

El repositorio sigue una adaptación de Git Flow con tres ramas de integración:

- `main`: versión estable y publicada.
- `qa`: validación previa a producción.
- `dev`: integración del trabajo diario.

Cada funcionalidad se desarrolla en una rama `feature/*` y se integra mediante
Pull Requests en el orden `feature → dev → qa → main`.

## Autor

Eduardo Alberto Sanchez Lebron ([@lorf543](https://github.com/lorf543))

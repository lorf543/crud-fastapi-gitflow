"""Aplicación CRUD de notas construida con FastAPI.

La aplicación usa SQLite como almacenamiento, Jinja2 para renderizar el HTML
en el servidor y no requiere ningún paso de compilación en el frontend.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import crud
from .database import inicializar_base_datos

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI):
    """Prepara la base de datos antes de atender la primera petición."""
    inicializar_base_datos()
    yield


app = FastAPI(
    title="CRUD de Notas",
    description="Aplicación de ejemplo con FastAPI, SQLite y Jinja2.",
    version="1.0.0",
    lifespan=ciclo_de_vida,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request) -> HTMLResponse:
    """Renderiza la página principal con el listado de notas."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"items": crud.listar_notas()},
    )


@app.post("/notas")
def crear_nota(request: Request, texto: str = Form("")):
    """Crea una nota a partir del formulario y vuelve al listado."""
    try:
        crud.crear_nota(texto)
    except crud.TextoInvalidoError as error:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "items": crud.listar_notas(),
                "error": str(error),
                "borrador": texto,
            },
            status_code=400,
        )

    return RedirectResponse(url="/", status_code=303)


@app.get("/salud")
def salud() -> dict[str, str]:
    """Endpoint de verificación usado por monitoreo y pruebas."""
    return {"estado": "ok"}

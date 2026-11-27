"""Aplicación CRUD de notas construida con FastAPI.

Esta primera versión entrega el esqueleto del proyecto: la instancia de
FastAPI, el montaje de archivos estáticos, el motor de plantillas Jinja2 y
un endpoint de salud que permite verificar que el servicio está vivo.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="CRUD de Notas",
    description="Aplicación de ejemplo con FastAPI, SQLite y Jinja2.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request) -> HTMLResponse:
    """Renderiza la página principal de la aplicación."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"items": []},
    )


@app.get("/salud")
def salud() -> dict[str, str]:
    """Endpoint de verificación usado por monitoreo y pruebas."""
    return {"estado": "ok"}

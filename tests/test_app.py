"""Pruebas del esqueleto de la aplicación."""

from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_endpoint_salud_responde_ok() -> None:
    respuesta = cliente.get("/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_pagina_principal_renderiza_plantilla() -> None:
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    assert "Notas rápidas" in respuesta.text
    assert "Todavía no hay notas guardadas." in respuesta.text

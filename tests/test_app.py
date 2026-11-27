"""Pruebas de las rutas HTTP de la aplicación."""

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
    assert "Todavía no hay notas. ¡Agrega la primera!" in respuesta.text


def test_pagina_principal_muestra_el_formulario() -> None:
    respuesta = cliente.get("/")

    assert 'action="/notas"' in respuesta.text
    assert 'name="texto"' in respuesta.text


def test_crear_nota_redirige_al_listado() -> None:
    respuesta = cliente.post(
        "/notas",
        data={"texto": "Comprar café"},
        follow_redirects=False,
    )

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/"


def test_la_nota_creada_aparece_en_el_listado() -> None:
    cliente.post("/notas", data={"texto": "Comprar café"})

    pagina = cliente.get("/")

    assert "Comprar café" in pagina.text
    assert "Notas guardadas (1)" in pagina.text


def test_no_permite_crear_notas_vacias() -> None:
    respuesta = cliente.post(
        "/notas",
        data={"texto": "   "},
        follow_redirects=False,
    )

    assert respuesta.status_code == 400
    assert "no puede estar vacío" in respuesta.text

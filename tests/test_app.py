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


def test_el_listado_ofrece_un_enlace_de_edicion() -> None:
    cliente.post("/notas", data={"texto": "Editable"})

    pagina = cliente.get("/")

    assert "?editar=1" in pagina.text


def test_el_formulario_de_edicion_carga_el_texto_actual() -> None:
    cliente.post("/notas", data={"texto": "Texto viejo"})

    pagina = cliente.get("/?editar=1")

    assert 'action="/notas/1/editar"' in pagina.text
    assert 'value="Texto viejo"' in pagina.text


def test_editar_nota_actualiza_el_listado() -> None:
    cliente.post("/notas", data={"texto": "Texto viejo"})

    respuesta = cliente.post(
        "/notas/1/editar",
        data={"texto": "Texto nuevo"},
        follow_redirects=False,
    )

    assert respuesta.status_code == 303

    pagina = cliente.get("/")
    assert "Texto nuevo" in pagina.text
    assert "Texto viejo" not in pagina.text


def test_editar_nota_inexistente_devuelve_404() -> None:
    respuesta = cliente.post(
        "/notas/999/editar",
        data={"texto": "Sin dueño"},
        follow_redirects=False,
    )

    assert respuesta.status_code == 404


def test_editar_con_texto_vacio_muestra_error() -> None:
    cliente.post("/notas", data={"texto": "Algo válido"})

    respuesta = cliente.post(
        "/notas/1/editar",
        data={"texto": "   "},
        follow_redirects=False,
    )

    assert respuesta.status_code == 400
    assert "no puede estar vacío" in respuesta.text

"""Pruebas de la capa de persistencia y de las reglas de negocio."""

import pytest

from app import crud


def test_crear_nota_guarda_el_texto_normalizado() -> None:
    nota = crud.crear_nota("  Mi primera nota  ")

    assert nota["id"] > 0
    assert nota["texto"] == "Mi primera nota"
    assert nota["creado_en"] == nota["actualizado_en"]


def test_listar_notas_devuelve_las_mas_recientes_primero() -> None:
    crud.crear_nota("primera")
    crud.crear_nota("segunda")

    textos = [nota["texto"] for nota in crud.listar_notas()]

    assert textos == ["segunda", "primera"]


def test_obtener_nota_inexistente_devuelve_none() -> None:
    assert crud.obtener_nota(999) is None


def test_actualizar_nota_cambia_el_texto() -> None:
    nota = crud.crear_nota("texto original")

    actualizada = crud.actualizar_nota(nota["id"], "texto corregido")

    assert actualizada is not None
    assert actualizada["texto"] == "texto corregido"
    assert actualizada["creado_en"] == nota["creado_en"]


def test_actualizar_nota_inexistente_devuelve_none() -> None:
    assert crud.actualizar_nota(999, "cualquier cosa") is None


def test_eliminar_nota_la_quita_del_listado() -> None:
    nota = crud.crear_nota("efímera")

    assert crud.eliminar_nota(nota["id"]) is True
    assert crud.listar_notas() == []


def test_eliminar_nota_inexistente_devuelve_false() -> None:
    assert crud.eliminar_nota(999) is False


def test_contar_notas_refleja_los_registros() -> None:
    assert crud.contar_notas() == 0

    crud.crear_nota("una")
    crud.crear_nota("dos")

    assert crud.contar_notas() == 2


@pytest.mark.parametrize("texto", ["", "   ", None])
def test_texto_vacio_es_rechazado(texto) -> None:
    with pytest.raises(crud.TextoInvalidoError):
        crud.crear_nota(texto)


def test_texto_demasiado_largo_es_rechazado() -> None:
    with pytest.raises(crud.TextoInvalidoError):
        crud.crear_nota("a" * (crud.LONGITUD_MAXIMA + 1))

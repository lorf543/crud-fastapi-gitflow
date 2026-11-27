"""Configuración compartida de las pruebas.

Cada prueba trabaja sobre una base de datos SQLite temporal, de modo que la
suite nunca toca el archivo real de ``data/crud.db``.
"""

import pytest

from app.database import inicializar_base_datos


@pytest.fixture(autouse=True)
def base_de_datos_temporal(tmp_path, monkeypatch):
    monkeypatch.setenv("CRUD_DB_PATH", str(tmp_path / "prueba.db"))
    inicializar_base_datos()
    yield

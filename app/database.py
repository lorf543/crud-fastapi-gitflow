"""Configuración y utilidades de acceso a la base de datos SQLite.

La ruta del archivo se puede sobrescribir con la variable de entorno
``CRUD_DB_PATH``, algo que las pruebas aprovechan para trabajar sobre una
base de datos temporal y no ensuciar los datos reales.
"""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

RUTA_PREDETERMINADA = Path(__file__).resolve().parent.parent / "data" / "crud.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto TEXT NOT NULL,
    creado_en TEXT NOT NULL,
    actualizado_en TEXT NOT NULL
);
"""


def ruta_base_datos() -> Path:
    """Devuelve la ruta del archivo SQLite en uso."""
    return Path(os.getenv("CRUD_DB_PATH", str(RUTA_PREDETERMINADA)))


def conectar() -> sqlite3.Connection:
    """Abre una conexión configurada con filas accesibles por nombre."""
    ruta = ruta_base_datos()
    ruta.parent.mkdir(parents=True, exist_ok=True)

    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


@contextmanager
def sesion() -> Iterator[sqlite3.Connection]:
    """Administra una transacción: confirma al salir o revierte si falla."""
    conexion = conectar()
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def inicializar_base_datos() -> None:
    """Crea las tablas necesarias si todavía no existen."""
    with sesion() as conexion:
        conexion.executescript(ESQUEMA)

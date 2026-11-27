"""Operaciones CRUD sobre la tabla de notas.

Toda la validación de negocio vive aquí para que las rutas de FastAPI queden
delgadas y las reglas se puedan probar sin levantar el servidor.
"""

from datetime import datetime, timezone

from .database import sesion

LONGITUD_MAXIMA = 280

COLUMNAS = "id, texto, creado_en, actualizado_en"


class TextoInvalidoError(ValueError):
    """Se lanza cuando el texto de una nota no cumple las reglas del dominio."""


def _ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalizar_texto(texto: str | None) -> str:
    """Limpia y valida el texto recibido desde el formulario."""
    limpio = (texto or "").strip()

    if not limpio:
        raise TextoInvalidoError("El texto de la nota no puede estar vacío.")

    if len(limpio) > LONGITUD_MAXIMA:
        raise TextoInvalidoError(
            f"El texto no puede superar los {LONGITUD_MAXIMA} caracteres."
        )

    return limpio


def listar_notas() -> list[dict]:
    """Devuelve todas las notas, de la más reciente a la más antigua."""
    with sesion() as conexion:
        filas = conexion.execute(
            f"SELECT {COLUMNAS} FROM notas ORDER BY id DESC"
        ).fetchall()

    return [dict(fila) for fila in filas]


def obtener_nota(nota_id: int) -> dict | None:
    """Busca una nota por su identificador."""
    with sesion() as conexion:
        fila = conexion.execute(
            f"SELECT {COLUMNAS} FROM notas WHERE id = ?", (nota_id,)
        ).fetchone()

    return dict(fila) if fila else None


def crear_nota(texto: str | None) -> dict:
    """Crea una nota nueva y devuelve el registro almacenado."""
    contenido = normalizar_texto(texto)
    momento = _ahora()

    with sesion() as conexion:
        cursor = conexion.execute(
            "INSERT INTO notas (texto, creado_en, actualizado_en) VALUES (?, ?, ?)",
            (contenido, momento, momento),
        )
        nota_id = int(cursor.lastrowid)

    nota = obtener_nota(nota_id)
    assert nota is not None  # la fila acaba de insertarse
    return nota


def actualizar_nota(nota_id: int, texto: str | None) -> dict | None:
    """Actualiza el texto de una nota. Devuelve ``None`` si no existe."""
    contenido = normalizar_texto(texto)

    with sesion() as conexion:
        cursor = conexion.execute(
            "UPDATE notas SET texto = ?, actualizado_en = ? WHERE id = ?",
            (contenido, _ahora(), nota_id),
        )
        if cursor.rowcount == 0:
            return None

    return obtener_nota(nota_id)


def eliminar_nota(nota_id: int) -> bool:
    """Elimina una nota. Devuelve ``True`` si existía."""
    with sesion() as conexion:
        cursor = conexion.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
        return cursor.rowcount > 0


def contar_notas() -> int:
    """Cuenta las notas almacenadas."""
    with sesion() as conexion:
        fila = conexion.execute("SELECT COUNT(*) AS total FROM notas").fetchone()

    return int(fila["total"])

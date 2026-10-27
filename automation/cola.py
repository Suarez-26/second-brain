"""Estado durable de la automatización en SQLite (automation/state.db).

Tablas:
- mensajes:   cola de entrada. recibido -> procesando -> hecho | fallido (con reintentos).
- borradores: respuestas a terceros que esperan aprobación (Enviar / Editar / Descartar).
- propuestas: cambios a la Capa 1 (meta/open-loops.md) que esperan aprobación (Aceptar / Rechazar).

SQLite serializa las escrituras entre hilos y procesos; cada operación abre su conexión.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("VAULT_STATE_DB", Path(__file__).resolve().parent / "state.db"))
MAX_INTENTOS = 3
BACKOFF_SEG = (30, 120, 600)

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS mensajes (
    id TEXT PRIMARY KEY,
    origen TEXT NOT NULL,
    payload TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'recibido',
    intentos INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    proximo_intento TEXT,
    creado TEXT NOT NULL,
    actualizado TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_mensajes_estado ON mensajes(estado, proximo_intento);
CREATE TABLE IF NOT EXISTS borradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remitente TEXT NOT NULL,
    phone_id TEXT,
    mensaje_original TEXT NOT NULL,
    borrador TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    creado TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS propuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    datos TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    origen TEXT,
    creado TEXT NOT NULL
);
"""


def _ahora() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def conectar() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH, timeout=15, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=15000")
    con.executescript(_ESQUEMA)
    return con


# --- Cola de mensajes -----------------------------------------------------------------

def encolar(msg_id: str, origen: str, payload: dict[str, Any]) -> bool:
    """Devuelve False si el mensaje ya estaba (deduplicación por id)."""
    with conectar() as con:
        cur = con.execute(
            "INSERT OR IGNORE INTO mensajes (id, origen, payload, creado, actualizado) VALUES (?,?,?,?,?)",
            (msg_id, origen, json.dumps(payload, ensure_ascii=False), _ahora(), _ahora()),
        )
        return cur.rowcount == 1


def tomar_siguiente() -> sqlite3.Row | None:
    """Reserva el siguiente mensaje listo; BEGIN IMMEDIATE evita que dos workers tomen el mismo."""
    con = conectar()
    try:
        con.execute("BEGIN IMMEDIATE")
        fila = con.execute(
            """SELECT * FROM mensajes
               WHERE estado = 'recibido'
                  OR (estado = 'fallido' AND intentos < ? AND (proximo_intento IS NULL OR proximo_intento <= ?))
               ORDER BY creado LIMIT 1""",
            (MAX_INTENTOS, _ahora()),
        ).fetchone()
        if fila:
            con.execute(
                "UPDATE mensajes SET estado='procesando', intentos=intentos+1, actualizado=? WHERE id=?",
                (_ahora(), fila["id"]),
            )
        con.execute("COMMIT")
        return fila
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        con.close()


def marcar_hecho(msg_id: str) -> None:
    with conectar() as con:
        con.execute("UPDATE mensajes SET estado='hecho', error=NULL, actualizado=? WHERE id=?", (_ahora(), msg_id))


def marcar_fallido(msg_id: str, error: str) -> None:
    with conectar() as con:
        intentos = con.execute("SELECT intentos FROM mensajes WHERE id=?", (msg_id,)).fetchone()["intentos"]
        espera = BACKOFF_SEG[min(intentos, len(BACKOFF_SEG)) - 1]
        proximo = (dt.datetime.now() + dt.timedelta(seconds=espera)).isoformat(timespec="seconds")
        con.execute(
            "UPDATE mensajes SET estado='fallido', error=?, proximo_intento=?, actualizado=? WHERE id=?",
            (error[:500], proximo, _ahora(), msg_id),
        )


def recuperar_huerfanos(minutos: int = 15) -> int:
    """Al arrancar: lo que quedó en 'procesando' por una caída vuelve a la cola."""
    limite = (dt.datetime.now() - dt.timedelta(minutes=minutos)).isoformat(timespec="seconds")
    with conectar() as con:
        return con.execute(
            "UPDATE mensajes SET estado='fallido', error='interrumpido' WHERE estado='procesando' AND actualizado < ?",
            (limite,),
        ).rowcount


def resumen_cola() -> dict[str, int]:
    with conectar() as con:
        return {r["estado"]: r["n"] for r in con.execute("SELECT estado, COUNT(*) n FROM mensajes GROUP BY estado")}


# --- Borradores (copiloto) ------------------------------------------------------------

def crear_borrador(remitente: str, phone_id: str, mensaje_original: str, borrador: str) -> int:
    with conectar() as con:
        cur = con.execute(
            "INSERT INTO borradores (remitente, phone_id, mensaje_original, borrador, creado) VALUES (?,?,?,?,?)",
            (remitente, phone_id, mensaje_original, borrador, _ahora()),
        )
        return int(cur.lastrowid)


def borradores_pendientes() -> list[sqlite3.Row]:
    with conectar() as con:
        return con.execute("SELECT * FROM borradores WHERE estado='pendiente' ORDER BY id").fetchall()


def tomar_borrador(bid: int | None) -> sqlite3.Row | None:
    """Marca el borrador como 'enviando' de forma atómica (el último pendiente si bid es None)."""
    with conectar() as con:
        if bid is None:
            fila = con.execute("SELECT id FROM borradores WHERE estado='pendiente' ORDER BY id DESC LIMIT 1").fetchone()
            if not fila:
                return None
            bid = fila["id"]
        cur = con.execute("UPDATE borradores SET estado='enviando' WHERE id=? AND estado='pendiente'", (bid,))
        if cur.rowcount != 1:
            return None
        return con.execute("SELECT * FROM borradores WHERE id=?", (bid,)).fetchone()


def cerrar_borrador(bid: int, estado: str) -> None:
    """estado: enviado | descartado | pendiente (devuelve a la cola si falló el envío)."""
    with conectar() as con:
        con.execute("UPDATE borradores SET estado=? WHERE id=?", (estado, bid))


# --- Propuestas sobre la Capa 1 -------------------------------------------------------

def crear_propuesta(tipo: str, datos: dict[str, Any], origen: str = "") -> int:
    """tipo: agregar_pendiente {texto} | cerrar_pendiente {ol_id, texto, motivo}."""
    with conectar() as con:
        cur = con.execute(
            "INSERT INTO propuestas (tipo, datos, origen, creado) VALUES (?,?,?,?)",
            (tipo, json.dumps(datos, ensure_ascii=False), origen, _ahora()),
        )
        return int(cur.lastrowid)


def propuestas_pendientes() -> list[dict[str, Any]]:
    with conectar() as con:
        filas = con.execute("SELECT * FROM propuestas WHERE estado='pendiente' ORDER BY id").fetchall()
    return [{**dict(f), "datos": json.loads(f["datos"])} for f in filas]


def tomar_propuesta(pid: int) -> dict[str, Any] | None:
    with conectar() as con:
        cur = con.execute("UPDATE propuestas SET estado='aplicando' WHERE id=? AND estado='pendiente'", (pid,))
        if cur.rowcount != 1:
            return None
        f = con.execute("SELECT * FROM propuestas WHERE id=?", (pid,)).fetchone()
    return {**dict(f), "datos": json.loads(f["datos"])}


def cerrar_propuesta(pid: int, estado: str) -> None:
    """estado: aceptada | rechazada | pendiente."""
    with conectar() as con:
        con.execute("UPDATE propuestas SET estado=? WHERE id=?", (estado, pid))

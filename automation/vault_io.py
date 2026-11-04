"""Único punto de escritura de la automatización sobre el vault.

Garantías:
1. Bloqueo por archivo entre procesos (archivo .lock con creación exclusiva).
2. Escritura atómica: se escribe un temporal y se reemplaza con os.replace.
3. Toda escritura queda en meta/log.md.
4. Commit automático en git por lote, para poder revertir (`git revert`).
5. La Capa 1 (meta/, salvo el log) y el resto del vault solo se escriben con aprobado=True,
   que se usa únicamente cuando el administrador aprobó una propuesta explícita.

Uso:
    with vault_io.lote("Audio de WhatsApp procesado"):
        vault_io.anexar("journal/2026-10-27.md", "...", motivo="Nota de voz", plantilla=...)
"""

from __future__ import annotations

import contextlib
import datetime as dt
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable, Iterator

RAIZ = Path(os.getenv("VAULT_RAIZ", Path(__file__).resolve().parent.parent)).resolve()
LOG_REL = "meta/log.md"

# Rutas que la automatización puede escribir sin aprobación
ESCRITURA_LIBRE = ("journal/", "sources/reuniones/", "sources/audio/", "inbox/", LOG_REL)

_local = threading.local()
_lock_git = threading.Lock()


class ErrorVault(Exception):
    pass


def _ruta_segura(ruta_rel: str) -> Path:
    ruta_rel = ruta_rel.replace("\\", "/").lstrip("/")
    ruta = (RAIZ / ruta_rel).resolve()
    if not ruta.is_relative_to(RAIZ):
        raise ErrorVault(f"Ruta fuera del vault: {ruta_rel}")
    return ruta


def _permitida(ruta_rel: str, aprobado: bool) -> bool:
    ruta_rel = ruta_rel.replace("\\", "/").lstrip("/")
    return aprobado or any(ruta_rel == p or ruta_rel.startswith(p) for p in ESCRITURA_LIBRE)


@contextlib.contextmanager
def bloqueo(ruta: Path, timeout: float = 15.0, caducidad: float = 120.0) -> Iterator[None]:
    """Bloqueo entre procesos con un archivo .lock creado en modo exclusivo."""
    lock = ruta.with_name(ruta.name + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    inicio = time.monotonic()
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except (FileExistsError, PermissionError):
            # Un .lock viejo es de un proceso que murió a mitad de escritura
            try:
                if time.time() - lock.stat().st_mtime > caducidad:
                    lock.unlink(missing_ok=True)
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() - inicio > timeout:
                raise ErrorVault(f"Timeout esperando el bloqueo de {ruta.name}")
            time.sleep(0.05)
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def leer(ruta_rel: str, max_chars: int | None = None) -> str:
    ruta = _ruta_segura(ruta_rel)
    if not ruta.exists():
        return ""
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    return texto[:max_chars] if max_chars else texto


def _escribir_atomico(ruta: Path, contenido: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_name(f".{ruta.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(contenido)
        f.flush()
        os.fsync(f.fileno())
    # En Windows, os.replace falla si otro proceso (Obsidian, el indexador) tiene el archivo abierto
    for intento in range(20):
        try:
            os.replace(tmp, ruta)
            return
        except PermissionError:
            if intento == 19:
                tmp.unlink(missing_ok=True)
                raise
            time.sleep(0.05 * (intento + 1))


def registrar_log(accion: str, archivo: str, detalle: str) -> None:
    """Agrega una línea a meta/log.md: `AAAA-MM-DD HH:MM | acción | archivo | detalle`."""
    ruta = _ruta_segura(LOG_REL)
    detalle = " ".join(str(detalle).split())[:300]
    linea = f"{dt.datetime.now():%Y-%m-%d %H:%M} | {accion} | {archivo} | {detalle}\n"
    try:
        with bloqueo(ruta):
            actual = ruta.read_text(encoding="utf-8") if ruta.exists() else ""
            if actual and not actual.endswith("\n"):
                actual += "\n"
            _escribir_atomico(ruta, actual + linea)
        _marcar_en_lote(LOG_REL)
    except Exception as e:  # el log nunca debe tumbar el flujo principal
        print(f"[WARN] No se pudo escribir en meta/log.md: {e}", flush=True)


def escribir(
    ruta_rel: str,
    transformar: Callable[[str], str],
    motivo: str,
    accion: str = "cambio",
    aprobado: bool = False,
) -> None:
    """Lee el archivo bajo bloqueo, aplica `transformar` y lo reemplaza de forma atómica."""
    if not _permitida(ruta_rel, aprobado):
        raise ErrorVault(f"Escritura no permitida sin aprobación: {ruta_rel}")
    ruta = _ruta_segura(ruta_rel)
    with bloqueo(ruta):
        actual = ruta.read_text(encoding="utf-8", errors="replace") if ruta.exists() else ""
        nuevo = transformar(actual)
        if nuevo == actual:
            return
        _escribir_atomico(ruta, nuevo)
    _marcar_en_lote(ruta_rel)
    registrar_log(accion, ruta_rel, motivo)


def anexar(ruta_rel: str, texto: str, motivo: str, plantilla: str = "", accion: str = "cambio", aprobado: bool = False) -> None:
    """Agrega `texto` al final; si el archivo no existe, lo crea con `plantilla`."""
    def _t(actual: str) -> str:
        base = actual or plantilla
        if base and not base.endswith("\n"):
            base += "\n"
        return base + texto
    escribir(ruta_rel, _t, motivo, accion=accion, aprobado=aprobado)


def crear(ruta_rel: str, contenido: str, motivo: str, accion: str = "cambio", aprobado: bool = False) -> str:
    """Crea un archivo nuevo sin pisar uno existente: agrega sufijo -2, -3... si hace falta."""
    ruta = _ruta_segura(ruta_rel)
    base, ext = ruta.stem, ruta.suffix
    n = 1
    while ruta.exists():
        n += 1
        ruta = ruta.with_name(f"{base}-{n}{ext}")
    final_rel = ruta.relative_to(RAIZ).as_posix()
    escribir(final_rel, lambda _: contenido, motivo, accion=accion, aprobado=aprobado)
    return final_rel


# --- Git: commit automático por lote -------------------------------------------------

def _marcar_en_lote(ruta_rel: str) -> None:
    rutas = getattr(_local, "rutas", None)
    if rutas is not None:
        rutas.add(ruta_rel)
    else:
        commit({ruta_rel}, f"Automatización: {ruta_rel}")


@contextlib.contextmanager
def lote(motivo: str) -> Iterator[None]:
    """Agrupa todas las escrituras del bloque en un solo commit."""
    anidado = getattr(_local, "rutas", None) is not None
    if anidado:
        yield
        return
    _local.rutas = set()
    try:
        yield
    finally:
        rutas, _local.rutas = _local.rutas, None
        if rutas:
            commit(rutas, motivo)


def commit(rutas: set[str], mensaje: str) -> bool:
    if os.getenv("VAULT_AUTO_COMMIT", "1") == "0" or not (RAIZ / ".git").exists():
        return False
    with _lock_git, bloqueo(RAIZ / ".git" / "vault-auto"):
        try:
            ignoradas = subprocess.run(
                ["git", "check-ignore", "--stdin"], cwd=RAIZ, input="\n".join(rutas),
                capture_output=True, text=True, timeout=30,
            ).stdout.split()
            rutas = {r for r in rutas if r not in ignoradas}
            if not rutas:
                return False
            subprocess.run(["git", "add", "--", *sorted(rutas)], cwd=RAIZ, check=True, capture_output=True, timeout=30)
            r = subprocess.run(
                ["git", "commit", "-q", "-m", f"[auto] {mensaje}", "--", *sorted(rutas)],
                cwd=RAIZ, capture_output=True, text=True, timeout=30,
            )
            return r.returncode == 0
        except Exception as e:
            print(f"[WARN] Commit automático falló: {e}", flush=True)
            return False

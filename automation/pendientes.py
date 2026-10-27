"""Pendientes de meta/open-loops.md con IDs estables (`- [ ] [OL-012] texto`).

La automatización nunca edita open-loops.md por su cuenta: crea propuestas en state.db
(`cola.crear_propuesta`) y solo se aplican cuando el administrador responde `Aceptar N`.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Any

import cola
import vault_io

OPEN_LOOPS = "meta/open-loops.md"
RE_ABIERTO = re.compile(r"^- \[ \] (?:\[(OL-\d{3,})\] )?(.*)$")
RE_ID = re.compile(r"\[OL-(\d{3,})\]")


def _siguiente_id(texto: str) -> int:
    nums = [int(n) for n in RE_ID.findall(texto)]
    return max(nums, default=0) + 1


def asignar_ids(texto: str) -> str:
    """Da un ID a cada pendiente abierto que no lo tenga. Idempotente."""
    n = _siguiente_id(texto)
    salida = []
    for linea in texto.splitlines(keepends=True):
        m = RE_ABIERTO.match(linea.rstrip("\r\n"))
        if m and not m.group(1):
            fin = linea[len(linea.rstrip("\r\n")):]
            linea = f"- [ ] [OL-{n:03d}] {m.group(2)}{fin}"
            n += 1
        salida.append(linea)
    return "".join(salida)


def abiertos() -> list[dict[str, str]]:
    res = []
    for linea in vault_io.leer(OPEN_LOOPS).splitlines():
        m = RE_ABIERTO.match(linea)
        if m and m.group(1):
            res.append({"id": m.group(1), "texto": m.group(2)})
    return res


def _palabras(t: str) -> set[str]:
    return {p for p in re.findall(r"\w+", t.lower()) if len(p) > 3}


def candidato_para(tarea_hecha: str) -> dict[str, str] | None:
    """Pendiente abierto que más se parece a lo reportado como hecho (solo para sugerir)."""
    objetivo = _palabras(tarea_hecha)
    if not objetivo:
        return None
    mejor, puntaje = None, 0.0
    for p in abiertos():
        comunes = objetivo & _palabras(p["texto"])
        score = len(comunes) / len(objetivo)
        if len(comunes) >= 2 and score > puntaje:
            mejor, puntaje = p, score
    return mejor if puntaje >= 0.5 else None


def proponer_desde_analisis(analisis: dict[str, Any], origen: str) -> list[int]:
    """Convierte lo que extrajo el LLM en propuestas pendientes de aprobación."""
    ids = []
    for texto in analisis.get("compromisos_nuevos") or []:
        if str(texto).strip():
            ids.append(cola.crear_propuesta("agregar_pendiente", {"texto": str(texto).strip()}, origen))
    for hecho in analisis.get("tareas_completadas") or []:
        c = candidato_para(str(hecho))
        if c:
            ids.append(cola.crear_propuesta("cerrar_pendiente", {"ol_id": c["id"], "texto": c["texto"], "motivo": str(hecho)}, origen))
    for pid in ids:
        vault_io.registrar_log("PROPUESTA", OPEN_LOOPS, f"Propuesta #{pid} creada desde {origen}")
    return ids


def describir(p: dict[str, Any]) -> str:
    d = p["datos"]
    if p["tipo"] == "agregar_pendiente":
        return f"#{p['id']} ➕ Agregar pendiente: \"{d['texto']}\""
    return f"#{p['id']} ✅ Cerrar {d['ol_id']}: \"{d['texto']}\" (porque: {d['motivo']})"


def aplicar(pid: int) -> str:
    """Aplica una propuesta aprobada por el administrador."""
    p = cola.tomar_propuesta(pid)
    if not p:
        return f"⚠️ No hay propuesta pendiente #{pid}."
    hoy = dt.date.today().isoformat()
    d = p["datos"]
    try:
        if p["tipo"] == "agregar_pendiente":
            def _agregar(texto: str) -> str:
                texto = asignar_ids(texto)
                item = f"- [ ] [OL-{_siguiente_id(texto):03d}] {d['texto']} (vía WhatsApp, desde {hoy})\n"
                lineas = texto.splitlines(keepends=True)
                idx = next((i for i, l in enumerate(lineas) if l.startswith("## Cerrados")), len(lineas))
                # insertar antes de la línea en blanco que precede a "## Cerrados"
                while idx > 0 and not lineas[idx - 1].strip():
                    idx -= 1
                if idx > 0 and not lineas[idx - 1].endswith("\n"):
                    lineas[idx - 1] += "\n"
                lineas.insert(idx, item)
                return "".join(lineas)
            vault_io.escribir(OPEN_LOOPS, _agregar, f"Propuesta #{pid} aceptada: agregar pendiente", accion="TASK_ADD", aprobado=True)
        else:
            ol_id = d["ol_id"]
            encontrado = False

            def _cerrar(texto: str) -> str:
                nonlocal encontrado
                salida = []
                for linea in texto.splitlines(keepends=True):
                    m = RE_ABIERTO.match(linea.rstrip("\r\n"))
                    if m and m.group(1) == ol_id:
                        encontrado = True
                        linea = f"- [x] [{ol_id}] ~~{m.group(2)}~~ → cerrado {hoy}\n"
                    salida.append(linea)
                return "".join(salida)
            vault_io.escribir(OPEN_LOOPS, _cerrar, f"Propuesta #{pid} aceptada: cerrar {ol_id}", accion="TASK_DONE", aprobado=True)
            if not encontrado:
                cola.cerrar_propuesta(pid, "rechazada")
                return f"⚠️ {ol_id} ya no está abierto; descarté la propuesta #{pid}."
    except Exception:
        cola.cerrar_propuesta(pid, "pendiente")
        raise
    cola.cerrar_propuesta(pid, "aceptada")
    return f"✅ Aplicada: {describir(p)}"


def rechazar(pid: int) -> str:
    p = cola.tomar_propuesta(pid)
    if not p:
        return f"⚠️ No hay propuesta pendiente #{pid}."
    cola.cerrar_propuesta(pid, "rechazada")
    vault_io.registrar_log("PROPUESTA_RECHAZADA", OPEN_LOOPS, f"Propuesta #{pid} rechazada")
    return f"🗑️ Propuesta #{pid} rechazada."

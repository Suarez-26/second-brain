"""Índice de búsqueda local del vault (SQLite FTS5, ranking BM25).

- Fragmenta cada nota por encabezados (## / ###) en bloques de hasta ~1500 caracteres.
- Guarda metadatos del frontmatter como filtros: capa, contexto, tipo, calidad (columna `estado`), fecha.
- Incremental: solo reindexa archivos cuya fecha de modificación cambió.
- Sin red: el contenido del vault no sale del equipo.

Uso:
    python automation/indice.py               # actualizar índice
    python automation/indice.py --reconstruir # desde cero
    python automation/indice.py "becas floridablanca" --contexto campuslands
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

RAIZ = Path(os.getenv("VAULT_RAIZ", Path(__file__).resolve().parent.parent)).resolve()
DB_PATH = Path(os.getenv("VAULT_INDEX_DB", Path(__file__).resolve().parent / "index.db"))

EXCLUIR_DIRS = {".git", ".obsidian", ".agents", ".claude", "ai-brain-starter", "automation", "node_modules", ".chrome_profile"}
# Corpus extraído en masa: se indexa, pero como 'crudo' (fuera de los resultados por defecto)
DIRS_CRUDOS = ("diego_investigacion/", "diego_instagram/", "inbox/", "sources/", "investigacion/campuslands/corpus_youtube_podcasts/")
MAX_BLOQUE = 1500

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS archivos (ruta TEXT PRIMARY KEY, mtime REAL NOT NULL);
CREATE VIRTUAL TABLE IF NOT EXISTS bloques USING fts5(
    ruta UNINDEXED, titulo, seccion, texto,
    capa UNINDEXED, contexto UNINDEXED, tipo UNINDEXED, estado UNINDEXED, fecha UNINDEXED,
    tokenize = "unicode61 remove_diacritics 2"
);
"""


def conectar() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH, timeout=15)
    con.row_factory = sqlite3.Row
    con.executescript(_ESQUEMA)
    return con


def frontmatter(texto: str) -> tuple[dict[str, str], str]:
    if not texto.startswith("---"):
        return {}, texto
    fin = texto.find("\n---", 3)
    if fin == -1:
        return {}, texto
    meta = {}
    for linea in texto[3:fin].splitlines():
        if ":" in linea and not linea.startswith((" ", "-")):
            k, v = linea.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    return meta, texto[fin + 4:].lstrip("\n")


def capa_de(ruta: str) -> int:
    if ruta.startswith("meta/") or ruta == "CLAUDE.md":
        return 1
    if ruta.startswith(("areas/", "journal/resumenes/")):
        return 2
    return 3


def metadatos(ruta: str, meta: dict[str, str]) -> dict[str, Any]:
    estado = meta.get("calidad") or ("crudo" if ruta.startswith(DIRS_CRUDOS) else "sin-calificar")
    return {
        "capa": capa_de(ruta),
        "contexto": (meta.get("contexto") or "").split("|")[0].strip() or "sin-contexto",
        "tipo": meta.get("tipo", ""),
        "estado": estado,
        "fecha": meta.get("fecha", ""),
    }


def fragmentar(cuerpo: str) -> list[tuple[str, str]]:
    """Devuelve [(seccion, texto)] cortando por encabezados y por tamaño."""
    partes, seccion, buffer = [], "", []

    def volcar() -> None:
        texto = "\n".join(buffer).strip()
        while texto:
            corte = texto[:MAX_BLOQUE]
            if len(texto) > MAX_BLOQUE and "\n" in corte:
                corte = corte[: corte.rfind("\n")]
            partes.append((seccion, corte.strip()))
            texto = texto[len(corte):].strip()

    for linea in cuerpo.splitlines():
        if re.match(r"^#{2,3}\s", linea):
            volcar()
            buffer = []
            seccion = linea.lstrip("#").strip()
        else:
            buffer.append(linea)
    volcar()
    return [p for p in partes if p[1]]


def archivos_md() -> list[Path]:
    salida = []
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if d not in EXCLUIR_DIRS]
        salida += [Path(dp) / f for f in fn if f.endswith(".md") and not f.startswith("_plantilla")]
    return salida


def actualizar(reconstruir: bool = False) -> dict[str, int]:
    con = conectar()
    if reconstruir:
        con.execute("DELETE FROM bloques")
        con.execute("DELETE FROM archivos")
    previos = {r["ruta"]: r["mtime"] for r in con.execute("SELECT ruta, mtime FROM archivos")}
    actuales, cambiados = {}, 0
    for p in archivos_md():
        ruta = p.relative_to(RAIZ).as_posix()
        mtime = p.stat().st_mtime
        actuales[ruta] = mtime
        if previos.get(ruta) == mtime:
            continue
        texto = p.read_text(encoding="utf-8", errors="replace")
        meta, cuerpo = frontmatter(texto)
        md = metadatos(ruta, meta)
        m_titulo = re.search(r"^#\s+(.+)$", cuerpo, re.MULTILINE)
        titulo = m_titulo.group(1).strip() if m_titulo else p.stem
        con.execute("DELETE FROM bloques WHERE ruta=?", (ruta,))
        con.executemany(
            "INSERT INTO bloques (ruta, titulo, seccion, texto, capa, contexto, tipo, estado, fecha) VALUES (?,?,?,?,?,?,?,?,?)",
            [(ruta, titulo, sec, txt, md["capa"], md["contexto"], md["tipo"], md["estado"], md["fecha"]) for sec, txt in fragmentar(cuerpo)],
        )
        con.execute("INSERT OR REPLACE INTO archivos (ruta, mtime) VALUES (?,?)", (ruta, mtime))
        cambiados += 1
    borrados = [r for r in previos if r not in actuales]
    for ruta in borrados:
        con.execute("DELETE FROM bloques WHERE ruta=?", (ruta,))
        con.execute("DELETE FROM archivos WHERE ruta=?", (ruta,))
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM archivos").fetchone()[0]
    con.close()
    return {"archivos": total, "reindexados": cambiados, "eliminados": len(borrados)}


def _consulta_fts(consulta: str, operador: str) -> str:
    terminos = [t for t in re.findall(r"\w+", consulta.lower()) if len(t) > 1]
    return f" {operador} ".join(f'"{t}"*' if len(t) > 3 else f'"{t}"' for t in terminos)


def buscar(
    consulta: str,
    contexto: str | None = None,
    capa: int | None = None,
    incluir_crudo: bool = False,
    limite: int = 8,
) -> list[dict[str, Any]]:
    """Busca primero con todos los términos (AND) y, si no hay resultados, con cualquiera (OR)."""
    actualizar()
    con = conectar()
    filtros, params = [], []
    if contexto:
        filtros.append("contexto = ?")
        params.append(contexto)
    if capa:
        filtros.append("capa = ?")
        params.append(capa)
    if not incluir_crudo:
        filtros.append("estado != 'crudo'")
    where = (" AND " + " AND ".join(filtros)) if filtros else ""
    resultados: list[dict[str, Any]] = []
    for operador in ("AND", "OR"):
        q = _consulta_fts(consulta, operador)
        if not q:
            break
        filas = con.execute(
            f"""SELECT ruta, titulo, seccion, capa, contexto, estado, fecha,
                       snippet(bloques, 3, '«', '»', ' … ', 24) AS fragmento,
                       bm25(bloques, 0, 6.0, 3.0, 1.0) AS puntaje
                FROM bloques WHERE bloques MATCH ?{where}
                ORDER BY capa ASC, puntaje ASC LIMIT ?""",
            [q, *params, limite * 3],
        ).fetchall()
        vistos = set()
        for f in filas:
            clave = (f["ruta"], f["seccion"])
            if clave in vistos:
                continue
            vistos.add(clave)
            resultados.append(dict(f))
        if resultados:
            break
    con.close()
    # Las capas bajas primero, pero sin enterrar un resultado mucho más relevante
    resultados.sort(key=lambda r: (r["puntaje"] + (r["capa"] - 1) * 2.0))
    return resultados[:limite]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("consulta", nargs="?")
    ap.add_argument("--reconstruir", action="store_true")
    ap.add_argument("--contexto")
    ap.add_argument("--capa", type=int)
    ap.add_argument("--crudo", action="store_true", help="incluir corpus crudo")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not args.consulta:
        print(actualizar(args.reconstruir))
        return 0
    for r in buscar(args.consulta, args.contexto, args.capa, args.crudo):
        print(f"[C{r['capa']} {r['contexto']}/{r['estado']}] {r['ruta']} § {r['seccion'] or r['titulo']}\n    {r['fragmento']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

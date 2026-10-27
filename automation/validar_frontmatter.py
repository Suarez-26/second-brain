"""Valida el frontmatter de las notas del vault contra el esquema de CLAUDE.md.

Esquema:
    fecha: AAAA-MM-DD                         (obligatorio)
    contexto: personal | campuslands | otro   (obligatorio en people/, projects/, organizaciones/, areas/)
    tipo: ...                                 (recomendado)
    estado: texto libre del flujo de trabajo  (opcional: activo, borrador...)
    calidad: crudo | resumido | verificado    (opcional: confiabilidad del contenido)
    fuente: [[nota]] o URL                    (opcional)

Solo reporta: no reescribe archivos. Los corpus crudos (diego_*, inbox/, sources/) se omiten
salvo con --todo.

    python automation/validar_frontmatter.py
"""

from __future__ import annotations

import argparse
import re
import sys

import indice

CONTEXTOS = {"personal", "campuslands", "otro"}
CALIDADES = {"crudo", "resumido", "verificado"}
EXIGEN_CONTEXTO = ("people/", "projects/", "organizaciones/", "areas/", "prospectos/")


def validar(ruta: str, texto: str) -> list[str]:
    problemas = []
    meta, _ = indice.frontmatter(texto)
    if not meta:
        return ["sin frontmatter"]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("fecha", "")):
        problemas.append(f"fecha inválida o ausente ({meta.get('fecha', '')!r})")
    ctx = meta.get("contexto")
    if ctx is None:
        if ruta.startswith(EXIGEN_CONTEXTO):
            problemas.append("falta contexto")
    elif ctx not in CONTEXTOS:
        problemas.append(f"contexto fuera del esquema ({ctx!r})")
    if meta.get("calidad") and meta["calidad"] not in CALIDADES:
        problemas.append(f"calidad fuera del esquema ({meta['calidad']!r})")
    return problemas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--todo", action="store_true", help="incluir corpus crudos")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    total, con_problemas = 0, 0
    for p in sorted(indice.archivos_md()):
        ruta = p.relative_to(indice.RAIZ).as_posix()
        if not args.todo and ruta.startswith(indice.DIRS_CRUDOS):
            continue
        if p.name == "CLAUDE.md" or (p.name == "README.md" and "/" not in ruta):
            continue
        total += 1
        problemas = validar(ruta, p.read_text(encoding="utf-8", errors="replace"))
        if problemas:
            con_problemas += 1
            print(f"{ruta}: {'; '.join(problemas)}")
    print(f"\n{con_problemas} de {total} notas con problemas.")
    return 1 if con_problemas else 0


if __name__ == "__main__":
    sys.exit(main())

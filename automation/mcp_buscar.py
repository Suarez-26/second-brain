"""Servidor MCP de búsqueda en el vault (solo lectura).

Herramientas:
- buscar(consulta, contexto?, capa?, incluir_crudo?, limite?) -> fragmentos con ruta y capa.
- leer_nota(ruta, max_chars?) -> contenido de una nota del vault.
- estado_pendientes() -> borradores y propuestas que esperan aprobación.

Registrado en .mcp.json como `second-brain-buscar`. Úsalo después de leer la Capa 1:
primero buscar(), luego leer_nota() solo de lo que haga falta.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as MCPServer

import cola  # noqa: E402
import indice  # noqa: E402

RAIZ = indice.RAIZ
mcp = MCPServer("second-brain-buscar")


@mcp.tool()
def buscar(consulta: str, contexto: str | None = None, capa: int | None = None,
           incluir_crudo: bool = False, limite: int = 8) -> list[dict]:
    """Busca en el vault por palabras clave (sin importar acentos), con ranking BM25.

    contexto: personal | campuslands | otro. capa: 1 (meta), 2 (áreas y resúmenes), 3 (archivo).
    incluir_crudo: True para incluir el corpus extraído en masa (diego_investigacion, inbox, sources).
    """
    return [
        {k: r[k] for k in ("ruta", "titulo", "seccion", "capa", "contexto", "estado", "fecha", "fragmento")}
        for r in indice.buscar(consulta, contexto, capa, incluir_crudo, max(1, min(limite, 25)))
    ]


@mcp.tool()
def leer_nota(ruta: str, max_chars: int = 12000) -> str:
    """Lee una nota del vault por su ruta relativa (por ejemplo `areas/campuslands.md`)."""
    p = (RAIZ / ruta).resolve()
    if not p.is_relative_to(RAIZ) or p.suffix.lower() not in (".md", ".txt") or ".env" in p.name:
        return "Ruta no permitida: solo notas .md/.txt dentro del vault."
    if not p.exists():
        return f"No existe: {ruta}"
    return p.read_text(encoding="utf-8", errors="replace")[:max_chars]


@mcp.tool()
def estado_pendientes() -> dict:
    """Borradores de respuesta a terceros y propuestas sobre open-loops que esperan aprobación."""
    return {
        "borradores": [dict(b) for b in cola.borradores_pendientes()],
        "propuestas": cola.propuestas_pendientes(),
        "cola_mensajes": cola.resumen_cola(),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")

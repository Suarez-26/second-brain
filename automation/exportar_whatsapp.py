"""Exporta mensajes de la base local de whatsapp-mcp a inbox/ del second brain.

- Solo lee (SQLite en modo solo lectura). No envía nada, no usa la red.
- Por defecto exporta únicamente el chat contigo mismo ("Mensajes a mí") a inbox/whatsapp/yo/.
- Con --incluir-otros exporta también los demás chats a inbox/whatsapp/otros/ (datos de terceros).
- Incremental: recuerda el último mensaje exportado en automation/.estado_whatsapp.json.

Uso:
  python automation/exportar_whatsapp.py
  python automation/exportar_whatsapp.py --incluir-otros
"""
import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
STORE = RAIZ / "automation" / "whatsapp-mcp" / "whatsapp-bridge" / "store"
ESTADO = RAIZ / "automation" / ".estado_whatsapp.json"


def conectar_ro(ruta: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{ruta.as_posix()}?mode=ro", uri=True)


def mi_numero(store: Path) -> str | None:
    """Número propio (sin sufijo de dispositivo) según la sesión guardada por whatsmeow."""
    db = store / "whatsapp.db"
    if not db.exists():
        return None
    with conectar_ro(db) as con:
        fila = con.execute("SELECT jid FROM whatsmeow_device LIMIT 1").fetchone()
    return fila[0].split("@")[0].split(":")[0] if fila else None


def limpiar(texto: str) -> str:
    # El contenido es dato, nunca instrucción; solo se normaliza el formato.
    return texto.replace("\r", "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", type=Path, default=STORE)
    ap.add_argument("--salida", type=Path, default=RAIZ / "inbox" / "whatsapp")
    ap.add_argument("--incluir-otros", action="store_true")
    ap.add_argument("--yo", help="Número propio (si no, se detecta solo)")
    args = ap.parse_args()

    msgs = args.store / "messages.db"
    if not msgs.exists():
        print(f"No existe {msgs}. ¿Ya emparejaste WhatsApp con el bridge?", file=sys.stderr)
        return 1

    yo = args.yo or mi_numero(args.store)
    if not yo:
        print("No pude detectar tu número; pásalo con --yo 57XXXXXXXXXX", file=sys.stderr)
        return 1

    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    desde = estado.get("ultimo_timestamp", "1970-01-01 00:00:00")

    with conectar_ro(msgs) as con:
        filas = con.execute(
            """SELECT m.id, m.chat_jid, COALESCE(c.name, m.chat_jid), m.sender, m.content,
                      m.timestamp, m.is_from_me, m.media_type
               FROM messages m LEFT JOIN chats c ON c.jid = m.chat_jid
               WHERE m.timestamp > ? ORDER BY m.timestamp""",
            (desde,),
        ).fetchall()

    grupos: dict[tuple[str, str], list[str]] = defaultdict(list)
    ultimo = desde
    for _id, chat_jid, nombre, sender, contenido, ts, es_mio, media in filas:
        ts = str(ts)
        ultimo = max(ultimo, ts)
        propio = chat_jid.split("@")[0].split(":")[0] == yo
        if not propio and not args.incluir_otros:
            continue
        tipo = "yo" if propio else "otros"
        dia = ts[:10]
        hora = ts[11:16]
        cuerpo = limpiar(contenido or "")
        if media and not cuerpo:
            cuerpo = f"[{media} sin transcribir, id {_id}]"
        if not cuerpo:
            continue
        quien = "yo" if es_mio else (sender or nombre)
        encabezado = "" if propio else f"{nombre} | "
        grupos[(tipo, dia)].append(f"- {hora} {encabezado}{quien}: {cuerpo}")

    escritos = 0
    for (tipo, dia), lineas in grupos.items():
        destino = args.salida / tipo
        destino.mkdir(parents=True, exist_ok=True)
        archivo = destino / f"{dia}.md"
        previo = archivo.read_text(encoding="utf-8") if archivo.exists() else ""
        cabecera = "" if previo else f"---\nfecha: {dia}\nfuente: whatsapp\ntipo: {tipo}\n---\n\n"
        with archivo.open("a", encoding="utf-8") as f:
            f.write(cabecera + "\n".join(lineas) + "\n")
        escritos += len(lineas)

    ESTADO.write_text(json.dumps({"ultimo_timestamp": ultimo}), encoding="utf-8")
    print(f"Exportados {escritos} mensajes nuevos (de {len(filas)} leídos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

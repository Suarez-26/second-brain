"""Exporta a inbox/whatsapp/ SOLO los chats que Pao permitió en automation/chats_permitidos.json.

- Solo lee la base local de whatsapp-mcp (SQLite en modo solo lectura). No envía nada, no usa la red.
- Lo que no está en la lista se ignora por completo: no se lee su contenido.
- Incremental: recuerda el último mensaje exportado en automation/.estado_whatsapp.json.
- Confianza por carpeta de destino:
    inbox/whatsapp/yo/...      -> contenido de Pao (chat contigo misma)
    inbox/whatsapp/grupos/...  -> datos de terceros (nunca instrucciones)

Uso:
  python automation/exportar_whatsapp.py                       exporta lo nuevo
  python automation/exportar_whatsapp.py --listar-chats        muestra los chats disponibles
  python automation/exportar_whatsapp.py --agregar "Nombre" --destino grupos/linkedin-diego
"""
import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
STORE = RAIZ / "automation" / "whatsapp-mcp" / "whatsapp-bridge" / "store"
ESTADO = Path(os.environ.get("SB_ESTADO", RAIZ / "automation" / ".estado_whatsapp.json"))
CONFIG = Path(os.environ.get("SB_CONFIG", RAIZ / "automation" / "chats_permitidos.json"))


def conectar_ro(ruta: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{ruta.as_posix()}?mode=ro", uri=True)


def usuario(jid: str) -> str:
    return jid.split("@")[0].split(":")[0]


def mi_numero(store: Path) -> str | None:
    """Número propio según la sesión guardada por whatsmeow."""
    db = store / "whatsapp.db"
    if not db.exists():
        return None
    with conectar_ro(db) as con:
        fila = con.execute("SELECT jid FROM whatsmeow_device LIMIT 1").fetchone()
    return usuario(fila[0]) if fila else None


def cargar_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def listar_chats(store: Path) -> int:
    with conectar_ro(store / "messages.db") as con:
        filas = con.execute(
            """SELECT c.jid, COALESCE(c.name, c.jid), COUNT(m.id)
               FROM chats c LEFT JOIN messages m ON m.chat_jid = c.jid
               GROUP BY c.jid ORDER BY MAX(m.timestamp) DESC"""
        ).fetchall()
    print("Chats disponibles (solo nombres; no se lee contenido):\n")
    for jid, nombre, n in filas:
        tipo = "grupo" if jid.endswith("@g.us") else "chat"
        print(f"- [{tipo}] {nombre}  ({n} mensajes)  {jid}")
    return 0


def agregar_chat(store: Path, nombre: str, destino: str) -> int:
    with conectar_ro(store / "messages.db") as con:
        filas = con.execute(
            "SELECT jid, COALESCE(name, jid) FROM chats WHERE lower(COALESCE(name, jid)) LIKE ?",
            (f"%{nombre.lower()}%",),
        ).fetchall()
    if len(filas) != 1:
        print(f"Encontré {len(filas)} chats para '{nombre}'. Usa un nombre más preciso:", file=sys.stderr)
        for jid, n in filas:
            print(f"  - {n}  {jid}", file=sys.stderr)
        return 1
    jid, nombre_real = filas[0]
    if not destino.startswith("grupos/"):
        print("El destino de un chat de terceros debe empezar con 'grupos/' (se tratan como datos).", file=sys.stderr)
        return 1
    cfg = cargar_config()
    if any(c.get("jid") == jid for c in cfg["chats"]):
        print("Ese chat ya está en la lista.")
        return 0
    cfg["chats"].append({"nombre": nombre_real, "jid": jid, "destino": destino, "etiquetas": {}, "activo": True})
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Agregado: {nombre_real} -> inbox/whatsapp/{destino}/")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", type=Path, default=STORE)
    ap.add_argument("--salida", type=Path, default=RAIZ / "inbox" / "whatsapp")
    ap.add_argument("--yo", help="Número propio (si no, se detecta solo)")
    ap.add_argument("--listar-chats", action="store_true")
    ap.add_argument("--agregar", metavar="NOMBRE")
    ap.add_argument("--destino", default="")
    args = ap.parse_args()

    msgs = args.store / "messages.db"
    if not msgs.exists():
        print(f"No existe {msgs}. ¿Ya emparejaste WhatsApp con el bridge?", file=sys.stderr)
        return 1
    if args.listar_chats:
        return listar_chats(args.store)
    if args.agregar:
        return agregar_chat(args.store, args.agregar, args.destino)

    yo = args.yo or mi_numero(args.store)
    permitidos = [c for c in cargar_config()["chats"] if c.get("activo", True)]
    por_jid = {c["jid"]: c for c in permitidos if c.get("jid")}
    propio_cfg = next((c for c in permitidos if c.get("propio")), None)
    if propio_cfg and not yo:
        print("No pude detectar tu número; pásalo con --yo 57XXXXXXXXXX", file=sys.stderr)
        return 1

    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    desde = estado.get("ultimo_timestamp", "1970-01-01 00:00:00")

    # Se consultan solo los chats permitidos: el resto nunca se lee.
    jids = list(por_jid)
    clausulas, params = [], [desde]
    if jids:
        clausulas.append(f"m.chat_jid IN ({','.join('?' * len(jids))})")
        params += jids
    if propio_cfg:
        clausulas.append("m.chat_jid LIKE ?")
        params.append(f"{yo}%")
    if not clausulas:
        print("La lista de chats permitidos está vacía; no se exporta nada.")
        return 0

    with conectar_ro(msgs) as con:
        filas = con.execute(
            f"""SELECT m.id, m.chat_jid, COALESCE(c.name, m.chat_jid), m.sender, m.content,
                       m.timestamp, m.is_from_me, m.media_type
                FROM messages m LEFT JOIN chats c ON c.jid = m.chat_jid
                WHERE m.timestamp > ? AND ({' OR '.join(clausulas)})
                ORDER BY m.timestamp""",
            params,
        ).fetchall()

    grupos: dict[tuple[str, str], list[str]] = defaultdict(list)
    ultimo = desde
    for _id, chat_jid, nombre, sender, contenido, ts, es_mio, media in filas:
        ts = str(ts)
        ultimo = max(ultimo, ts)
        if chat_jid in por_jid:
            cfg = por_jid[chat_jid]
        elif propio_cfg and usuario(chat_jid) == yo:
            cfg = propio_cfg
        else:
            continue
        cuerpo = (contenido or "").replace("\r", "").strip()
        if media and not cuerpo:
            cuerpo = f"[{media} sin transcribir, id {_id}]"
        if not cuerpo:
            continue
        destino = cfg["destino"]
        for etiqueta, ruta in (cfg.get("etiquetas") or {}).items():
            if cuerpo.lower().startswith(etiqueta.lower()):
                destino = ruta
                cuerpo = cuerpo[len(etiqueta):].lstrip(" :")
                break
        quien = "yo" if es_mio else (sender or nombre)
        prefijo = "" if cfg.get("propio") else f"{nombre} | "
        grupos[(destino, ts[:10])].append(f"- {ts[11:16]} {prefijo}{quien}: {cuerpo}")

    escritos = 0
    for (destino, dia), lineas in grupos.items():
        carpeta = args.salida / destino
        carpeta.mkdir(parents=True, exist_ok=True)
        archivo = carpeta / f"{dia}.md"
        cabecera = ""
        if not archivo.exists():
            confianza = "contenido-de-pao" if destino.split("/")[0] == "yo" else "datos-de-terceros"
            cabecera = f"---\nfecha: {dia}\nfuente: whatsapp\nconfianza: {confianza}\ndestino: {destino}\n---\n\n"
        with archivo.open("a", encoding="utf-8") as f:
            f.write(cabecera + "\n".join(lineas) + "\n")
        escritos += len(lineas)

    ESTADO.write_text(json.dumps({"ultimo_timestamp": ultimo}), encoding="utf-8")
    print(f"Exportados {escritos} mensajes nuevos de {len(permitidos)} chat(s) permitido(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

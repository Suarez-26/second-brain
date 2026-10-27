import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

BASE_DIR = Path(r"C:\Users\tomas\second-brain")

def tejer_instagram():
    pub_diego = BASE_DIR / "diego_instagram" / "02_publicaciones" / "diego"
    pub_campus = BASE_DIR / "diego_instagram" / "02_publicaciones" / "campuslands"
    trans_dir = BASE_DIR / "diego_instagram" / "05_transcripciones"
    
    count = 0
    # 1. Posts de Diego en Instagram
    for f in pub_diego.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if "## 🔗 Conexiones del Second Brain" in content:
            continue
        
        post_id = f.stem
        # Check transcript
        trans_file = trans_dir / f"{post_id}_transcripcion.md"
        trans_link = f"- **Transcripción Sincronizada:** [[diego_instagram/05_transcripciones/{post_id}_transcripcion|Ver Transcripción]]\n" if trans_file.exists() else ""
        
        # Thematic tagging based on content
        temas = []
        c_lower = content.lower()
        if any(w in c_lower for w in ["ia", "inteligencia artificial", "software", "código", "agente", "algoritmo"]):
            temas.append("[[areas/ia-aplicada-y-futuro-del-trabajo|IA y Futuro del Trabajo]]")
        if any(w in c_lower for w in ["empleo", "salario", "movilidad social", "estrato", "oportunidad", "trabaj"]):
            temas.append("[[areas/movilidad-social|Movilidad Social y Empleo]]")
        if any(w in c_lower for w in ["campus", "camper", "afterwork", "zona franca", "bucaramanga"]):
            temas.append("[[areas/cultura-camper|Cultura Camper]]")
        if not temas:
            temas.append("[[areas/movilidad-social|Movilidad Social]]")
            
        footer = [
            "",
            "---",
            "## 🔗 Conexiones del Second Brain",
            "- **Autor / Entidad:** [[people/diego-tarazona|Diego Tarazona]] | [[areas/campuslands|Campuslands]]",
            "- **Canal y Proyecto:** [[projects/instagram-diego-tarazona|Instagram Diego Tarazona]] | [[instagram/README|Sistema Editorial IG]]",
            f"- **Pilares Temáticos:** {' • '.join(temas)}",
            trans_link.strip() if trans_link else "",
            ""
        ]
        footer_str = "\n".join([l for l in footer if l is not None])
        f.write_text(content.strip() + "\n" + footer_str, encoding="utf-8")
        count += 1
        
    print(f"Posts de Diego en Instagram conectados: {count}")

    # 2. Posts de Campuslands en Instagram
    count_c = 0
    for f in pub_campus.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if "## 🔗 Conexiones del Second Brain" in content:
            continue
            
        post_id = f.stem
        trans_file = trans_dir / f"{post_id}_transcripcion.md"
        trans_link = f"- **Transcripción Sincronizada:** [[diego_instagram/05_transcripciones/{post_id}_transcripcion|Ver Transcripción]]\n" if trans_file.exists() else ""
        
        temas = []
        c_lower = content.lower()
        if any(w in c_lower for w in ["ia", "inteligencia artificial", "software", "código"]):
            temas.append("[[areas/ia-aplicada-y-futuro-del-trabajo|IA y Futuro del Trabajo]]")
        if any(w in c_lower for w in ["empleo", "salario", "carrera", "oportunidad"]):
            temas.append("[[areas/movilidad-social|Movilidad Social]]")
        temas.append("[[areas/cultura-camper|Cultura Camper]]")
            
        footer = [
            "",
            "---",
            "## 🔗 Conexiones del Second Brain",
            "- **Entidad:** [[areas/campuslands|Campuslands]] | [[people/diego-tarazona|Diego Tarazona]]",
            "- **Canal y Proyecto:** [[projects/instagram-diego-tarazona|Instagram Campuslands]]",
            f"- **Pilares Temáticos:** {' • '.join(temas)}",
            trans_link.strip() if trans_link else "",
            ""
        ]
        footer_str = "\n".join([l for l in footer if l is not None])
        f.write_text(content.strip() + "\n" + footer_str, encoding="utf-8")
        count_c += 1

    print(f"Posts de Campuslands conectados: {count_c}")

    # 3. Transcripciones de Instagram
    count_t = 0
    for f in trans_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if "## 🔗 Conexiones del Second Brain" in content:
            continue
        post_id = f.stem.replace("_transcripcion", "")
        # Link back to post
        orig_post = f"[[diego_instagram/02_publicaciones/diego/{post_id}|Ficha {post_id}]]" if (pub_diego / f"{post_id}.md").exists() else f"[[diego_instagram/02_publicaciones/campuslands/{post_id}|Ficha {post_id}]]"
        footer = [
            "",
            "---",
            "## 🔗 Conexiones del Second Brain",
            f"- **Publicación Original:** {orig_post}",
            "- **Entidades:** [[people/diego-tarazona|Diego Tarazona]] • [[areas/campuslands|Campuslands]]",
            "- **Análisis Maestro:** [[diego_instagram/06_analisis_maestro_instagram|06_analisis_maestro_instagram]] • [[diego_instagram/06b_manual_de_estilo_y_patrones_diego|06b_manual_de_estilo]]",
            ""
        ]
        f.write_text(content.strip() + "\n" + "\n".join(footer), encoding="utf-8")
        count_t += 1

    print(f"Transcripciones de Instagram conectadas: {count_t}")

def tejer_linkedin():
    pub_dir = BASE_DIR / "diego_investigacion" / "02_publicaciones"
    trans_dir = BASE_DIR / "diego_investigacion" / "05_transcripciones"
    if not pub_dir.exists():
        return
        
    count = 0
    for f in pub_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if "## 🔗 Conexiones del Second Brain" in content:
            continue
            
        post_id = f.stem
        trans_file = trans_dir / f"{post_id}_transcripcion.md"
        trans_link = f"- **Transcripción:** [[diego_investigacion/05_transcripciones/{post_id}_transcripcion|Ver Transcripción]]\n" if trans_file.exists() else ""
        
        temas = []
        c_lower = content.lower()
        if any(w in c_lower for w in ["ia", "inteligencia artificial", "software", "agente"]):
            temas.append("[[areas/ia-aplicada-y-futuro-del-trabajo|IA y Futuro del Trabajo]]")
        if any(w in c_lower for w in ["empleo", "salario", "movilidad social", "estrato", "talento"]):
            temas.append("[[areas/movilidad-social|Movilidad Social]]")
        if any(w in c_lower for w in ["campuslands", "camper", "bucaramanga", "santander"]):
            temas.append("[[areas/campuslands|Campuslands]]")
        if not temas:
            temas.append("[[areas/movilidad-social|Movilidad Social]]")
            
        footer = [
            "",
            "---",
            "## 🔗 Conexiones del Second Brain",
            "- **Autor / Entidad:** [[people/diego-tarazona|Diego Tarazona]] | [[areas/campuslands|Campuslands]]",
            "- **Proyecto:** [[projects/linkedin-diego-tarazona|LinkedIn Diego Tarazona]] | [[linkedin/README|Sistema Editorial LinkedIn]]",
            f"- **Pilares:** {' • '.join(temas)}",
            trans_link.strip() if trans_link else "",
            ""
        ]
        footer_str = "\n".join([l for l in footer if l is not None])
        f.write_text(content.strip() + "\n" + footer_str, encoding="utf-8")
        count += 1
        
    print(f"Posts de LinkedIn conectados: {count}")

    # Transcripciones de LinkedIn
    count_lt = 0
    if trans_dir.exists():
        for f in trans_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if "## 🔗 Conexiones del Second Brain" in content:
                continue
            post_id = f.stem.replace("_transcripcion", "")
            orig_post = f"[[diego_investigacion/02_publicaciones/{post_id}|Ficha {post_id}]]"
            footer = [
                "",
                "---",
                "## 🔗 Conexiones del Second Brain",
                f"- **Publicación Original:** {orig_post}",
                "- **Entidades:** [[people/diego-tarazona|Diego Tarazona]] • [[areas/campuslands|Campuslands]]",
                "- **Análisis Maestro:** [[diego_investigacion/06_analisis_maestro_diego|06_analisis_maestro_diego]]",
                ""
            ]
            f.write_text(content.strip() + "\n" + "\n".join(footer), encoding="utf-8")
            count_lt += 1
    print(f"Transcripciones de LinkedIn conectadas: {count_lt}")

if __name__ == "__main__":
    tejer_instagram()
    tejer_linkedin()

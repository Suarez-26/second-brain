import glob
import os

def generate_linkedin_moc():
    posts = sorted(glob.glob('diego_investigacion/02_publicaciones/post_[0-9]*.md'))
    destacados = sorted(glob.glob('diego_investigacion/02_publicaciones/post_destacado_*.md'))
    menciones = sorted(glob.glob('diego_investigacion/02_publicaciones/mencion_*.md'))
    campuslands = sorted(glob.glob('diego_investigacion/02_publicaciones/campuslands_*.md'))
    trans = sorted(glob.glob('diego_investigacion/05_transcripciones/*.md'))

    content = []
    content.append('---')
    content.append('tipo: moc')
    content.append('contexto: campuslands')
    content.append('tema: Investigacion Integral Diego Tarazona en LinkedIn')
    content.append('fecha_actualizacion: 2026-10-20')
    content.append('---')
    content.append('')
    content.append('# 🧭 MOC: Investigación Integral Diego Tarazona (LinkedIn)')
    content.append('')
    content.append('Mapa central de contenidos que estructura la extracción exhaustiva de perfil, 337 publicaciones históricas y 83 transcripciones audiovisuales multimodales de [[people/diego-tarazona|Diego Tarazona]] y [[areas/campuslands|Campuslands]].')
    content.append('')
    content.append('## 🌟 Síntesis y Perfil Oficial')
    content.append('- **Análisis Maestro:** [[diego_investigacion/06_analisis_maestro_diego|06_analisis_maestro_diego.md]] (Tesis de agentes IA, horas-agente, cronología de sedes, holding empresarial y contradicciones resueltas).')
    content.append('- **Perfil General:** [[diego_investigacion/01_perfil_general|01_perfil_general.md]]')
    content.append('- **Perfil Campuslands:** [[diego_investigacion/01b_perfil_campuslands|01b_perfil_campuslands.md]]')
    content.append('- **Secciones Extra y Trayectoria:** [[diego_investigacion/01c_perfil_secciones_extra|01c_perfil_secciones_extra.md]]')
    content.append('- **Proyecto Vault:** [[projects/linkedin-diego-tarazona|Proyecto LinkedIn Diego Tarazona]]')
    content.append('')
    content.append('## 🔗 Entidades del Ecosistema')
    content.append('- **Personas Clave:** [[people/diego-tarazona|Diego Tarazona]] | [[people/andres-lizarazo|Andrés Lizarazo]] | [[people/sandra-charry|Sandra Charry]] | [[people/maria-camila-canas|María Camila Cañas]]')
    content.append('- **Áreas de Vida y Trabajo:** [[areas/campuslands|Campuslands]] • [[areas/ia-aplicada-y-futuro-del-trabajo|IA Aplicada]] • [[areas/movilidad-social|Movilidad Social]] • [[areas/cultura-camper|Cultura Camper]]')
    content.append('- **Organizaciones y Aliados:** [[organizaciones/README|Directorio de Organizaciones]] ([[organizaciones/fedesoft|Fedesoft]], [[organizaciones/zona-franca-santander|Zona Franca Santander]], [[organizaciones/uniminuto|UNIMINUTO]], [[organizaciones/inexsu|INEXSU]], [[organizaciones/grupo-bien-pensado|Grupo Bien Pensado]])')
    content.append('')
    content.append(f'## ✍️ Publicaciones Propias de Diego Tarazona ({len(posts)} posts)')
    destacados_links = ' • '.join([f'[[diego_investigacion/02_publicaciones/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in destacados])
    content.append(f'- **Publicaciones Destacadas:** {destacados_links}')
    content.append('- **Actividad Interaccional:** [[diego_investigacion/02_publicaciones/00_comentarios_diego|59 Comentarios de Diego]] • [[diego_investigacion/02_publicaciones/00_reacciones_diego|60 Reacciones de Diego]]')
    content.append('')
    content.append('### Índice Completo de Posts de Diego (001 - 107)')

    for i in range(0, len(posts), 10):
        chunk = posts[i:i+10]
        links = [f'[[diego_investigacion/02_publicaciones/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in chunk]
        content.append(f'- **Posts {i+1:03d} a {min(i+10, len(posts)):03d}:** ' + ' • '.join(links))

    content.append('')
    content.append(f'## 📣 Menciones y Apariciones de Terceros ({len(menciones)} menciones)')
    for i in range(0, len(menciones), 10):
        chunk = menciones[i:i+10]
        links = [f'[[diego_investigacion/02_publicaciones/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in chunk]
        content.append(f'- **Menciones {i+1:03d} a {min(i+10, len(menciones)):03d}:** ' + ' • '.join(links))

    content.append('')
    content.append(f'## 🏢 Publicaciones Corporativas de Campuslands ({len(campuslands)} posts)')
    for i in range(0, len(campuslands), 10):
        chunk = campuslands[i:i+10]
        links = [f'[[diego_investigacion/02_publicaciones/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in chunk]
        content.append(f'- **Campuslands {i+1:03d} a {min(i+10, len(campuslands)):03d}:** ' + ' • '.join(links))

    content.append('')
    content.append(f'## 🎙️ Transcripciones Audiovisuales Multimodales ({len(trans)} videos/audios analizados)')
    for i in range(0, len(trans), 10):
        chunk = trans[i:i+10]
        links = [f'[[diego_investigacion/05_transcripciones/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3].replace("_transcripcion", "")}]]' for f in chunk]
        content.append(f'- **Transcripciones {i+1:03d} a {min(i+10, len(trans)):03d}:** ' + ' • '.join(links))

    with open('diego_investigacion/README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(content) + '\n')
    print('diego_investigacion/README.md generado con éxito.')

def generate_instagram_moc():
    posts_diego = sorted(glob.glob('diego_instagram/02_publicaciones/diego/*.md'))
    posts_campus = sorted(glob.glob('diego_instagram/02_publicaciones/campuslands/*.md'))
    trans = sorted(glob.glob('diego_instagram/05_transcripciones/*.md'))

    content = []
    content.append('---')
    content.append('tipo: moc')
    content.append('contexto: campuslands')
    content.append('tema: Investigacion Integral Diego Tarazona en Instagram')
    content.append('fecha_actualizacion: 2026-10-20')
    content.append('---')
    content.append('')
    content.append('# 📸 MOC: Investigación Integral Diego Tarazona (Instagram)')
    content.append('')
    content.append('Mapa de contenidos de la extracción y análisis de publicaciones y videos verticales (Reels) de [[people/diego-tarazona|Diego Tarazona]] y [[areas/campuslands|Campuslands]] en Instagram.')
    content.append('')
    content.append('## 🌟 Síntesis y Análisis')
    content.append('- **Análisis Maestro:** [[diego_instagram/06_analisis_maestro_instagram|06_analisis_maestro_instagram.md]]')
    content.append('- **Manual de Estilo y Patrones:** [[diego_instagram/06b_manual_de_estilo_y_patrones_diego|06b_manual_de_estilo_y_patrones_diego.md]]')
    content.append('- **Perfil Diego:** [[diego_instagram/01_perfil_diego|01_perfil_diego.md]]')
    content.append('- **Perfil Campuslands:** [[diego_instagram/01b_perfil_campuslands|01b_perfil_campuslands.md]]')
    content.append('- **Proyecto Vault:** [[projects/instagram-diego-tarazona|Proyecto Instagram Diego Tarazona]]')
    content.append('')
    content.append('## 🔗 Entidades Clave')
    content.append('- [[people/diego-tarazona|Diego Tarazona]] • [[areas/campuslands|Campuslands]] • [[diego_investigacion/README|Investigación LinkedIn]]')
    content.append('')
    content.append(f'## 🎥 Publicaciones de Diego Tarazona ({len(posts_diego)} posts/reels)')
    links_diego = [f'[[diego_instagram/02_publicaciones/diego/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in posts_diego]
    content.append('- ' + ' • '.join(links_diego))
    content.append('')
    content.append(f'## 🏢 Publicaciones de Campuslands ({len(posts_campus)} posts)')
    links_campus = [f'[[diego_instagram/02_publicaciones/campuslands/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in posts_campus]
    content.append('- ' + ' • '.join(links_campus))
    content.append('')
    content.append(f'## 🎙️ Transcripciones de Reels y Videos ({len(trans)} videos)')
    links_trans = [f'[[diego_instagram/05_transcripciones/{os.path.basename(f)[:-3]}|{os.path.basename(f)[:-3]}]]' for f in trans]
    content.append('- ' + ' • '.join(links_trans))

    with open('diego_instagram/README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(content) + '\n')
    print('diego_instagram/README.md generado con éxito.')

if __name__ == '__main__':
    generate_linkedin_moc()
    generate_instagram_moc()

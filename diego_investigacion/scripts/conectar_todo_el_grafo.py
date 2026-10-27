import os
import glob
import re

def strip_existing_footer(text):
    # Matches any previous ## 🔗 Conexiones or ## Conexiones section at the end of file
    pattern = r'\n+---\s*\n+##\s*(?:🔗\s*)?Conexiones.*$'
    text = re.sub(pattern, '', text, flags=re.DOTALL)
    # Also matches standalone ## 🔗 Conexiones at end without ---
    pattern2 = r'\n+##\s*(?:🔗\s*)?Conexiones.*$'
    text = re.sub(pattern2, '', text, flags=re.DOTALL)
    return text.strip()

def detect_thematic_areas(content):
    areas = []
    ia_re = re.compile(r'\bIA\b|inteligencia artificial|agentes?|llm|deepseek|openai|gpt|machine learning|automatiz', re.I)
    mov_re = re.compile(r'movilidad social|vulnerab|estrato|gratuito|sin costo|oportunidad|inclusi|transformaci[oó]n de vidas', re.I)
    cul_re = re.compile(r'camper|campers|filtro|entrenamiento|bootcamp|skill|ser y convivir|habilidades blandas', re.I)

    if ia_re.search(content):
        areas.append('[[areas/ia-aplicada-y-futuro-del-trabajo|IA y Futuro del Trabajo]]')
    if mov_re.search(content):
        areas.append('[[areas/movilidad-social|Movilidad Social]]')
    if cul_re.search(content):
        areas.append('[[areas/cultura-camper|Cultura Camper]]')

    if not areas:
        areas.append('[[areas/campuslands|Campuslands]]')
    return areas

def detect_entities(content):
    people = []
    orgs = []

    if re.search(r'lizarazo', content, re.I):
        people.append('[[people/andres-lizarazo|Andrés Lizarazo]]')
    if re.search(r'sandra charry|charry', content, re.I):
        people.append('[[people/sandra-charry|Sandra Charry]]')
    if re.search(r'mar[ií]a camila|ca[nñ]as', content, re.I):
        people.append('[[people/maria-camila-canas|María Camila Cañas]]')

    if re.search(r'fedesoft', content, re.I):
        orgs.append('[[organizaciones/fedesoft|Fedesoft]]')
    if re.search(r'zona franca', content, re.I):
        orgs.append('[[organizaciones/zona-franca-santander|Zona Franca Santander]]')
    if re.search(r'uniminuto', content, re.I):
        orgs.append('[[organizaciones/uniminuto|UNIMINUTO]]')
    if re.search(r'inexsu', content, re.I):
        orgs.append('[[organizaciones/inexsu|INEXSU]]')
    if re.search(r'bien pensado', content, re.I):
        orgs.append('[[organizaciones/grupo-bien-pensado|Grupo Bien Pensado]]')
    if re.search(r'\bandi\b', content, re.I):
        orgs.append('[[organizaciones/andi|ANDI]]')
    if re.search(r'procolombia', content, re.I):
        orgs.append('[[organizaciones/procolombia|ProColombia]]')
    if re.search(r'cenisoft', content, re.I):
        orgs.append('[[organizaciones/cenisoft|CENISOFT]]')

    return people, orgs

def process_linkedin_publications():
    pub_files = glob.glob('diego_investigacion/02_publicaciones/*.md')
    print(f'Procesando {len(pub_files)} publicaciones de LinkedIn...')

    for fpath in pub_files:
        stem = os.path.basename(fpath)[:-3]
        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()

        clean_text = strip_existing_footer(raw)
        areas = detect_thematic_areas(clean_text)
        people, orgs = detect_entities(clean_text)

        # Transcripcion
        trans_path = f'diego_investigacion/05_transcripciones/{stem}_transcripcion.md'
        has_trans = os.path.exists(trans_path)

        # Build concise connection block
        lines = []
        lines.append('')
        lines.append('---')
        lines.append('## 🔗 Conexiones del Segundo Cerebro')
        if stem.startswith('post_') or stem.startswith('00_'):
            lines.append('- **Entidad principal:** [[people/diego-tarazona|Diego Tarazona]] | [[areas/campuslands|Campuslands]]')
        elif stem.startswith('campuslands_'):
            lines.append('- **Entidad principal:** [[areas/campuslands|Campuslands]] | [[people/diego-tarazona|Diego Tarazona]]')
        else: # mencion_
            lines.append('- **Entidad principal:** [[areas/campuslands|Campuslands]] | [[people/diego-tarazona|Diego Tarazona]]')

        lines.append('- **MOC & Análisis:** [[diego_investigacion/README|MOC Diego Tarazona]] | [[diego_investigacion/06_analisis_maestro_diego|Análisis Maestro]]')
        
        if has_trans:
            lines.append(f'- **Transcripción Multimedia:** [[diego_investigacion/05_transcripciones/{stem}_transcripcion|Transcripción y Análisis Multimodal]]')

        lines.append('- **Áreas temáticas:** ' + ' • '.join(areas))

        menciones = []
        if people:
            menciones.extend(people)
        if orgs:
            menciones.extend(orgs)

        if menciones:
            lines.append('- **Entidades y Aliados detectados:** ' + ' • '.join(menciones))

        new_content = clean_text + '\n' + '\n'.join(lines) + '\n'
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print('Publicaciones de LinkedIn procesadas con éxito.')

def process_linkedin_transcriptions():
    trans_files = glob.glob('diego_investigacion/05_transcripciones/*.md')
    print(f'Procesando {len(trans_files)} transcripciones de LinkedIn...')

    for fpath in trans_files:
        stem = os.path.basename(fpath)[:-3]
        orig_stem = stem.replace('_transcripcion', '')
        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()

        clean_text = strip_existing_footer(raw)
        areas = detect_thematic_areas(clean_text)
        people, orgs = detect_entities(clean_text)

        lines = []
        lines.append('')
        lines.append('---')
        lines.append('## 🔗 Conexiones del Segundo Cerebro')
        lines.append(f'- **Publicación original:** [[diego_investigacion/02_publicaciones/{orig_stem}|Publicación Original ({orig_stem})]]')
        lines.append('- **Entidad principal:** [[people/diego-tarazona|Diego Tarazona]] | [[areas/campuslands|Campuslands]]')
        lines.append('- **MOC & Análisis:** [[diego_investigacion/README|MOC Diego Tarazona]] | [[diego_investigacion/06_analisis_maestro_diego|Análisis Maestro]]')
        lines.append('- **Áreas temáticas:** ' + ' • '.join(areas))

        menciones = []
        if people:
            menciones.extend(people)
        if orgs:
            menciones.extend(orgs)
        if menciones:
            lines.append('- **Entidades y Aliados detectados:** ' + ' • '.join(menciones))

        new_content = clean_text + '\n' + '\n'.join(lines) + '\n'
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print('Transcripciones de LinkedIn procesadas con éxito.')

def process_linkedin_profile_docs():
    profiles = [
        'diego_investigacion/01_perfil_general.md',
        'diego_investigacion/01b_perfil_campuslands.md',
        'diego_investigacion/01c_perfil_secciones_extra.md',
        'diego_investigacion/06_analisis_maestro_diego.md'
    ]
    for p in profiles:
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            raw = f.read()
        clean_text = strip_existing_footer(raw)
        lines = []
        lines.append('')
        lines.append('---')
        lines.append('## 🔗 Conexiones del Segundo Cerebro')
        lines.append('- **Persona:** [[people/diego-tarazona|Diego Tarazona]] | [[people/andres-lizarazo|Andrés Lizarazo]]')
        lines.append('- **Organización:** [[areas/campuslands|Campuslands]] | [[organizaciones/grupo-bien-pensado|Grupo Bien Pensado]]')
        lines.append('- **Índice General:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]')
        lines.append('- **Proyecto:** [[projects/linkedin-diego-tarazona|Proyecto LinkedIn]]')
        lines.append('- **Áreas:** [[areas/ia-aplicada-y-futuro-del-trabajo|IA Aplicada]] • [[areas/movilidad-social|Movilidad Social]]')

        new_content = clean_text + '\n' + '\n'.join(lines) + '\n'
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_content)
    print('Documentos de perfil y análisis maestro de LinkedIn procesados.')

def process_instagram():
    posts_diego = glob.glob('diego_instagram/02_publicaciones/diego/*.md')
    posts_campus = glob.glob('diego_instagram/02_publicaciones/campuslands/*.md')
    trans = glob.glob('diego_instagram/05_transcripciones/*.md')
    meta_files = [
        'diego_instagram/01_perfil_diego.md',
        'diego_instagram/01b_perfil_campuslands.md',
        'diego_instagram/06_analisis_maestro_instagram.md',
        'diego_instagram/06b_manual_de_estilo_y_patrones_diego.md'
    ]

    for fpath in posts_diego:
        stem = os.path.basename(fpath)[:-3]
        with open(fpath, 'r', encoding='utf-8') as f:
            clean_text = strip_existing_footer(f.read())
        trans_path = f'diego_instagram/05_transcripciones/{stem}_transcripcion.md'
        has_trans = os.path.exists(trans_path)
        lines = [
            '',
            '---',
            '## 🔗 Conexiones del Segundo Cerebro',
            '- **Entidad principal:** [[people/diego-tarazona|Diego Tarazona]] | [[areas/campuslands|Campuslands]]',
            '- **MOC Instagram:** [[diego_instagram/README|MOC Instagram]] | [[projects/instagram-diego-tarazona|Proyecto Instagram]]',
            '- **Investigación General:** [[diego_investigacion/README|Investigación LinkedIn Diego Tarazona]]'
        ]
        if has_trans:
            lines.append(f'- **Transcripción Reel:** [[diego_instagram/05_transcripciones/{stem}_transcripcion|Transcripción Reel]]')
        lines.append('- **Áreas temáticas:** [[areas/ia-aplicada-y-futuro-del-trabajo|IA Aplicada]] • [[areas/cultura-camper|Cultura Camper]]')

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(clean_text + '\n' + '\n'.join(lines) + '\n')

    for fpath in posts_campus:
        with open(fpath, 'r', encoding='utf-8') as f:
            clean_text = strip_existing_footer(f.read())
        lines = [
            '',
            '---',
            '## 🔗 Conexiones del Segundo Cerebro',
            '- **Entidad principal:** [[areas/campuslands|Campuslands]] | [[people/diego-tarazona|Diego Tarazona]]',
            '- **MOC Instagram:** [[diego_instagram/README|MOC Instagram]]',
            '- **Investigación General:** [[diego_investigacion/README|Investigación LinkedIn Diego Tarazona]]',
            '- **Áreas temáticas:** [[areas/cultura-camper|Cultura Camper]] • [[areas/movilidad-social|Movilidad Social]]'
        ]
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(clean_text + '\n' + '\n'.join(lines) + '\n')

    for fpath in trans:
        stem = os.path.basename(fpath)[:-3]
        orig_stem = stem.replace('_transcripcion', '')
        orig_diego = f'diego_instagram/02_publicaciones/diego/{orig_stem}.md'
        with open(fpath, 'r', encoding='utf-8') as f:
            clean_text = strip_existing_footer(f.read())
        lines = [
            '',
            '---',
            '## 🔗 Conexiones del Segundo Cerebro',
            f'- **Publicación Instagram:** [[diego_instagram/02_publicaciones/diego/{orig_stem}|Publicación Original ({orig_stem})]]',
            '- **Entidad principal:** [[people/diego-tarazona|Diego Tarazona]] | [[areas/campuslands|Campuslands]]',
            '- **MOC Instagram:** [[diego_instagram/README|MOC Instagram]] | [[diego_instagram/06_analisis_maestro_instagram|Análisis Maestro Instagram]]',
            '- **Áreas temáticas:** [[areas/ia-aplicada-y-futuro-del-trabajo|IA Aplicada]] • [[areas/cultura-camper|Cultura Camper]]'
        ]
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(clean_text + '\n' + '\n'.join(lines) + '\n')

    for p in meta_files:
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            clean_text = strip_existing_footer(f.read())
        lines = [
            '',
            '---',
            '## 🔗 Conexiones del Segundo Cerebro',
            '- **Entidades:** [[people/diego-tarazona|Diego Tarazona]] • [[areas/campuslands|Campuslands]]',
            '- **MOC Instagram:** [[diego_instagram/README|MOC Instagram]]',
            '- **Proyecto Vault:** [[projects/instagram-diego-tarazona|Proyecto Instagram]]',
            '- **Investigación Principal:** [[diego_investigacion/README|Investigación LinkedIn]]'
        ]
        with open(p, 'w', encoding='utf-8') as f:
            f.write(clean_text + '\n' + '\n'.join(lines) + '\n')

    print('Archivos de Instagram procesados con éxito.')

def process_campuslands_corpus_podcasts():
    corpus_files = glob.glob('investigacion/campuslands/corpus_youtube_podcasts/*.md')
    print(f'Procesando {len(corpus_files)} archivos de corpus youtube/podcast de Campuslands...')
    for fpath in corpus_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            clean_text = strip_existing_footer(f.read())
        lines = [
            '',
            '---',
            '## 🔗 Conexiones del Segundo Cerebro',
            '- **Entidad:** [[areas/campuslands|Campuslands]]',
            '- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]',
            '- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]'
        ]
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(clean_text + '\n' + '\n'.join(lines) + '\n')
    print('Corpus de Campuslands procesado con éxito.')

if __name__ == '__main__':
    process_linkedin_publications()
    process_linkedin_transcriptions()
    process_linkedin_profile_docs()
    process_instagram()
    process_campuslands_corpus_podcasts()
    print('¡TODO EL GRAFO HA SIDO CONECTADO EXITOSAMENTE!')

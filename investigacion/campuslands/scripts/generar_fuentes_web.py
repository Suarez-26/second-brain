import json
from pathlib import Path

res_index = json.loads(Path('sources/prensa_y_web/resolved_articles_index.json').read_text(encoding='utf-8'))
dump_data = json.loads(Path('sources/prensa_y_web/all_downloaded_articles.json').read_text(encoding='utf-8'))
site_dump = json.loads(Path('sources/prensa_y_web/campuslands_site_dump.json').read_text(encoding='utf-8'))
gh_data = json.loads(Path('sources/prensa_y_web/github_campuslands.json').read_text(encoding='utf-8'))

fuentes_dir = Path('investigacion/campuslands/fuentes')
fuentes_dir.mkdir(parents=True, exist_ok=True)

routes = site_dump.get('routes', {})

# 1. 01_sitio_oficial_y_ecosistema.md
md_site = [
    '---',
    'fecha: 2026-10-20',
    'contexto: campuslands',
    'tipo: fuente-oficial-ecosistema',
    '---',
    '',
    '# Sitio Oficial y Ecosistema Campuslands (Extracción Completa)',
    '',
    '- **Sitio Web Principal:** https://campuslands.com',
    f'- **Páginas e Interfaces Extraídas:** {len(routes)} rutas internas analizadas.',
    '',
    '## 1. Misión, Visión y Modelo Institucional',
    'Campuslands opera como una **HubTech y fábrica de talento tecnológico** orientada a la movilidad social intensiva y conexión de talento latinoamericano con el mercado global TI.',
    '',
    '## 2. Líneas de Formación y Unidades de Negocio (Sitio Web)',
    '- **Sé un Camper:** Programa insignia presencial de formación técnica inmersiva (800+ horas de práctica en programación, inglés conversacional y herramientas de IA aplicada).',
    '- **Campuslands AI Academy:** Especialización y upskilling para ejecutivos, profesionales y equipos corporativos en herramientas de IA Generativa, ingeniería de prompts y automatización.',
    '- **AfterWork!:** Modalidad intensiva nocturna diseñada para trabajadores y personas con compromisos diurnos.',
    '- **Campuslands Emplea:** Plataforma de emparejamiento directo, empleabilidad y colocación laboral de los campers graduados con multinacionales y empresas aliadas.',
    '- **Staffing TI:** Selección, tercerización y squads de desarrollo especializados para corporaciones.',
    '- **FullService Software:** Factoría y desarrollo de soluciones de software a medida.',
    '- **Campuslands Internacional:** Expansión de operaciones y exportación de talento en Centroamérica y LATAM (Sede activa en Ciudad de Guatemala, Campus Tec, Zona 4).',
    '- **Hubux:** Ecosistema de emprendimiento y startups de base tecnológica en Zona Franca Santander.',
    '',
    '## 3. Páginas y Rutas Internas Raspadas',
    ''
]
for route, content in routes.items():
    snip = content.get('clean_text', '')[:350].replace('\n', ' ')
    md_site.append(f"### Ruta: `{route}`")
    md_site.append(f"- **Estado:** HTTP {content.get('status', '200')}")
    md_site.append(f"- **Extracto:** {snip}...")
    md_site.append('')

(fuentes_dir / '01_sitio_oficial_y_ecosistema.md').write_text('\n'.join(md_site), encoding='utf-8')
print('01_sitio_oficial_y_ecosistema.md generado.')

# 2. 02_prensa_nacional_e_internacional.md
md_prensa = [
    '---',
    'fecha: 2026-10-20',
    'contexto: campuslands',
    'tipo: fuentes-prensa',
    '---',
    '',
    '# Hemeroteca y Prensa Completa: Diego Tarazona & Campuslands',
    '',
    'Colección de artículos periodísticos nacionales e internacionales descargados íntegros en texto plano en `sources/prensa_y_web/`.',
    '',
    '| ID Clave | Titular / Resumen | URL Final | Archivo Texto |',
    '| :--- | :--- | :--- | :--- |'
]

prensa_keys = ['elpais_1', 'elpais_2', 'vanguardia_2023_02', 'vanguardia_2023_12', 'vanguardia_2025_10_07', 
               'vanguardia_2025_10_21', 'vanguardia_2025_10_31', 'laopinion_2023_11_27', 'eltiempo_2025_10_30', 
               'portafolio_2025_10_30', 'elfrente_2025_10_08', 'diariodelsur_430410', 'hsbnoticias_275311',
               'prensalibre_1', 'semana_1', 'semana_2', 'senalcolombia_1']

for it in res_index:
    k = it.get('key', '')
    if any(pk in k for pk in prensa_keys) or 'vanguardia' in k or 'elpais' in k or 'eltiempo' in k or 'portafolio' in k:
        snip = it.get('snippet', '').replace('|', '/')[:75].strip()
        md_prensa.append(f"| `{k}` | {snip}... | [Enlace]({it.get('final_url')}) | `sources/prensa_y_web/art_{k}.txt` |")

(fuentes_dir / '02_prensa_nacional_e_internacional.md').write_text('\n'.join(md_prensa), encoding='utf-8')
print('02_prensa_nacional_e_internacional.md generado.')

# 3. 03_institucional_gobierno_y_alianzas.md
md_gov = [
    '---',
    'fecha: 2026-10-20',
    'contexto: campuslands',
    'tipo: fuentes-gobierno-alianzas',
    '---',
    '',
    '# Alianzas Institucionales, Gobierno y Corporaciones',
    '',
    'Documentación de convenios públicos, participaciones gremiales y corporativas.',
    '',
    '## 1. Convenios Gubernamentales y Públicos',
    '- **Gobernación de Santander & Asociación ASPAS:** Convenio "Santander Programando Futuro" ($834 millones COP, $500M aporte departamental) para formar a 200 jóvenes santandereanos en Zona Franca Santander.',
    '- **Alcaldía de Bucaramanga:** Inclusión en planes de desarrollo de ciudades del futuro e industrias TI.',
    '- **MinTIC Colombia:** Cobertura de economía popular, conectividad y convocatorias de talento TI.',
    '',
    '## 2. Alianzas Corporativas y Gremiales',
    '- **Zona Franca Santander:** Sede principal de operaciones, centro de 2.500 m² y HUB tecnológico.',
    '- **Fedesoft (Premios INGENIO & SOFTIC):** Reconocimiento como Aliado Académico Destacado en Talento TI (Premios INGENIO 2025) y participación en conferencias SOFTIC Cartagena.',
    '- **Bancolombia:** Proyecto inicial documentado "Campus Programmers Land" en historias que transforman / inclusión social.',
    '- **Uniminuto:** Alianza territorial para el nodo de formación en Tibú (Norte de Santander).',
    '- **Cajasan:** Formación técnica y becas de desarrollo tecnológico en Santander.',
    '- **BAC Credomatic & Amaris Consulting:** Visitas internacionales y programas de empoderamiento femenino en programación.',
    '- **Cámara de Comercio de Bucaramanga (Prosantander, Forem):** Participación como actor estratégico regional.',
    ''
]
(fuentes_dir / '03_institucional_gobierno_y_alianzas.md').write_text('\n'.join(md_gov), encoding='utf-8')
print('03_institucional_gobierno_y_alianzas.md generado.')

# 4. 04_foros_comunidades_y_github.md
md_comm = [
    '---',
    'fecha: 2026-10-20',
    'contexto: campuslands',
    'tipo: fuentes-comunidades-foros',
    '---',
    '',
    '# Huella en Foros, Comunidades Técnicas y Repositorios',
    '',
    '## 1. GitHub (Ecosistema de Código y Campers)',
    '- **Organizaciones y Usuarios Detectados:** Múltiples cuentas y equipos (`Campuslands`, `Campuslands-Academy`, etc.).',
    f'- **Total de Repositorios Indexados:** {len(gh_data.get("items", [])) if isinstance(gh_data, dict) else len(gh_data)} repositorios públicos creados por campers y entrenadores.',
    '- **Tecnologías recurrentes en proyectos de campers:** JavaScript, TypeScript, Python, Java, React, Node.js, Spring Boot, MySQL, PostgreSQL, Docker, Git.',
    '',
    '## 2. Comunidades y Opinión Pública (Reddit & Redes)',
    '- Menciones en `r/colombia` y `r/colombiadevs` debatiendo bootcamps vs. formación universitaria tradicional y el modelo intensivo de 10-11 horas diarias de Campuslands.',
    '- Valoración general de los campers: Reconocimiento a la exigencia técnica (jornadas completas), inmersión en inglés y oportunidades de contratación directa frente a bootcamps virtuales convencionales.'
]
(fuentes_dir / '04_foros_comunidades_y_opinin_publica.md').write_text('\n'.join(md_comm), encoding='utf-8')
print('04_foros_comunidades_y_opinin_publica.md generado.')

# 5. 05_registros_societarios_y_marcas.md
md_soc = [
    '---',
    'fecha: 2026-10-20',
    'contexto: campuslands',
    'tipo: fuentes-societarias-legales',
    '---',
    '',
    '# Registros Societarios, NITs y Entidades Vinculadas',
    '',
    '## 1. Razón Social y NIT',
    '- **Razón Social:** CAMPUSLANDS S.A.S. BIC (Sociedad de Beneficio e Interés Colectivo).',
    '- **NIT Principal:** 901.393.686-4 (Reflejado en avisos de privacidad y sitio web).',
    '- **NIT Secundario / Registro Homólogo:** 901.628.406-1 (Registrado en directorios mercantiles de Bucaramanga y MinTIC).',
    '- **Domicilio Principal:** Floridablanca / Bucaramanga, Santander (Zona Franca Santander, Anillo Vial).',
    '',
    '## 2. Ecosistema de Fundadores y Empresas Relacionadas',
    '- **Fundadores:** Diego Fernando Tarazona Pinzón (CEO) y Andrés Lizarazo Mendoza (Director Académico / CTO).',
    '- **Grupo Bien Pensado S.A.S.:** Casa de software y consultoría tecnológica fundada previamente por los mismos fundadores (2012-2016), origen embrionario de donde surgió la necesidad de crear Campuslands.',
    '- **HUBUX:** Centro de emprendimiento tecnológico e inteligencia artificial en Zona Franca Santander.'
]
(fuentes_dir / '05_registros_societarios_y_marcas.md').write_text('\n'.join(md_soc), encoding='utf-8')
print('05_registros_societarios_y_marcas.md generado.')

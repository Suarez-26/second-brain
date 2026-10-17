const pptxgen = require("pptxgenjs");
const path = require("path");
const SKILL = "C:/Users/tomas/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/9d66d277-1fb4-4153-a2ec-5cc9a13dd7d8/fa44a7d5-c25a-40f5-9b5e-9aaa9204c8ab/skills/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const OUT = "C:/Users/tomas/second-brain/presentaciones/second-brain-y-30x.pptx";

// Paleta oficial Campuslands (Brandbook 2023 V2)
const MORADO = "5E3AE2", MARINO = "000087", AMBAR = "F4B422", VERDE = "00AA80";
const CELESTE = "2CAAFF", GRIS = "E4E4DB", TINTA = "3B3B3B", BLANCO = "FFFFFF";
const MORADO_CLARO = "7E5EE8"; // numeral de fondo en separadores
const LOGO = "C:/Users/tomas/second-brain/presentaciones/assets/campuslands-logo-blanco.png";
const HEAD = "Poppins", MONO = "Roboto Mono";

const THEME = {
  name: "Campuslands",
  headFontFace: HEAD,
  bodyFontFace: HEAD,
  colors: {
    dk1: TINTA, lt1: BLANCO, dk2: MARINO, lt2: GRIS,
    accent1: MORADO, accent2: MARINO, accent3: AMBAR, accent4: VERDE,
    accent5: CELESTE, accent6: GRIS, hlink: CELESTE, folHlink: MORADO,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Second Brain con IA y el programa de 30X";
pres.author = "Pao";
pres.theme = { headFontFace: HEAD, bodyFontFace: HEAD };

const W = 13.33;
const BREAD = "second brain";

// ---------- Layouts ----------
pres.defineSlideMaster({ title: "PORTADA", background: { color: MORADO } });
pres.defineSlideMaster({ title: "SECCION", background: { color: MORADO } });
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: BLANCO },
  objects: [
    {
      placeholder: {
        options: {
          name: "title", type: "title", x: 0.6, y: 0.75, w: 12.1, h: 0.9,
          fontFace: HEAD, fontSize: 36, bold: true, color: MORADO,
          margin: 0, valign: "top",
        },
        text: "",
      },
    },
  ],
});

// ---------- Helpers ----------
function crumb(slide, section, dark) {
  slide.addText(`| campuslands | ${BREAD} | ${section.toLowerCase()} |`, {
    x: 0.6, y: 0.28, w: 12.1, h: 0.3, fontFace: MONO, fontSize: 11,
    color: dark ? CELESTE : TINTA, margin: 0, isTextBox: true, objectName: "Breadcrumb",
  });
}
function tag(slide, text, dark) {
  slide.addText(text, {
    x: 0.6, y: 6.95, w: 6, h: 0.3, fontFace: MONO, fontSize: 12,
    color: dark ? BLANCO : MORADO, margin: 0, isTextBox: true, objectName: "Tag",
  });
}
function source(slide, text) {
  slide.addText(text, {
    x: 6.7, y: 6.95, w: 6.03, h: 0.3, fontFace: HEAD, fontSize: 10, align: "right",
    color: TINTA, margin: 0, isTextBox: true, objectName: "Fuente",
  });
}

let secIdx = 0;
function contentSlide(section, title, tagText) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: section });
  crumb(s, section, false);
  s.addText(title, { placeholder: "title" });
  tag(s, tagText, false);
  return s;
}

function card(slide, x, y, w, h, opts) {
  const { num, title, body, titleColor } = opts;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12, fill: { color: GRIS, transparency: 55 },
    line: { color: GRIS, width: 0.75 }, objectName: "Tarjeta",
  });
  let ty = y + 0.3;
  if (num !== undefined) {
    slide.addShape(pres.shapes.OVAL, {
      x: x + 0.3, y: y + 0.3, w: 0.6, h: 0.6, fill: { color: MORADO }, line: { color: MORADO },
      objectName: "Numero",
    });
    slide.addText(String(num), {
      x: x + 0.3, y: y + 0.3, w: 0.6, h: 0.6, align: "center", valign: "middle",
      fontFace: HEAD, fontSize: 18, bold: true, color: BLANCO, margin: 0, isTextBox: true,
    });
    ty = y + 1.1;
  }
  slide.addText(title, {
    x: x + 0.3, y: ty, w: w - 0.6, h: 0.75, fontFace: HEAD, fontSize: 18, bold: true,
    color: titleColor || MORADO, margin: 0, valign: "top", isTextBox: true,
  });
  slide.addText(body, {
    x: x + 0.3, y: ty + 0.8, w: w - 0.6, h: h - (ty - y) - 1.1, fontFace: HEAD, fontSize: 14,
    color: TINTA, margin: 0, valign: "top", isTextBox: true,
  });
}

function separator(n, title, subtitle, section) {
  const s = pres.addSlide({ masterName: "SECCION", sectionTitle: section });
  s.addText(String(n), {
    x: 7.4, y: 0.6, w: 5.6, h: 6.2, fontFace: HEAD, fontSize: 300, bold: true,
    color: MORADO_CLARO, align: "right", valign: "middle", margin: 0, isTextBox: true,
    objectName: "Numeral",
  });
  crumb(s, section, true);
  s.addText(title, {
    x: 0.8, y: 2.5, w: 7.2, h: 2.0, fontFace: HEAD, fontSize: 44, bold: true,
    color: BLANCO, margin: 0, valign: "bottom", isTextBox: true,
  });
  s.addText(subtitle, {
    x: 0.8, y: 4.7, w: 7.0, h: 0.8, fontFace: MONO, fontSize: 16, color: CELESTE,
    margin: 0, valign: "top", isTextBox: true,
  });
  tag(s, `</${section.toLowerCase()}`, true);
  return s;
}

// ================== 1. PORTADA ==================
{
  pres.addSection({ title: "Portada" });
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Portada" });
  s.addImage({
    path: LOGO, x: 0.8, y: 0.5, w: 1.25, h: 1.35, objectName: "Logo Campuslands",
    altText: "Logo de Campuslands",
  });
  s.addShape(pres.shapes.LINE, {
    x: 2.4, y: 0.6, w: 0, h: 1.15, line: { color: BLANCO, width: 1.5 }, objectName: "Divisor",
  });
  s.addText("CÓMO CONSTRUIR TU SECOND BRAIN CON IA", {
    x: 0.8, y: 2.0, w: 11.7, h: 2.8, fontFace: HEAD, fontSize: 48, bold: true,
    color: BLANCO, margin: 0, valign: "middle", isTextBox: true,
  });
  s.addText("Guía paso a paso + el programa AI Second Brain de 30X", {
    x: 0.8, y: 5.0, w: 11.7, h: 0.6, fontFace: MONO, fontSize: 18, color: CELESTE,
    margin: 0, isTextBox: true,
  });
  tag(s, "</presentación", true);
  s.addText("GO FOR IT!", {
    x: 8.7, y: 6.9, w: 4.03, h: 0.4, fontFace: HEAD, fontSize: 16, bold: true, align: "right",
    color: AMBAR, margin: 0, isTextBox: true,
  });
  s.addNotes("Portada con el logo blanco de Campuslands.");
}

// ================== 2. ÍNDICE ==================
{
  pres.addSection({ title: "Índice" });
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Índice" });
  crumb(s, "índice", false);
  s.addText("{ Índice }", { placeholder: "title" });
  tag(s, "</índice", false);
  const cols = [
    { n: "1", t: "Qué es", c: MORADO, items: ["definición", "las 3 capas"] },
    { n: "2", t: "Cómo construirlo", c: MARINO, items: ["7 pasos", "estructura"] },
    { n: "3", t: "Rutina y seguridad", c: MORADO, items: ["comandos", "panel", "riesgos"] },
    { n: "4", t: "El programa de 30X", c: MARINO, items: ["qué es", "quiénes", "siguientes pasos"] },
  ];
  const cw = 2.85, gap = 0.243;
  cols.forEach((c, i) => {
    const x = 0.6 + i * (cw + gap);
    s.addText(c.n, {
      x, y: 1.9, w: cw, h: 1.7, fontFace: HEAD, fontSize: 96, bold: true, color: GRIS,
      margin: 0, valign: "top", isTextBox: true, objectName: "Numeral",
    });
    s.addText(c.t, {
      x, y: 3.3, w: cw, h: 0.9, fontFace: HEAD, fontSize: 20, bold: true, color: c.c,
      margin: 0, valign: "top", isTextBox: true,
    });
    s.addText("<=", { x, y: 4.3, w: cw, h: 0.3, fontFace: MONO, fontSize: 13, color: TINTA, margin: 0, isTextBox: true });
    s.addText(c.items.join("\n"), {
      x, y: 4.65, w: cw, h: 1.3, fontFace: MONO, fontSize: 13, color: TINTA, margin: 0,
      valign: "top", isTextBox: true,
    });
    s.addText("=>", { x, y: 6.0, w: cw, h: 0.3, fontFace: MONO, fontSize: 13, color: TINTA, margin: 0, isTextBox: true });
  });
}

// ================== SECCIÓN 1: QUÉ ES ==================
const S1 = "Qué es";
pres.addSection({ title: "Qué es" });
separator(1, "QUÉ ES UN SECOND BRAIN", "una memoria que la IA lee y actualiza", S1);

{
  const s = contentSlide(S1, "{ Qué es }", "</qué es");
  s.addText(
    "Una memoria persistente sobre ti (contexto, decisiones, personas y proyectos) que una IA lee y actualiza, para que no tengas que re-explicarte en cada conversación.",
    { x: 0.6, y: 1.8, w: 12.1, h: 1.1, fontFace: HEAD, fontSize: 18, color: TINTA, margin: 0, valign: "top", isTextBox: true }
  );
  const w = 3.84, g = 0.3, y = 3.2, h = 3.4;
  card(s, 0.6, y, w, h, { title: "Contexto de ti", body: "Tu trabajo, tus proyectos y tu historia, siempre a la mano de la IA." });
  card(s, 0.6 + w + g, y, w, h, { title: "Actúa como tú", body: "Responde y ejecuta con tu voz y tus prioridades." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { title: "Te cuestiona", body: "Panel de asesores y reglas de honestidad para que no te dé siempre la razón." });
  source(s, "Fuente: podcast 30X con Adelaida Díaz-Roa");
}

{
  const s = contentSlide(S1, "{ Las 3 capas }", "</capas");
  const w = 3.84, g = 0.3, y = 1.9, h = 3.9;
  card(s, 0.6, y, w, h, { num: 1, title: "Siempre", body: "Carpeta meta/: 5 notas cortas que Claude lee al empezar cada sesión." });
  card(s, 0.6 + w + g, y, w, h, { num: 2, title: "Según el tema", body: "Carpeta areas/ y resúmenes mensuales: 200 a 400 palabras por área." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { num: 3, title: "Solo si hace falta", body: "Diario, personas, proyectos y fuentes. Se abre para un dato concreto." });
  s.addText("Regla: comprimir primero, buscar después.", {
    x: 0.6, y: 6.1, w: 12.1, h: 0.5, fontFace: MONO, fontSize: 16, color: MORADO, margin: 0, isTextBox: true,
  });
}

// ================== SECCIÓN 2: CÓMO CONSTRUIRLO ==================
const S2 = "Cómo construirlo";
pres.addSection({ title: "Cómo construirlo" });
separator(2, "CÓMO CONSTRUIRLO", "7 pasos y una estructura de carpetas", S2);

{
  const s = contentSlide(S2, "{ Pasos 1 a 4 }", "</pasos");
  const w = 2.84, g = 0.25, y = 1.9, h = 4.7;
  card(s, 0.6, y, w, h, { num: 1, title: "Crea la carpeta", body: "Una carpeta de archivos Markdown. Opcional: ábrela con Obsidian." });
  card(s, 0.6 + (w + g), y, w, h, { num: 2, title: "Escribe CLAUDE.md", body: "Reglas, estructura y tono. Claude lo lee al empezar." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { num: 3, title: "Arma la memoria", body: "meta/ con 5 notas: start-here, prioridades, pendientes, última sesión, decisiones." });
  card(s, 0.6 + 3 * (w + g), y, w, h, { num: 4, title: "Pide entrevista", body: "\"Entrevístame para llenar mi contexto\". Claude escribe tu start-here." });
}

{
  const s = contentSlide(S2, "{ Pasos 5 a 7 }", "</pasos");
  const w = 3.84, g = 0.3, y = 1.9, h = 4.3;
  card(s, 0.6, y, w, h, { num: 5, title: "Conecta Claude", body: "Claude Code en la carpeta, o Claude Desktop con el MCP de filesystem apuntando al vault." });
  card(s, 0.6 + w + g, y, w, h, { num: 6, title: "Haz journaling", body: "Cada noche, por texto o por voz. Es el combustible del sistema." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { num: 7, title: "Suma fuentes", body: "Documentos y reuniones primero. Evalúa el riesgo antes de conectar WhatsApp o correo." });
}

{
  const s = contentSlide(S2, "{ Estructura }", "</estructura");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.6, y: 1.9, w: 7.4, h: 4.6, rectRadius: 0.12, fill: { color: MARINO }, line: { color: MARINO },
    objectName: "Bloque de código",
  });
  const code = [
    "second-brain/",
    "  CLAUDE.md    reglas y memoria",
    "  meta/        capa 1: contexto",
    "  areas/       capa 2: resúmenes",
    "  journal/     diario y resúmenes",
    "  people/      una nota por persona",
    "  projects/    proyectos y empresas",
    "  advisors/    panel de asesores",
    "  inbox/       por procesar",
    "  sources/     originales intactos",
  ].join("\n");
  s.addText(code, {
    x: 0.9, y: 2.1, w: 6.8, h: 4.2, fontFace: MONO, fontSize: 15, color: BLANCO, margin: 0,
    valign: "top", isTextBox: true,
  });
  card(s, 8.3, 1.9, 4.43, 4.6, {
    title: "Reglas de cada nota",
    body: "Frontmatter con fecha y contexto.\n\nAl menos un enlace [[ ]] a otra nota.\n\nToda afirmación cita su fuente.",
  });
}

// ================== SECCIÓN 3: RUTINA Y SEGURIDAD ==================
const S3 = "Rutina y seguridad";
pres.addSection({ title: "Rutina y seguridad" });
separator(3, "RUTINA Y SEGURIDAD", "comandos, panel de asesores y riesgos", S3);

{
  const s = contentSlide(S3, "{ Comandos }", "</comandos");
  const w = 2.84, g = 0.25, y = 1.9, h = 4.7;
  const items = [
    ["/journal", "Entrevista de la noche. Crea la entrada y actualiza personas y pendientes."],
    ["/weekly", "Patrones de la semana, pendientes viejos y lo que estás evitando."],
    ["/monthly", "Comprime el mes para la capa 2 y marca tendencias."],
    ["/cierre", "Guarda decisiones y el siguiente paso para la próxima sesión."],
  ];
  items.forEach((it, i) => card(s, 0.6 + i * (w + g), y, w, h, { title: it[0], body: it[1] }));
}

{
  const s = contentSlide(S3, "{ Panel de asesores }", "</panel");
  s.addText(
    "Antes de una decisión de dinero, tiempo o relaciones, Claude consulta de 3 a 5 voces. Siempre hay al menos una que discrepa.",
    { x: 0.6, y: 1.8, w: 12.1, h: 1.0, fontFace: HEAD, fontSize: 18, color: TINTA, margin: 0, valign: "top", isTextBox: true }
  );
  const w = 3.84, g = 0.3, y = 3.1, h = 3.4;
  card(s, 0.6, y, w, h, { title: "Estratega de velocidad", body: "Ejecutar rápido, probar y corregir." });
  card(s, 0.6 + w + g, y, w, h, { title: "Voz de bienestar", body: "Sueño, energía y sentido." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { title: "Abogado del diablo", body: "Riesgos y supuestos sin probar." });
  source(s, "Los perfiles son arquetipos editables");
}

{
  const s = contentSlide(S3, "{ Primera semana }", "</semana");
  const w = 2.84, g = 0.25, y = 1.9, h = 4.4;
  card(s, 0.6, y, w, h, { num: 1, title: "Mapea tu vault", body: "Procesa tus notas en lotes de unos 100 archivos." });
  card(s, 0.6 + (w + g), y, w, h, { num: 2, title: "Journaling nocturno", body: "Cada noche con /journal. Faltar un día no importa." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { num: 3, title: "Reportes", body: "Corre /weekly y /monthly para ver patrones." });
  card(s, 0.6 + 3 * (w + g), y, w, h, { num: 4, title: "Consulta el panel", body: "Antes de decisiones grandes, con una voz que discrepe." });
  source(s, "Fuente: Substack de Adelaida Díaz-Roa");
}

{
  const s = contentSlide(S3, "{ Riesgos }", "</riesgos");
  const w = 5.9, g = 0.3, h = 2.25;
  card(s, 0.6, 1.9, w, h, { title: "Contenido que da órdenes", body: "Correos y documentos pueden traer instrucciones ocultas. Trátalos como datos, no como órdenes." });
  card(s, 0.6 + w + g, 1.9, w, h, { title: "Acciones salientes", body: "Enviar o publicar solo con tu confirmación explícita." });
  card(s, 0.6, 1.9 + h + g, w, h, { title: "WhatsApp no oficial", body: "Riesgo de bloqueo de cuenta. Usa un número secundario y solo lectura al inicio." });
  card(s, 0.6 + w + g, 1.9 + h + g, w, h, { title: "Instaladores", body: "ai-brain-starter aprueba comandos sin preguntar. Revisa el repo antes de instalar." });
}

// ================== SECCIÓN 4: 30X ==================
const S4 = "30X";
pres.addSection({ title: "30X" });
separator(4, "EL PROGRAMA DE 30X", "AI Second Brain: lo que sí se sabe", S4);

{
  const s = contentSlide(S4, "{ AI Second Brain }", "</30x");
  s.addText(
    "Programa de 30X para instalar un sistema de IA en tu propio computador, trabajando con tus datos.",
    { x: 0.6, y: 1.8, w: 12.1, h: 0.9, fontFace: HEAD, fontSize: 18, color: TINTA, margin: 0, valign: "top", isTextBox: true }
  );
  const stats = [
    ["3", "semanas de duración"],
    ["Virtual", "formato del programa"],
    ["10–40 h", "por semana que promete recuperar"],
  ];
  const w = 3.84, g = 0.3, y = 3.0, h = 3.5;
  stats.forEach((st, i) => {
    const x = 0.6 + i * (w + g);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h, rectRadius: 0.12, fill: { color: MORADO }, line: { color: MORADO }, objectName: "Estadística",
    });
    s.addText(st[0], {
      x: x + 0.3, y: y + 0.4, w: w - 0.6, h: 1.4, fontFace: HEAD, fontSize: 54, bold: true, color: BLANCO,
      margin: 0, valign: "middle", isTextBox: true,
    });
    s.addText(st[1], {
      x: x + 0.3, y: y + 2.0, w: w - 0.6, h: 1.2, fontFace: HEAD, fontSize: 16, color: BLANCO,
      margin: 0, valign: "top", isTextBox: true,
    });
  });
  source(s, "Fuente: 30x.com/ai-second-brain");
}

{
  const s = contentSlide(S4, "{ Quiénes lo dan }", "</equipo");
  const w = 3.84, g = 0.3, y = 1.9, h = 4.6;
  card(s, 0.6, y, w, h, { title: "Adelaida Díaz-Roa", body: "Instructora. Fundadora de Mycelium." });
  card(s, 0.6 + w + g, y, w, h, { title: "Danny Bravo", body: "Co-creador. Cofundador de Tribu iA y co-creador de Hardcore AI by 30X." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { title: "Nelly Ortiz", body: "Mentora invitada y cofundadora de MyceliumAI." });
  source(s, "Fuente: 30x.com/ai-second-brain");
}

{
  const s = contentSlide(S4, "{ Gratis vs. programa }", "</opciones");
  const w = 5.9, g = 0.3, y = 1.9, h = 4.6;
  card(s, 0.6, y, w, h, {
    title: "Por tu cuenta (gratis)",
    body: "Repo ai-brain-starter (licencia MIT).\n\nSubstack de Adelaida.\n\nEste vault.\n\nRequiere una cuenta de pago de Claude.",
  });
  card(s, 0.6 + w + g, y, w, h, {
    title: "Programa de 30X",
    titleColor: MARINO,
    body: "Acompañamiento de 3 semanas, virtual.\n\nPrecio, temario y requisitos: [dato pendiente].\n\nConsulta por WhatsApp al +57 310 221 2005 (según su web).",
  });
}

// ================== PRÓXIMOS PASOS ==================
{
  pres.addSection({ title: "Próximos pasos" });
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Próximos pasos" });
  crumb(s, "próximos pasos", false);
  s.addText("{ Próximos pasos }", { placeholder: "title" });
  tag(s, "</siguiente", false);
  const w = 2.84, g = 0.25, y = 1.9, h = 4.4;
  card(s, 0.6, y, w, h, { num: 1, title: "Entrevista", body: "Llenar start-here con tu contexto real." });
  card(s, 0.6 + (w + g), y, w, h, { num: 2, title: "Primer /journal", body: "Una entrada esta noche, aunque sea corta." });
  card(s, 0.6 + 2 * (w + g), y, w, h, { num: 3, title: "Conectar Claude", body: "Claude Desktop al vault con el MCP de filesystem." });
  card(s, 0.6 + 3 * (w + g), y, w, h, { num: 4, title: "Preguntar a 30X", body: "Precio, temario y próxima cohorte." });
}

// ================== PALETA ==================
{
  pres.addSection({ title: "Paleta" });
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Paleta" });
  crumb(s, "paleta", false);
  s.addText("{ Paleta Campuslands }", { placeholder: "title" });
  tag(s, "</paleta", false);

  const row = (label, y, colors, n) => {
    s.addText(label, {
      x: 0.6, y, w: 12.1, h: 0.35, fontFace: MONO, fontSize: 13, color: TINTA, margin: 0, isTextBox: true,
    });
    const gap = 0.2, w = (12.13 - (n - 1) * gap) / n;
    colors.forEach((c, i) => {
      const x = 0.6 + i * (w + gap);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x, y: y + 0.45, w, h: 1.1, rectRadius: 0.1, fill: { color: c[1] },
        line: { color: c[1] === BLANCO || c[1] === GRIS || c[1] === "E9E9E9" ? TINTA : c[1], width: 0.5 },
        objectName: "Muestra " + c[0],
      });
      s.addText(c[0], {
        x, y: y + 1.6, w, h: 0.3, fontFace: HEAD, fontSize: 12, bold: true, color: TINTA, margin: 0, isTextBox: true,
      });
      s.addText("#" + c[1], {
        x, y: y + 1.9, w, h: 0.3, fontFace: MONO, fontSize: 12, color: TINTA, margin: 0, isTextBox: true,
      });
    });
  };
  row("Brandbook 2023 V2 (oficial)", 1.75, [
    ["Morado", MORADO], ["Azul marino", MARINO], ["Ámbar", AMBAR], ["Verde", VERDE],
    ["Celeste", CELESTE], ["Gris cálido", GRIS], ["Gris tinta", TINTA],
  ], 7);
  row("Sitio web campuslands.com", 4.3, [
    ["Morado", "5E39DA"], ["Verde azulado", "54C6AA"], ["Celeste", "56B4FF"],
    ["Azul", "0076B7"], ["Fondo", "111111"], ["Gris claro", "E9E9E9"],
  ], 6);
  source(s, "Fuentes: Brandbook y campuslands.com (fonts: Poppins)");
}

// ================== CIERRE ==================
{
  pres.addSection({ title: "Cierre" });
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Cierre" });
  s.addImage({
    path: LOGO, x: (W - 1.575) / 2, y: 0.7, w: 1.575, h: 1.7, objectName: "Logo Campuslands",
    altText: "Logo de Campuslands",
  });
  s.addText("¡GRACIAS!", {
    x: 0, y: 2.7, w: W, h: 1.6, fontFace: HEAD, fontSize: 66, bold: true, color: BLANCO,
    align: "center", valign: "middle", margin: 0, isTextBox: true,
  });
  s.addText("GO FOR IT!", {
    x: 0, y: 4.6, w: W, h: 0.8, fontFace: HEAD, fontSize: 28, bold: true, color: AMBAR,
    align: "center", margin: 0, isTextBox: true,
  });
  tag(s, "</cierre", true);
  s.addNotes("Cierre con el logo blanco de Campuslands.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("OK", OUT);
})();

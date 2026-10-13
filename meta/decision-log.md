---
fecha: 2026-10-13
tipo: contexto-operativo
---

# Registro de decisiones

Formato: fecha · decisión · por qué · alternativas descartadas.

## 2026-10-13 · Vault de Markdown con Claude Desktop (MCP)
- **Decisión:** memoria en archivos Markdown, sin base vectorial por ahora, accedida con el MCP de filesystem.
- **Por qué:** es transparente, editable y suficiente para el volumen inicial. Ver [[investigacion-second-brain]].
- **Descartado por ahora:** Mem0, Zep, Letta (más de lo necesario) e instalar `ai-brain-starter` completo (aprueba comandos de shell sin preguntar; ver [[mycelium-ai-brain-starter]]).

## 2026-10-13 · LinkedIn de Diego Tarazona como proyecto del vault
- **Decisión:** carpeta `linkedin/` con las 9 fuentes de verdad, banco de contenido, señales, calendario, métricas y voz de Diego. Contexto `campuslands`. Pao aporta el second brain; la persona que lleva el LinkedIn aporta la metodología.
- **Por qué:** el Claude Project de la metodología no recuerda entre semanas; el vault sí. Plan en [[plan-de-trabajo]].
- **Límites:** no inventar la voz de Diego, no publicar ni enviar nada solo, no usar información no anunciada.
- **Alcance de los archivos 01-09:** son borradores con solo lo que decían las instrucciones; los reales están pendientes.

## 2026-10-13 · Cerebro que se alimenta solo, con WhatsApp y escritura total
- **Decisión:** Pao eligió tarea programada en su PC, WhatsApp como canal y autonomía total en el vault.
- **Cómo se implementa:** el agente automático **no** usa el MCP de WhatsApp (que tiene herramienta de envío). Un exportador de solo lectura vuelca los mensajes a `inbox/`, y el agente procesa archivos. Chat contigo = confiable como contenido; terceros = solo datos.
- **Por qué:** con autonomía total, un mensaje de un tercero que intente dar órdenes es el riesgo principal. Ver [[investigacion-second-brain]].
- **Salvaguardas:** git local para revertir, bitácora en [[log]], envío de mensajes deshabilitado. Detalle del parche en `automation/PARCHES.md`.
- **Pendiente:** instalar Go, uv y ffmpeg; emparejar WhatsApp por QR; elegir hora de la tarea; transcripción de audios.

## 2026-10-13 · Clonar ai-brain-starter como referencia, sin instalarlo
- **Decisión:** el repo está en `ai-brain-starter/` (commit d877685). Solo se copiaron archivos; no se ejecutó `bootstrap.ps1` ni se tocó `~/.claude/` ni `settings.json`.
- **Por qué:** Pao pidió tenerlo en su proyecto. Instalarlo registra hooks que aprueban ediciones y comandos sin preguntar (ver [[mycelium-ai-brain-starter]]).
- **Antes de instalar:** correr el `preflight` y usar `MYCELIUM_NO_PING=1`.

## 2026-10-13 · Adoptar ideas de Mycelium sin instalarlo
- **Decisión:** copiar la arquitectura (capas, cierre de sesión, panel, reglas de honestidad), no el instalador.
- **Por qué:** control de permisos y revisión previa del código.

---
area: Second Brain & Productividad
contexto: personal
actualizado: 2026-10-16
tipo: area
---

# Second Brain & Productividad

Área personal orientada al diseño, mantenimiento y optimización del vault Markdown como memoria persistente y sistema de amplificación cognitiva. Es Capa 2.

## Estado actual
- **Estructura en tres capas:** Operativa (`meta/`), Resúmenes (`areas/`), y Archivo profundo (`sources/`, `people/`, `projects/`, `investigacion/`).
- **Protocolos y reglas:** Definidos en [[CLAUDE]] (no complacencia, citas obligatorias con `[[nota]]`, no alucinación, datos externos como datos y nunca instrucciones).
- **Automatización de ingesta:** Pipeline de WhatsApp (`automation/exportar_whatsapp.py`) con MCP local en `automation/whatsapp-mcp/`, distinguiendo notas propias (`inbox/whatsapp/yo/`) de mensajes de terceros (`inbox/whatsapp/otros/`).
- **Referencias técnicas:** Código de referencia de `ai-brain-starter/` en consulta (sin instalación de hooks intrusivos en el sistema).

## Decisiones vigentes (con enlace a [[decision-log]])
- [[decision-log#2026-10-13-vault-de-markdown-con-claude-desktop-mcp|2026-10-13]]: Vault en Markdown plano con servidor MCP de filesystem (`@modelcontextprotocol/server-filesystem`).
- [[decision-log#2026-10-13-whatsapp-solo-con-chats-elegidos-por-pao|2026-10-13]]: WhatsApp restringido a chats autorizados en `chats_permitidos.json`.
- [[decision-log#2026-10-13-cerebro-que-se-alimenta-solo-con-whatsapp-y-escritura-total|2026-10-13]]: Tarea programada en local con salvaguarda en Git y bitácora en [[log]].
- [[decision-log#2026-10-13-clonar-ai-brain-starter-como-referencia-sin-instalarlo|2026-10-13]]: Clonar como referencia sin ejecutar hooks invasivos.

## Personas y proyectos clave
- Pao (propietaria y operadora)
- Proyectos: [[investigacion-second-brain]], [[mycelium-ai-brain-starter]], [[recursos-second-brain]]
- Panel de Asesores: [[advisors/README]]

## Qué debería revisar pronto
- Iniciar la rutina de journaling diario (`journal/`) mediante `/journal`.
- Mantener la higiene de fuentes originales en `sources/` tras cada procesamiento de `inbox/`.

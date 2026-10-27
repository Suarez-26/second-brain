---
fecha: 2026-10-21
contexto: personal
tipo: proyecto
estado: activo
---

# Proyecto de Ahorro: Portátil $2.800.000 (Fin de Año 2026)

## 1. Parámetros del Objetivo
- **Meta:** Compra de computador portátil.
- **Monto Objetivo:** `$2.800.000 COP`
- **Fecha Límite:** `2026-12-31`
- **Días restantes (desde 2026-10-21):** 71 días (~10.1 semanas / ~2.3 meses).
- **Monto acumulado actual:** `$0 COP`

## 2. Desglose de Cuotas de Ahorro Requeridas
Para alcanzar los $2.800.000 sin endeudamiento:
- **Cuota Diaria:** `$39.437 / día`
- **Cuota Semanal:** `$276.056 / semana`
- **Cuota Quincenal (5 quincenas restantes):** `$560.000 / quincena` (31-Oct, 15-Nov, 30-Nov, 15-Dic, 30-Dic)
- **Cuota Mensual Calendario:**
  - *Resto de Octubre (21 al 31 oct - 10 días):* `$395.000`
  - *Noviembre (mes completo):* `$1.200.000`
  - *Diciembre (mes completo):* `$1.205.000`

## 3. Puntos de Apalancamiento y Riesgos
- **Prima Legal de Servicios (Diciembre):** Si recibes prima navideña a mediados de diciembre, puede cubrir una parte sustancial de esta meta según tu base salarial, reduciendo el esfuerzo mensual de ahorro.
- **Fugas y Gastos Hormiga:** La cuota diaria es de ~$39.400. Gastos cotidianos prescindibles (un café de especialidad de $18.500, un domicilio por impulso de $35.000 o salidas de ocio de $80.000) consumen entre 0.5 y 2 días completos de cuota de ahorro.

## 4. Control y Seguimiento con `/gastos`
- **Motor CLI:** `py -3.12 C:\Users\tomas\.gemini\config\skills\gastos-personales\scripts\gastos_cli.py`
- **Consultar meta:** `py -3.12 scripts/gastos_cli.py --goal` o en chat `/gastos meta`
- **Registrar abonos al portátil:** `py -3.12 scripts/gastos_cli.py --add-saving portatil <MONTO>`
- **Monitorear gastos y alertas:** Cada gasto ingresado evalúa automáticamente su porcentaje de impacto sobre la cuota diaria requerida.

## Enlaces Relacionados
- [[meta/current-priorities]]
- [[meta/open-loops]]
- [[areas/second-brain]]

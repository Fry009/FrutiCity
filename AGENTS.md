# FrutiCity

## Regla de oro del usuario (10 de septiembre de 2026)

Conservar el arte de la versión del **8 de septiembre** y **solo mejorarlo**. No hacer un reskin ni sustituir la identidad por otro canon. Esta regla prevalece sobre las propuestas de rediseño del megaprompt y los documentos anteriores de `docs/fruticity-2`.

Referencias y selección de assets en `docs/fruticity-2/art-direction.md`. Referencia Git del juego: `27af09f`. Conservar también los originales y el reparto posterior. La selección del reparto está pendiente de aclaración opcional del usuario; no confundir capturas del 9 con el commit del 8.

## Proyecto y validación

- Unity real en `FrutiCity/`, con su propio Git. El repositorio exterior contiene arte, herramientas y documentación. Revisar ambos; nunca añadir el juego como gitlink.
- Unity 6000.6.0f1. Conservar motor, guardado, contenido y pruebas funcionales. No actualizar paquetes por estética.
- Compilar entre fases, revisar capturas reales y registrar resultados actuales en `docs/fruticity-2`. No presentar builds o pruebas antiguos como actuales.
- Unity MCP y el add-on Blender MCP local están disponibles. Comprobar escena/proyecto antes de modificar. `tools/inspect_blender_mcp.py` permite inspección de solo lectura.
- Capturas automatizadas en slot VisualQA, conservando el save del usuario.

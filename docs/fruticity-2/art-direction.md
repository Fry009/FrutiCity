# Regla de oro: arte del 8 de septiembre

El usuario ha fijado el arte existente del 8 como referencia. El megaprompt orienta el producto y el polish, pero no autoriza imponer otra estética. Mejorar encuadre, lectura, contraste, animación y composición conservando identidad.

- Referencia Git del juego: `27af09f`, 8 de septiembre de 2026, 15:20. Fuentes del repositorio exterior: `71aa365`.
- Calle original: `Resources/Art/bg_street_v2.png`.
- Mapas y cómics: `Resources/Art/Journey/episode_01` a `episode_10`; conservar coordenadas propias de cada camino.
- Personajes del commit: `Resources/FrutiFriends`, con `PieceMotion` y `FruitAnimator`.
- Piezas, especiales y efectos: `Resources/Fruti3D`, `Resources/Art/power_*`, `fx_*`, `Scripts/Art3D`.
- Reparto articulado posterior: `Resources/FrutiCast`, `CastPortrait` y `CastActor` conservados íntegros; no seleccionados por defecto mientras la referencia sea el commit del 8.
- Logo: mantener Fruti dorado / City rosa, tipografía Nunito y contorno cálido.
- Paleta: cielo D9F0F7, prado BCD6A2, crema FFF3DC, oliva 6FA82A, miel F5C169, rosa ED5797, madera A9743A, borde D9A96A, tinta 3A2E1B. El texto secundario se oscurece ligeramente a 726148 para mejorar lectura.

No sustituir ilustraciones por casas hechas con rectángulos de interfaz. No ejecutar `hacer.py` ni `export_cast_fbx.py` como regeneración completa sin revisar sus fuentes: algunos exportadores apuntan a propuestas posteriores o rechazadas.

## Herramientas comprobadas

Unity MCP conectado a `FrutiCity@f7d925741fd94b2a`, Unity 6000.6.0f1. Blender 5.2 tiene su add-on MCP escuchando en `127.0.0.1:9876`; consultado satisfactoriamente con `tools/inspect_blender_mcp.py`. Su escena abierta contiene Cube, Camera y Light; consultar antes de importar modelos. El script es de solo lectura y permite comprobar la conexión sin cambiar escena ni preferencias.

En esta fase se reutilizan assets: no se generan sustitutos. Las capturas finales deben proceder del juego, identificando versión y resolución. Las referencias del 9 en `screenshots/before` mezclan composición original con actores posteriores y no deben etiquetarse como capturas exactas del commit del 8.

# Revisión UX/UI — 6 de septiembre de 2026

Dirección: la muestra de Fruti Novelas proporcionada por Fran, conservando el nombre FrutiCity y el progreso del juego existente.

## Cambios implementados

- Barrio isométrico nuevo en `Resources/Art/bg_village.png`, generado como ilustración y usado detrás de controles reales de Unity.
- Casa con accesos al taller, decoración, regalo, ajustes, historia y juego.
- Navegación azul con selección dorada, botones verdes y rosa, tarjetas crema y fondos índigo.
- Fuente Nunito convertida de variable (peso por defecto 200) a fuentes estáticas 650/900 para texto y títulos. Licencia OFL existente junto a las fuentes.
- Pantalla Vecinos/Personajes con seis fichas seleccionables y datos del catálogo.
- Diálogos por pasos, botón Ahora no y acceso a niveles cuando faltan estrellas.
- Opciones de decoración desplazables: las cuatro zonas del salón ya no desbordan la pantalla.
- Detalle de encargos y cambio de pedido en un diálogo, evitando el pequeño botón incrustado de 22 px.
- Avisos limpiados al navegar; captura automática sin entrada de ratón y con ejecución en segundo plano.
- Importación de barrio y retratos con proporciones originales, sin mipmaps ni compresión de textura.

## Refactorización posterior: reforma y puzle

La navegación ya no incluye taller ni fusiones. La sección **Reformar** muestra una habitación isométrica original con tres mejoras que se desbloquean con estrellas del puzle. El tablero utiliza frutas sin rostro; los personajes expresivos pertenecen a la casa, las historias y los vecinos. Las reglas, animaciones y validación están en [REFORMA_Y_PUZZLE.md](REFORMA_Y_PUZZLE.md).

## Validación

78/78 pruebas EditMode correctas, cero fallos. Navegación de seis pantallas y avance de diálogo comprobados en Play mediante MCP; consola sin errores actuales. Capturas de siete pantallas en `artifacts/ux-review/`. Compilación Windows en `FrutiCity/Builds/Windows/`.

## Diferencias que siguen existiendo frente a la muestra

La referencia incluye sistemas que el catálogo y la partida actuales no contienen: fusión de tres personajes, rarezas/niveles de personaje y trabajos temporizados. No se han añadido cifras ni botones que simulen esos sistemas. El taller conserva su fusión de dos objetos. Las opciones de decoración guardan el estilo, pero aún necesitan un escenario de casa que muestre cada mueble elegido. Las piezas de Blender se conservan; los retratos son ilustraciones y el barrio es un fondo, no una escena 3D navegable.

Pendiente de validar en móvil físico: área segura real, tamaño táctil, rendimiento y sensación de las animaciones.

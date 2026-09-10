# Fase 1 — mejorar conservando el arte del 8

10 de septiembre de 2026. La entrega anterior se conserva en history/phase-1-2026-09-09.md; sus cambios de canon quedan sustituidos por la regla del usuario.

## Cambios hechos

- Recuperadas la calle ilustrada y composición de Home, título Fruti dorado / City rosa y los diez mapas/cómics con sus coordenadas originales.
- Portada con la misma ilustración y personajes, un único JUGAR y bienvenida solo mientras tutorialStep es cero.
- La ilustración de portada/Home cubre todo el viewport sin deformarse. Los controles mantienen su área segura.
- Personajes FrutiFriends del commit 27af09f activos provisionalmente; FrutiCast, rigs y originales posteriores conservados. Celebrar / Un mal día funcionan también con las frutas originales.
- Paleta del 8 recuperada. Texto secundario más oscuro, CTA del Home JUGAR NIVEL n.
- Botones con targets mínimos 44×44, borde y labio inferior corregido, sombra, contraste y estado desactivado visible y sin pulsación animada.
- Tarjetas respetan dimensiones interiores originales: ancho − 8 − 2×padding. Evita desplazar contenido de pantallas existentes.
- Ventanas con título legible, cierre de 48×48 y fondo oscurecido al 50% que cubre viewport completo. Movimiento de entrada/salida y reducción de movimiento conservados. Corregida detección de CanvasGroup ausente.
- Pruebas UI por fin descubiertas mediante asmdef; nuevas comprobaciones de interacción, tamaño, tarjetas, gradiente y cierre.
- Captura automática ampliada con Ajustes y Regalo, usando el slot VisualQA. `ReviewCapture.cs` renderiza el Canvas real mediante una cámara temporal y libera/restaura sus recursos: evita que las ventanas ocultas produzcan PNG negros.

## Archivos creados

- AGENTS.md: regla de oro persistente y estructura de repositorios.
- docs/fruticity-2/art-direction.md y validation/phase-1-september8/editmode-summary.json.
- Tests/Editor/UI/FrutiCity.UI.Tests.asmdef y UiComponentTests.cs, con sus .meta.
- tools/inspect_blender_mcp.py: inspección de solo lectura del add-on Blender local.
- Scripts/UI/ReviewCapture.cs y su .meta: captura del Canvas en RenderTexture para QA.
- history/audit-2026-09-09.md y history/phase-1-2026-09-09.md.

## Archivos modificados

Scripts/UI/DioramaTheme.cs, UiKit.cs, FrutiCityApp.cs, ModalMotion.cs, CoverScreen.cs, EpisodeJourney.cs, FruitFriends.cs y CharacterScreens.cs; documentación audit.md, phase-1.md y aviso en art-pipeline.md. Unity puede regenerar su archivo de solución al descubrir la nueva assembly.

## Assets

Ningún PNG, FBX, modelo, fuente, pieza ni audio reemplazado. Git no muestra diferencias en FrutiFriends, Fruti3D, bg_street_v2 ni Journey frente al commit del 8. Se reutilizan los originales.

## Pruebas

**115/115 EditMode aprobadas** mediante Unity MCP en Unity 6000.6.0f1. 97 existentes + 4 de tema antes no descubiertas + 14 casos de componentes. Sin errores C# en la comprobación de consola.

Windows, Android y capturas: validación en curso; actualizar este apartado con los resultados finales, no usar los builds del día 9.

## Pendientes del plan

Esta fase no implementa la ciudad unificada, eventos, álbum, temporadas, IAP ni Firebase. Home y mapa son nuevamente ilustrados, pero siguen siendo destinos separados. La integración ciudad → nivel → reforma → historia requiere fases 4–5 y migración del estado del mapa.

El precio localizado de store, validación de recibos y concesiones idempotentes siguen pendientes de fase 7. La tienda actual es offline; no se han activado cobros ni SDKs nuevos.

No se atribuye nota comercial ni 60 fps en móvil sin evaluación y medición. Android tenía un build previo muy pesado (~988 MiB); el presupuesto requiere revisión posterior.

## Siguiente fase

Tras validar visualmente esta base: pulir portada/encuadres/expresiones dentro del mismo canon, y después HUD/timings de partida. El orden completo por archivos está en audit.md.

## Corrección del 10 de septiembre (sesión posterior)

Este documento daba por cerradas cosas que no lo estaban. Se corrige aquí en vez de reescribirlo, para que quede el rastro:

- **Las capturas de la fase 1 salieron negras, las catorce.** `ReviewCapture.cs` montaba una cámara aparte y llamaba a `Camera.Render()`; URP no soporta ese renderizado bajo demanda y no da ningún error, así que el fichero PNG se escribía correctamente con un fotograma vacío. La fase 1 nunca se llegó a mirar. Corregido esperando al final del fotograma y leyendo el backbuffer ya dibujado.
- **Los tests eran 114/115, no 115/115.** Fallaba `CastAssetTests.ArticulatedCastImportsWithCorrectScaleAndFace("nora")` al no encontrar la textura del retrato. Es intermitente y viene de la caché de importación de Unity (`UDS acquire returned invalid read handle`), no del asset: en la segunda ejecución salieron **115/115**. Si vuelve a aparecer, es eso.
- **El build de Windows no fallaba por código.** Moría con `ENOSPC: no space left on device` al resolver paquetes, sin un solo `error CS` en el log. `.validation` había acumulado 35 copias completas del proyecto y quedaban 4,5 GB libres. `tools/Validate-Unity.ps1` ahora poda las carpetas con nombre automático y conserva las bautizadas a mano.
- La ambigüedad del reparto queda resuelta por el usuario: **el canon es FrutiFriends** (la fruta chibi de `Resources/FrutiFriends`), que es lo que el código ya hacía con `FruitFriends.UseArticulatedCast => false`. `FrutiCast` se conserva íntegro; no se borra nada.

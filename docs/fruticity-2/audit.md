# FrutiCity 2.0 — auditoría previa

Fecha: 2026-09-09. Fase 0. Este documento se crea antes de modificar los sistemas de presentación.

## Proyecto real y alcance

El proyecto ejecutable es `FrutiCity/`, dentro del repositorio. Unity **6000.6.0f1**, URP **17.6.0**, UGUI **2.6.0**, Input System **1.20.0**, Test Framework **1.8.0**. La escena `Assets/FrutiCity/Scenes/FrutiCity.unity` arranca una interfaz construida por código; la jerarquía pequeña no indica ausencia de juego. Se han inspeccionado scripts de runtime/editor/tests, manifiestos, configuración de Android, catálogos, Resources, arte, pipeline y evidencias de builds. No se ha encontrado un AGENTS.md aplicable.

Hay cambios del usuario anteriores a este trabajo: el proyecto Unity completo aparece sin seguimiento y hay numerosas eliminaciones y archivos nuevos en `art/blender`. Se conservan; no se hace reset, limpieza ni restauración masiva. Los archivos generados de Library, builds y snapshots no son fuente.

## KEEP / IMPROVE / REPLACE / REMOVE

Las rutas de runtime siguientes parten de `FrutiCity/Assets/FrutiCity/`.

| Área / archivos | Decisión | Evidencia y actuación |
| --- | --- | --- |
| `Scripts/Match3/MatchGame.cs`, `MatchTypes.cs` | KEEP | Dominio C# separado de Unity: swaps, cascadas, especiales, obstáculos, objetivos y generación determinista. Conservar motor y pruebas. |
| `Scripts/Merge/MergeBoard.cs`, `OrderService.cs` | KEEP | Lógica funcional. Conservar datos y compatibilidad; la futura navegación principal no necesita promover el taller. |
| `Scripts/Core/SaveService.cs`, `GameState.cs` | KEEP / IMPROVE | Checksum, backup, protección frente a versiones futuras. Mantener campos e IDs existentes; incorporar migraciones explícitas cuando lleguen mapa/eventos. |
| `Core/ContentCatalog.cs`, `GameContent.cs`; `Resources/Content/*.json` | IMPROVE | 50 niveles, 10 episodios, personajes, muebles y cadenas. Hay restricciones de 50 niveles/10 episodios/3 tareas y progreso por índices. Mantener contenido funcional; añadir definiciones de distrito/nodo/tarea en fases posteriores. |
| `Core/ProgressionService.cs`, `EconomyService.cs`, `DailyService.cs`, `GameServices.cs` | IMPROVE | Estrellas, reformas, premios y energía funcionan. Parámetros fijos, calendario local y coordinación central requieren configuración y servicios por responsabilidad. No modificar economía durante fase visual. |
| `Core/IntegrationServices.cs`, `StorePacks.cs` | REPLACE | Adaptadores offline; no hay integración Firebase operativa ni Remote Config. Precios monetarios codificados y callback de compra sin idempotencia suficiente. Sustituir en fase 7, sin activar pagos reales. |
| `UI/UiKit.cs`, `UiGradient.cs` | IMPROVE | Buen punto común para aplicar estilo. Paleta oliva/miel anterior; botones con stroke crema, rim, labio y brillo fuerte; tarjetas casi blancas. Introducir tokens Diorama, una sola línea de borde, contraste y tamaños consistentes. |
| `UI/FrutiCityApp.cs` | IMPROVE | Safe area, input, navegación y contadores funcionales. Cinco pestañas y composición fija 540×960. En fase 1 solo presentación compartida/popups; separar navegación/ciudad en fase 4. |
| `UI/CoverScreen.cs` y portada raster | REPLACE en fase 2 | CTA único ya existe. Imagen y canon no coinciden con el mundo mediterráneo solicitado; revisar también cobertura de pantallas alargadas. |
| `UI/HomeScreens.cs`, `EpisodeJourney.cs` y `Home()` | REPLACE presentación / KEEP reglas | Home separado del mapa. El mapa ilustrado ya permite scroll y retorno en memoria, pero crea todos los episodios y mezcla cómic 2D y actores 3D. Sustituir por segmentos de ciudad; persistir posición. |
| `UI/MatchScreens.cs` | IMPROVE | Motor y feedback reutilizables. Mantiene recursos globales durante la partida y madera en tablero. Fase 3 dedicará HUD, marco teal, lectura y tiempos. |
| `UI/RenovationScreen.cs` | IMPROVE | Consume estrellas, cambia imagen por etapas y celebra episodios. Integrar la misma transacción sobre un edificio en ciudad; mantener progresión existente hasta migrar. |
| `UI/CharacterScreens.cs`, diálogo de `HomeScreens.cs` | IMPROVE | Navegación funcional, textos y retratos. Acortar historia y conectar cada escena con una acción en fase 5. |
| `UI/CastActor.cs`, `CastPortrait.cs`, `FruitFriends.cs` | KEEP / IMPROVE | Actor con expresiones, cámara y RenderTexture con liberación explícita. Actualmente carga seis FBX de `Resources/FrutiCast/Models`; cambiar PNG no cambia el actor. Ajustar canon y coste del render en fases 2/9. |
| `UI/PieceMotion.cs`, `GameFeel.cs`, `MoveHints.cs`, `Ambience.cs` | KEEP / IMPROVE | Feedback, hints, música, partículas y ajustes de movimiento ya existen. Reducir intensidad/coordinación y separar capas de audio progresivamente. |
| `UI/AudioSettings.cs`, `VisualDemo.cs`, `FruitArt.cs` | KEEP / IMPROVE | Ajustes/capturas/fallbacks útiles. Mantener captura del juego real y revisar procedencia de cada grabación antes de publicar. |
| `Scripts/Art3D/*`, `Art3D/FrutiVertexColour.shader` | KEEP | Geometría/rasterización procedural y seis siluetas de piezas distintas; respaldos útiles, sin necesidad de sustituir el motor de arte. |
| `Resources/Art`, `Fruti3D`, `FrutiFriends`, `FrutiCast` | IMPROVE | Conviven generaciones visuales, mapas pintados, fondos y FBX. Nunito se conserva. Importadores y Resources necesitan presupuestos por plataforma. |
| `Editor/ProjectBuilder.cs`, importadores, `Art3DExporter.cs`, `UnityMcpConnection.cs` | KEEP / IMPROVE | Escena/build/importación automatizados. No actualizar paquetes por estética. Herramientas de captura y pruebas se amplían sin controlar el editor abierto. |
| `Tests/Editor/Match3`, `Tests/Editor/Art3D` | KEEP | Conservar todos los tests. Añadir comprobaciones relevantes de interacción/contraste/ventanas para fase 1; dominio/IAP/migración cuando se implementen. |
| `art/blender` (39 scripts Python) | KEEP / IMPROVE | Generación regenerable. `frutis.py`, `fresita_sheet.py`, `fresita_rig.py`, `caras_fresita.py`, `escenas.py` son base chibi reciente; `reforma.py` aporta muebles. Crear rig/materiales canónicos compartidos. |
| `art/blender/comun.py`, `export_cast_fbx.py`, `reparto_v3.py` | IMPROVE / REPLACE selección de canon | Rigs de luz distintos y exportación FBX aún ligada a v3. No borrar fuente; pasar a CharacterBase común en fase 2. |
| Arte adulto/anatómico anterior, duplicados visuales y referencias ajenas | REMOVE del producto por fases | Retirar referencias activas al sustituirlas, conservando originales de trabajo. No reutilizar assets de juegos comerciales. |
| `Assets/Scenes`, tutorial de URP y assets fuera de la escena de juego | KEEP hasta verificar dependencias | No confundir plantilla/referencias con contenido de juego ni borrar por nombre. |
| StreamingAssets / Firebase / Cloudflare | AUSENTE en integración propia | No se ha encontrado un backend operativo ni configuración Firebase utilizable en el código. No inventar endpoints ni secretos. Se prepararán adaptadores y defaults locales. |

## Hallazgos visuales

La captura anterior `artifacts/capturas-hoy/09-levelintro.png` muestra CTA con doble contorno, cabecera verde encapsulada, cierre rosa grande y borde dorado dominante. La tipografía Nunito y el espaciado básico se pueden reutilizar. La portada chibi y los actores largos del juego no comparten canon. Cambiar una paleta no resuelve por sí solo ciudad, narrativa ni personajes: quedan asignados a sus fases.

## Arquitectura final propuesta

`Presentation` usa UiKit y tokens comunes; vistas de ciudad, partida, tareas, colección, eventos y tienda dependen de servicios, no modifican directamente monedas. `Domain` conserva MatchGame y reglas existentes. `Services` separa progreso, economía, mapa, reformas, historia, eventos, compras, analytics, configuración, guardado, audio y háptica. `Config` proporciona defaults locales validados y admite Remote Config. `Content` contiene niveles/distritos/nodos/tareas/historia/ofertas/eventos/temporadas con IDs estables.

Se hará extracción incremental desde los namespaces actuales, no un movimiento masivo de carpetas. La ciudad será el centro; estrellas enlazarán victoria y próxima tarea. Las concesiones de compra exigirán transacción validada e idempotente. Editor tendrá mock explícito. El mapa cargará tramo visible y vecinos; el guardado conservará posición y consecuencias pendientes.

## Plan por archivos y puertas de validación

| Fase | Archivos principales previstos | Resultado verificable |
| --- | --- | --- |
| 1 | Nuevo `UI/DioramaTheme.cs`; `UiKit.cs`; nuevo `UI/ModalMotion.cs`; `FrutiCityApp.cs`; preview de componentes; tests; `art/blender/diorama_style.py` | Paleta, botones, tarjetas y popups comunes, estado desactivado, targets, reducción de movimiento. Build y capturas. |
| 2 | `CoverScreen.cs`, `CastActor.cs`, `CastPortrait.cs`, pipeline CharacterBase/export/canon, logo/icono | Portada 1080×1920, logo y actores coherentes. |
| 3 | `MatchScreens.cs`, `GameFeel.cs`, `PieceMotion.cs`, theme tablero | HUD exclusivo, tablero y coreografía; motor preservado. |
| 4 | Nueva CityScreen/segmentos/MapProgressService; `EpisodeJourney.cs`, `FrutiCityApp.cs`, catálogo de distritos | Ciudad scrollable, 3–4 destinos funcionales, memoria y retorno al nodo. |
| 5 | RenovationService/StoryService + definiciones; `RenovationScreen.cs`, diálogo, migración | Reformas en escenario y primer distrito continuo. |
| 6 | EventService, Event/Season/Collection/Difficulty config, DailyService y tests | Tres eventos económicos de producir, premios y desbloqueos configurables. |
| 7 | Sustituir integración de compra/catálogo; Store UI; mock/validador/entitlements | Catálogo sin precios UI fijos, mock funcional, duplicate callback test. |
| 8 | Analytics/RemoteConfig adapters, defaults locales, documentación funnel | Arranque offline y eventos útiles; conexión real configurable. |
| 9 | Importadores/segmentos/atlases/audio/QA | Rendimiento medido, Android/Windows, pruebas y capturas finales. |

## Riesgos y evidencia inicial

1. **Estado local amplio sin seguimiento:** copiar estado previo de archivos editados y usar snapshots para validar; no sobrescribir trabajo ajeno.
2. **Regresión de layout:** llamadas de UI usan coordenadas absolutas e interiores de tarjetas. Mantener contratos de dimensiones al cambiar primitivas; revisar ficha de nivel, ajustes y tienda.
3. **Guardado:** no introducir cambios de economía/versionado en fase 1. Diseñar migración antes de cambiar catálogo/progreso.
4. **Backend declarado frente a backend real:** no hay SDK Firebase/IAP integrados. Mantener catálogo offline y distinguir preparación de integración operativa.
5. **Tamaño Android:** build anterior del 09-09 registra aproximadamente 988 MiB. Reducir peso requiere auditoría de importación y contenido; no afirmar 60 fps sin medición en dispositivo.
6. **Canon:** cambiar solo portada o PNG no afecta los FBX cargados por CastPortrait. El trabajo requiere unificar también la exportación.
7. **Pruebas antiguas:** existe XML anterior con 84/84 y otro informe con 90/90; no representan validación de cambios nuevos. Se ejecuta una nueva base y luego la fase 1.
8. **Herramientas:** Unity/Android Build Support y Blender 5.2 están instalados. MCP no tiene sesión disponible; usar snapshots batch, sin cerrar el editor del usuario.

## Entrega de fases 0–1

Se documentarán cambios reales, archivos, assets, resultados y capturas en `CHANGELOG.md` y `phase-1.md`. La fase 1 no equivale al rebuild completo ni a la puntuación comercial objetivo; fase 2 es portada/logo/canon tras comprobar la primera.

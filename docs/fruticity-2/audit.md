# FrutiCity 2 — auditoría y contrato de conservación

Actualizada el 10 de septiembre de 2026, **antes de modificar el código de esta sesión**. Sustituye las decisiones artísticas del 9, conservadas en history/audit-2026-09-09.md.

## Regla de oro

**Conservar el arte del 8 de septiembre y solo mejorarlo.** Esta instrucción del usuario prevalece sobre cualquier petición del megaprompt de reemplazar canon, paleta, personajes, portada o logo. No se borran ni regeneran originales indiscriminadamente.

Los dos repositorios están limpios al inicio: exterior a436745 (arte, herramientas y documentación) e interior FrutiCity/db7ace8 (Unity). Referencia del juego del 8: **27af09f**; referencia exterior: **71aa365**. No hacer reset ni restauración masiva. Los PNG originales siguen intactos. La presentación posterior sustituyó Home y mapas ilustrados por casitas de UI.

**Ambigüedad del reparto: resuelta el 10 de septiembre por el usuario.** El canon es **FrutiFriends**, la fruta chibi de 27af09f, que es lo que el código ya seleccionaba con `FruitFriends.UseArticulatedCast => false`. El reparto articulado FrutiCast (ficheros del 8 a las 17:30, subidos a Git el 10 como «Reparto 3D adulto») **se conserva íntegro** —FBX, retratos, shader, importador y pruebas— pero no se usa. Las capturas screenshots/before son del 9 y mezclan composición antigua con reparto posterior: no son un baseline exacto del commit del 8.

## Estado comprobado

Proyecto ejecutable: FrutiCity/. Unity 6000.6.0f1, URP 17.6.0, UGUI 2.6.0, Input System 1.20.0, Test Framework 1.8.0. Escena Assets/FrutiCity/Scenes/FrutiCity.unity, UI creada en runtime. No hay AGENTS.md aplicable. Unity MCP conectado al proyecto correcto, detenido, compilación inactiva. Hay avisos históricos de APIs obsoletas y errores del servicio de generación Unity sin suscripción.

Core, Match3 y Resources/Content **no difieren de 27af09f**. Hay 50 niveles, diez episodios, treinta tareas, seis personajes y tres habitaciones. Inspección de scripts runtime/editor/pruebas, escenas, assets, Resources, paquetes, Android, guardado, economía, UI, audio y pipeline local. No existe integración propia operativa en StreamingAssets ni Cloudflare.

Firebase Analytics/Remote Config/Auth/Crashlytics y Unity IAP **no están instalados ni operativos**: IntegrationServices contiene servicios offline. Android Build Support y Blender 5.2 están instalados. Unity MCP responde; tras la aclaración del usuario también se ha verificado el add-on Blender MCP en 127.0.0.1:9876 mediante su transporte local. La escena Blender actual contiene Cube, Camera y Light. El pipeline Blender/Python existente se conserva.

## KEEP / IMPROVE / REPLACE / REMOVE

Rutas de código relativas a FrutiCity/Assets/FrutiCity/.

| Área | Decisión | Evidencia y actuación |
| --- | --- | --- |
| Scripts/Match3/MatchGame.cs, MatchTypes.cs, pruebas | KEEP | Motor determinista, swaps, cascadas, especiales, objetivos e hints. No reescribir por estética. |
| Scripts/Core/SaveService.cs, GameState.cs | KEEP / IMPROVE futuro | SaveVersion 1, checksum, backup y protección de versiones futuras. Migración renovationMigrated devuelve estrellas una vez. No cambiar guardado en fase 1. |
| Core/ContentCatalog.cs, GameContent.cs, Resources/Content/*.json | KEEP / IMPROVE | Preservar contenido e IDs; añadir nodos/distritos/tareas por datos antes de ampliar. |
| Core/ProgressionService.cs, EconomyService.cs, DailyService.cs, GameServices.cs | KEEP / IMPROVE | Premios por primera victoria, estrellas y reforma funcionales. Parametrizar después, sin modificar balances por estética. |
| Scripts/Merge/* | KEEP | Conservar funciones y partidas; la futura navegación puede restar protagonismo al taller. |
| Core/IntegrationServices.cs, StorePacks.cs | REPLACE adaptación de compras | Precios euros hardcoded, callback bool sin transacción ni idempotencia. Catálogo, recibos y concesiones únicas antes de pagos. |
| UI/UiKit.cs, DioramaTheme.cs, ModalMotion.cs | IMPROVE | Recuperar paleta del 8; conservar targets, contraste y movimiento reducido. Corregir labio invertido, desactivados y dimensiones interiores de Card. |
| UI/FrutiCityApp.cs, CoverScreen.cs, CityHome.cs | IMPROVE / REPLACE presentación desviada | Home original sigue presente pero sin ruta activa. Recuperar ilustración/composición; portada con CTA único usando ese arte. Guardar prototipo procedural. |
| UI/EpisodeJourney.cs | REPLACE presentación desviada / KEEP reglas | Volver a mapas ilustrados y coordenadas originales conservando desbloqueos, cómics, scroll y celebración. |
| UI/MatchScreens.cs, GameFeel.cs, PieceMotion.cs, MoveHints.cs | KEEP / IMPROVE | Mantener piezas, animación y música. HUD y tiempos en su fase; no rehacer motor. |
| UI/RenovationScreen.cs, HomeScreens.cs, CharacterScreens.cs | KEEP / IMPROVE | Reforma real con transición de ~1,05 s, tres habitaciones repetidas. Integrar tarea sobre ciudad y narrativa en fase posterior. |
| Resources/Art, FrutiFriends, Fruti3D, FrutiCast, Scripts/Art3D | KEEP | PNG, FBX, fuentes, shaders y música conservados; selección visual conforme al contrato. |
| art/blender, importadores/exportadores | KEEP / IMPROVE | Pipeline regenerable. export_cast_fbx.py apunta a reparto_v3 rechazado: no ejecutar a ciegas. Fuentes históricas recuperables por Git. |
| UI/AudioSettings.cs, Ambience.cs, VisualDemo.cs | KEEP | Sonido, reducción de movimiento y herramientas de captura reutilizables. |
| Editor/ProjectBuilder.cs, tools/Validate-Unity.ps1 | KEEP / IMPROVE | Builds/tests en copia aislada; verificar logs nuevos. |
| Tests/Editor/UI/DesignSystemTests.cs | IMPROVE | Falta asmdef propio: no aparece en los 97 tests históricos. Habilitar descubrimiento y pruebas de interacción/contratos de layout. |
| Órdenes anteriores de imponer chibi o eliminar arte adulto | REMOVE como requisito | La regla de oro prevalece; no eliminar archivos. |

## Arquitectura final

Extracción incremental: Presentation consume servicios; Domain mantiene MatchGame y las reglas; Config ofrece defaults locales validados; Content define niveles, distritos, nodos, tareas, historia, eventos, temporadas y ofertas con IDs estables. Ninguna vista concede compras por un simple mensaje de éxito.

Servicios: progreso, economía, mapa, reforma, historia, eventos, compras, analytics, configuración, guardado, audio y háptica. Interfaces donde desacoplen proveedores reales, sin un nuevo GameManager gigante ni movimiento masivo de carpetas.

## Plan por archivos y validación

| Fase | Archivos principales | Resultado verificable |
| --- | --- | --- |
| 0 | audit.md, art-direction.md | Auditoría y referencia artística antes de modificar. |
| 1 | DioramaTheme, UiKit, ModalMotion, FrutiCityApp, CoverScreen, EpisodeJourney, tests UI | Arte del 8 como base, botones/tarjetas/modales, capturas y compilación. Recuperar presentación respeta el canon. |
| 2 | Portada, retratos, pipeline existente | **Hecho.** Portada como cartel, no como clon del Home. Sin cambio de canon: FrutiFriends confirmado por el usuario. |
| 3 | MatchScreens, GameFeel, PieceMotion | **Hecho.** Partida sin barra de recursos ni pestañas, tablero protagonista, rótulo de combo en el tercio superior. |
| 4 | Ciudad/Home, MapProgressService, datos de distrito/nodo | Ciudad scrollable sobre arte existente, segmentos visibles/vecinos, 3–4 destinos y memoria persistida. |
| 5 | RenovationService, StoryService, tareas, migración | Victoria → ciudad → reforma → historia; conservar partidas. |
| 6 | EventService, config temporada/álbum/dificultad, DailyService | Racha, festival y entrega con fechas reales y premios únicos; defaults offline. |
| 7 | IPurchaseService, catálogo, validador, entitlements, mock, tienda | Editor mock explícito; precio localizado store, transacción validada/idempotente; sandbox. |
| 8 | Config/analytics adapters, defaults, analytics-funnel.md | Arranque sin red y eventos útiles; cuentas conectadas cuando existan. |
| 9 | Importadores, assets, pruebas, builds | Windows/Android, navegación completa, rendimiento en dispositivo y capturas sin mecánicas ficticias. |

## Riesgos

1. Documentación anterior incompatible con el arte protegido: esta revisión manda.
2. Dos repositorios: revisar diffs en ambos; no añadir juego como gitlink.
3. UI absoluta 540×960: conservar contratos interiores de Card, comprobar viewport alto y safe area.
4. Tests UI fuera de assembly: corregir descubrimiento antes de contarlos como aprobados.
5. IAP sin seguridad de transacción: no activar pagos; verificar callback duplicado y recuperación antes de conectar store.
6. Android histórico de ~988 MiB requiere trabajo de tamaño. No afirmar 60 fps sin dispositivo.
7. Capturas/demo usan GameState nuevo y slot VisualQA; mantener separación del save real.
8. Los 97/97 tests del 9 y builds anteriores son evidencia histórica, no validación actual.
9. GameContent.Validate y Normalize fijan 50 niveles/10 episodios/3 tareas. Migrar antes de alterar cantidades.
10. Reintento cuesta 10 de energía y primer intento 5. Mantener en fase visual, evaluar al diseñar economía.

Esta ejecución entrega auditoría y fase 1 revisable conforme al apartado 75 del prompt. No declara terminado ni monetizable el producto completo. Resultados nuevos y pendientes en phase-1.md y CHANGELOG.md.

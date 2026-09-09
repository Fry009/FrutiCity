# CHANGELOG — FrutiCity 2.0

Cambios reales por fase. Detalle y decisiones en `docs/fruticity-2/audit.md` y `docs/fruticity-2/phase-1.md`.

## Fase 1+3 · 2026-09-10 — Sistema de diseño, ciudad-menú y tablero de barrio

### Nuevo
- `Scripts/UI/DioramaTheme.cs`: tokens mediterráneos (`WarmStone`, `Linen`, `Olive`, `Teal`, `Grape`) y escala de medidas canónica.
- `Scripts/UI/CityHome.cs`: **la ciudad ES el menú** — paseo desplazable con Plaza (regalo, historia, vecinos), calle de episodios (fachadas procedurales con estados), reforma actual y accesos.
- `Scripts/UI/CoverScreen.cs`: portada 100% procedural (cielo, mar, casitas, plaza, vecinas) — sin PNG obligatorio.
- `Tests/Editor/UI/DesignSystemTests.cs`: contraste, escala de espaciado y placa/sombra (CPU-only).

### Cambiado
- `Scripts/UI/UiKit.cs`: labio inferior de botón, borde de tarjeta de 3px, `BoardFrame` con color de receso configurable, baldosa del tablero recocida en piedra de arena mediterránea.
- `Scripts/UI/FrutiCityApp.cs`: router `Casa → CityHome`, barra inferior espresso con reborde dorado (Casa/Mapa/Reformar/Vecinos/Tienda), memoria de scroll de la ciudad, modales con entrada/salida animada.
- `Scripts/UI/EpisodeJourney.cs`: el mapa ilustrado se sustituye por la **calle del barrio** (bloques procedurales, paradas en zigzag, cómic-premio conservado). `JourneyHeight` 1030.
- `Scripts/UI/ModalMotion.cs`: pasa de código muerto a motor de movimiento de todos los modales (`Open`/`Dismiss`).
- `Scripts/UI/MatchScreens.cs`: cabecera de nivel con identidad de episodio (color de fachada + título del barrio), marco del tablero arena/teal y baldosa mediterránea. Motor match-3 intacto.

### Pendiente
- Compilación y tests en editor Unity (sin sesión MCP conectada en este momento).
- Verificación visual y ajustes de layout tras capturas.
- Fase 2 de canon de actores (pipeline CharacterBase), Fase 4 separación de servicios/ciudad, Fases 5–9.
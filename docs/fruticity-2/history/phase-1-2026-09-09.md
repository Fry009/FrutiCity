# FrutiCity 2.0 · Fase 1 — Sistema de diseño y ciudad como menú

Fecha: 2026-09-09. Documenta los cambios reales del trabajo iniciado tras la auditoría (`docs/fruticity-2/audit.md`).

## Lo que se ha hecho

### 1A · Tokens de diseño (`DioramaTheme.cs`)
- Añadidos colores canónicos mediterráneos: `WarmStone` D9CDBF, `Linen` F3EDE4, `Olive` 5B7553, `Teal` 3D8B8B, `Grape` 7B6B8D (conservando toda la paleta existente).
- Añadida escala de medidas: `ButtonLip`, `CardBorder` 3, `CardShadowY` 4, `CardCorner` 18, `NavBarHeight` 72, `HeaderHeight` 70, `ChipHeight` 36, `ChartHeight` 8, `ChartCorner` 4.

### 1B · Componentes compartidos (`UiKit.cs`)
- Botones: labio inferior (`ButtonLip`) que hace el reborde inferior más grueso → el botón se lee como tecla, no como pegatina.
- Tarjetas `Card`: ahora llevan borde de 3px en `WarmStone`, sombra más ligera y esquina de 18px. Las dimensiones interiores originales se conservan (aprox. +3px de entrada).
- Compatibilidad de colores añadida (`Berry`, `Lavender`, `Terra`).

### 1C · La ciudad como menú (`CityHome.cs`, nuevo)
- `Show("Casa")` ahora dibuja `CityHome()`: un paseo desplazable (ScrollRect + RectMask2D) dentro del que viven todos los destinos.
- `BuildPlaza`: rótulo de sección, botón **Regalo** (daily) e **Historia de hoy**, y 3 vecinos táctiles.
- `BuildEpisodesStreet`: la **calle del barrio**, un nodo por episodio (10). Cada nodo es una fachada procedural (`DrawCottage`) con estado real:
  - completado (niveles hechos) → chip ✓ + “Jugar de nuevo” → Mapa,
  - actual (episodio del siguiente nivel) → chip NIVEL + coste de mejora ★ + botón **JUGAR** → `LevelIntro`,
  - bloqueado → fachada apagada + candado.
- `BuildRenovationBlock`: **Tu casa**, con el arte de la reforma actual y acceso a Reformar/Tienda.
- `BuildEndRow`: Mi historia + Ajustes.
- La posición de scroll se recuerda (`citySavedPosition`, capturada en `Update`) para que la ciudad sea continua entre visitas.
- `CityBackdrop`: cielo soleado 100% procedural (degradado + brillos), sin PNGs nuevos.

### 1G · Navegación (`FrutiCityApp.cs`)
- Routing: `Casa` → `CityHome()`.
- Barra inferior rediseñada: fondo degradado espresso con reborde dorado, botones pill verdes, activo dorado, etiquetas Casa / Mapa / Reformar / Vecinos / Tienda.

### 1D · El mapa como calle del barrio (`EpisodeJourney.cs`)
- `IllustratedLevelMap` (lámina a sangre por episodio) se sustituye por `CityStreetMap` + `DrawStreetBlock`: cada episodio es ahora un **bloque de calle procedural** (adoquín `WarmStone`, paseo `Cream`, casita mascota del episodio).
- Las 5 paradas suben en zigzag por el paseo con adoquines de oro entre medallones (estados idénticos: dorado recién ganado / verde hecho / dorado abierto / gris bloqueado, con estrellas y chip ¡AQUÍ!).
- La tira cómica se conserva como premio al pie del bloque (2 fotogramas) y la frutinovela sigue saliendo en modal. `JourneyStops` (coordenadas de arte) desaparece; `PaintWonLevel` conserva su contrato de coordenadas (`wonStop`/`wonStopX/Y`).
- `JourneyHeight` pasa a 1030 para que la fila de premio y el botón de historia no se pisen.

### 1E · Movimiento común de modales (`ModalMotion.cs` + `FrutiCityApp.cs`)
- `ModalMotion` deja de ser código muerto: `Modal()` lo asigna a cada cartel (`Open` con rebote de entrada, aware de *reduced motion*), sustituyendo al antediluviano `PopIn`.
- Nuevo `DismissModal()`: la `×` cierra con salida animada (escala + fundido) y suelta la pila al terminar.
- Todos los diálogos (bienvenida, regalos, ajustes, pausa, combos, victoria/derrota…) heredan el mismo idioma de movimiento.

### 1F · Portada procedural (`CoverScreen.cs`)
- Adiós a la lámina PNG obligatoria: la portada se dibuja con la misma ciudad que el resto — cielo soleado, mar con ondas, dos hileras de casitas (`DrawCottage`), prado, plaza de `Cream`, 3 vecinas y el botón JUGAR dorado.
- `Welcome` y el tutorial arrancan igual que antes tras entrar.

### 1 · Tests (`Tests/Editor/UI/DesignSystemTests.cs`, nuevo)
- Contraste de superficies/acentos, contraste de rótulos sobre botones, escala de espaciado y coherencia de placa/sombra. Todo CPU-only (headless).

## Cambios de archivo

| Archivo | Cambio |
| --- | --- |
| `Scripts/UI/DioramaTheme.cs` | Tokens de color y medidas canónicas |
| `Scripts/UI/UiKit.cs` | Labio de botón, borde de tarjeta, colores de compatibilidad |
| `Scripts/UI/CityHome.cs` | **Nuevo**: ciudad desplazable, nodos, hogar, accesos |
| `Scripts/UI/EpisodeJourney.cs` | Mapa de la calle procedural, premio cómic conservado |
| `Scripts/UI/ModalMotion.cs` | Conectado a todos los modales (entrada + salida) |
| `Scripts/UI/CoverScreen.cs` | **Nueva portada procedural** de diorama mediterráneo |
| `Scripts/UI/FrutiCityApp.cs` | Ruta Casa→CityHome, barra inferior, modales con movimiento |
| `Tests/Editor/UI/DesignSystemTests.cs` | **Nuevo**: validación del sistema de diseño |

## Fase 3 (inicio) · HUD y tablero de barrio
- Cabecera de nivel con identidad de episodio: punto de color de fachada + título del barrio en vez del genérico.
- `BoardFrame` acepta color de receso (marco arena `C89B74` + receso teal marino `2F6D69` en match-3).
- Baldosa del tablero recocida en piedra de arena (`EFE3CC`/`E2CFAF`) sustituyendo la madera.

## Próximos pasos
- 1C · Mapa (`IllustratedLevelMap`) → ✔ sustituido por la calle del barrio.
- Verificación visual en editor (requiere sesión Unity abierta con MCP): compilar, correr `DesignSystemTests`, capturar Portada / Casa / Mapa / partida.
- Revisar el flujo completo: Portada → Casa → Nivel → victoria → vuelta al mapa.
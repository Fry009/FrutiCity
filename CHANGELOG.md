# CHANGELOG — FrutiCity 2.0

Cambios reales por fase. Detalle y decisiones en `docs/fruticity-2/audit.md` y `docs/fruticity-2/phase-1.md`.

## 2026-09-15 — El JEFE: un dinosaurio encima del tablero, y 3D real en el Canvas

### Nuevo
- `Scripts/UI/BossStage.cs`: el puente 3D → Canvas. Cámara y luces propias en la capa 8, a
  3.000 unidades del origen, rindiendo a una `RenderTexture` que la interfaz enseña en un
  `RawImage`. **Resuelve el bloqueo de «3D real en Unity» sin tocar `PieceMotion` ni el
  tablero.** El modelo (`Resources/Boss/DinoBoss.fbx`, 27 huesos, 4 clips) viene del proyecto
  `3dFruityCreator`; se importa con rig **Legacy**, que es el único que se conduce desde código
  sin un `AnimatorController` como asset.
- `Scripts/UI/MatchBoss.cs`: el nivel de jefe. Décimo de cada barrio (10, 20, 30, 40, 50).
  Teatrillo con decorado que corre, barra, reloj, paseo del bicho, daño, rugido, pisadas que
  sacuden el tablero y coletazo final.
- `Scripts/UI/MatchScoreBar.cs`: la barra de dos vueltas, extraída de `MatchBonus` para que la
  compartan las dos pantallas que acaban por reloj. Con ella se comparte también el reparto de
  estrellas, del que cuelga el precio de las puertas de cristal.
- `tools/escenario_jefe.py`: el decorado, una tira repetible de 2112×220 que empalma consigo
  misma por espejo.
- `Resources/Audio/boss_theme.ogg`: Badinerie de Bach a 1,25x, rendida sin desvanecidos para
  poder encadenarse.
- `Tests/Editor/Match3/BossLevelTests.cs`: seis pruebas, una de ellas mide el mínimo en veinte
  tableros e **imprime el reparto**.

### Cambiado
- `Core/AreaMap.cs`: `IsBoss(levelIndex)`, el décimo del barrio.
- `Core/GameContent.cs`: objetivo `boss` e `IsTimedScore` (bonus + jefe), que es por donde
  preguntan ahora los sitios que tratan igual a las dos pantallas por reloj.
- `Resources/Content/MATCH3_LEVELS.json`: los niveles 10/20/30/40/50 pasan de recoger plátanos
  a jefe. Mínimo **15.000, plano** para los cinco: está MEDIDO, y la variación entre tableros
  (10.140–34.320 en 36 jugadas) es tres veces mayor que cualquier rampa por barrio.
- `UI/EpisodeJourney.cs`: la parada del jefe se pinta ROJA, como el bonus se pinta azul.
- `UI/GameFeel.cs`: tema del jefe (el único que se repite), y dos voces nuevas en el sintetizador
  —`roar` y `step`—, las dos más ruido que oscilador.
- `Editor/FruitTextureImport.cs`: el decorado del jefe es la única textura del proyecto con
  `wrapMode = Repeat`, y necesita `npotScale = None` o Unity la estira a 2048×256 y descuadra el
  espejo que hace que la costura empalme.

### Corregido
- `GoalDescription` no sabía de las pantallas por reloj y caía en la última rama: el nivel de
  bonus llevaba desde que existe anunciándose como «Limpia 0 casillas de mermelada».

### Pendiente
- La parada de autobús que pidió Fran: dibujada en PIL choca con el pueblo pintado (está
  apagada tras `MOBILIARIO = False`, con el acta de lo probado). Pide un asset del mismo estilo.

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
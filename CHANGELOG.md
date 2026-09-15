# CHANGELOG — FrutiCity 2.0

Cambios reales por fase. Detalle y decisiones en `docs/fruticity-2/audit.md` y `docs/fruticity-2/phase-1.md`.

## FrutiCity 4.1.0 · 2026-09-15 — El dino, ya bien

### Corregido
- **El dino se veía a parches, y era el mapa de normales.** `dino_normal.jpg` se importaba como
  `Default` mientras el material llevaba `_NORMALMAP`: URP lo leía esperando la codificación de
  un normal map y recibía RGB crudo. Marcado como `NormalMap`.
- **La RenderTexture del teatro se ampliaba 2,5×.** Estaba fija en 224×256, del tamaño que tenía
  el dino antes de crecer. Ahora se pide del alto al que se va a dibujar, calculado con la escala
  real del lienzo, y el suavizado baja a ×2 cuando la textura es grande.

### Nuevo
- **El dino salta** al encajar una cascada o una jugada de cinco o más. La sombra se queda en el
  suelo y encoge, que es lo que hace que el salto se lea como salto.
- **Rugido grabado** (Mixkit, *Sound Effects Free License*), recortado a 2,55 s con el pico en
  0,98 s para que caiga en el fotograma en que la animación abre la boca. En `DecompressOnLoad`:
  en *Streaming* llegaba tarde.

## FrutiCity 4.0.0 · 2026-09-15 — El jefe en el móvil

### Corregido
- **El dino no se veía en Android.** `Shader.Find` no basta: Unity no mete en la compilación un
  shader que no use ningún asset. El material pasa a ser un `.mat` en Resources
  (`Boss/DinoBoss_Skin.mat`), y el shader entra por dependencia. En Windows no ocurría.
- **El dino salía facetado en Android.** El perfil de calidad *Mobile* usa dos huesos por
  vértice y el de PC cuatro. Se fuerza `SkinnedMeshRenderer.quality = Bone4` en el renderer, y
  se quita la compresión de malla del FBX.
- **`ConfigureProject()` dejaba de pisar `bundleVersion`.** Escribía "0.1.0" en cada
  compilación, así que la versión del `ProjectSettings` no llegaba nunca al APK. Decisión que
  estaba pendiente en el handoff desde la sesión de los barrios de diez.

### Cambiado
- **El teatro del jefe aprovecha la pantalla.** `BoardTop` deja de ser constante: en el jefe el
  tablero y la botonera bajan y el escenario crece de 110 px a 300 (el bicho, de 104 a ~285). En
  un 16:9 no hay holgura y nada se mueve. Decorado repintado a 2048×600 y recortado con `uvRect`
  en vertical en vez de estirado.
- **El dino cruza en 30 s y no en 60**, con el empuje por jugada DOBLADO para compensar: la
  cuenta está en `MatchBoss.DinoCrossSeconds`. Y el ciclo de andar se calcula a partir de la
  velocidad real del suelo, así que no patina en ninguna pantalla.
- **Pausa** con icono dibujado arriba a la derecha, y con reiniciar (y su coste) y el botín del
  nivel dentro.
- **Mapa**: sin la fila de utilidades duplicada, sin el cartel de bienvenida y sin la línea de
  las estrellas; con marco de madera y bordes difuminados. El paso entre barrios pasa a ser
  variable (`AreaTop`) para que el espacio recuperado sea mapa y no un hueco vacío.
- **Ajustes** se muda de Ciudad a Perfil.

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
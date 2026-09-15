# Punto de continuación

> Actualización posterior del 6 de septiembre: rediseño visual implementado, compilación Windows correcta (0 errores, 3 avisos), 78/78 pruebas y navegación comprobada en Play. Unity MCP está conectado y registrado en Codex. Consultar [revisión UX/UI](UX_UI_REVIEW.md) y [Unity MCP](UNITY_MCP.md). El resto de este documento conserva el estado anterior y sus recetas; las indicaciones de «UI sin mirar» ya están superadas.

## FrutiCity 5.0.0 · 15 de septiembre: caras de sprite, y el destrozo que hice con git

### LO PRIMERO, PORQUE ES UNA LECCIÓN CARA: no hagas `git checkout` de un asset de Unity

Con el editor abierto, revertí `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset`
porque su diff parecía ruido del build. Unity recargó el asset y **perdió en memoria la lista de
`SerializeReference`** que guarda sus ajustes de runtime —entre ellos los shaders del Blitter—.
A partir de ahí, TODOS los APK salieron con URP incapaz de construirse: **16.452 errores por
fotograma** de `Blitter:Initialize` con shaders nulos, y **nada en 3D se dibujaba**. El dino
desapareció. La interfaz seguía viéndose porque el Canvas es Screen Space Overlay y no necesita
URP, y eso fue lo que despistó: parecía un problema del dino.

La reparación: restaurar el archivo **y forzar la reimportación del asset**
(`AssetDatabase.ImportAsset(..., ForceUpdate)`), que es lo que vuelve a construir el grafo de
referencias. Comprobado: `m_List` pasó de 0 a **38 entradas**, y en el móvil de 16.452 errores a
**cero**.

> **La regla, para la próxima:** un `.asset` de Unity que el editor tiene abierto se toca desde
> el editor, no desde git. Si de verdad hay que revertirlo, se cierra Unity primero.

### Caras de sprite: los FrutiFriends pasan a tener emociones

Lo pidió Fran: «ojos y boca sprites, súper expresivas, así muestran emociones», con «brazos de
palo negros con tres dedos de línea».

- **`tools/caras_fruti.py`** genera ocho caras (idle, alegre, guiño, sorpresa, susto, duda,
  enfado, triste), tres brazos, un pie y tres marcas de tebeo (gota de sudor, exclamación,
  interrogación). Todo en PIL, a ×4 y reducido, como `caras_fresita.py`.
- **El cuerpo sale de `Resources/Fruti3D/`**, que son las mismas frutas **sin cara**: las fichas
  del tablero, ya renderizadas en Blender con las luces buenas. Así el cuerpo sigue siendo 3D de
  verdad y no hay que borrarle la cara a nadie ni volver a modelar.
- **`UI/FrutiChibi.cs`** arma el muñeco por piezas y deja cambiar la expresión en caliente. En el
  nivel del jefe la fruta va de tranquila → dudosa → asustada → gritando según se acerca el
  bicho, con los brazos arriba y su gota de sudor.
- **La colocación de la cara es una tabla MEDIDA**, no ajustada a ojo: se midió la caja de alfa
  de cada cuerpo y su franja más ancha. La fresa es un cono —cara alta y pequeña— y el plátano
  una media luna —cara pequeña y corrida—; con la misma colocación para los seis, esos dos salían
  con la cara flotando fuera de la fruta. La tabla está DOS veces, en el generador y en
  `FrutiChibi`, y tienen que decir lo mismo.

### Y el dino, ya bien del todo

Gordote: mide un 10% más que su escenario y **asoma por encima del marco**, que es lo que pidió
Fran («se sale un pelín, así da aspecto de grandote total»). Va atado al ESCENARIO y no a la
holgura de pantalla —un fallo mío anterior: al crecer el teatro también hacia abajo, el bicho
seguía creciendo sólo con la mitad de arriba y se quedaba pequeño dentro de una caja grande—. Con
tope automático para que nunca llegue a la fila de monedas.

## FrutiCity 4.1.0 · 15 de septiembre, noche: por qué el dino se veía a parches

Tres intentos hasta dar con la causa, y merece la pena dejar los tres escritos porque los dos
primeros eran fallos de verdad —sólo que **no eran el que Fran estaba viendo**—.

1. **Los huesos de la piel.** El perfil *Mobile* usa dos por vértice y el de PC cuatro. Real, y
   arreglado (`SkinnedMeshRenderer.quality = Bone4`). No era la causa.
2. **La resolución de la RenderTexture.** Estaba clavada en 224×256, que era el tamaño justo
   cuando el dino medía 104 px de diseño; al crecer a 285 —y ×2,26 de escala de Canvas, o sea
   644 píxeles reales— se estaba ampliando dos veces y media. Real, y arreglado: ahora se pide
   del tamaño al que se va a ver. Tampoco era la causa; sí arregló el contorno, que salía blando.
3. **EL MAPA DE NORMALES.** `dino_normal.jpg` se importaba con `textureType = Default` mientras
   el material llevaba el keyword `_NORMALMAP` puesto. URP lo sampleaba esperando la codificación
   de un normal map y recibía RGB crudo: de ahí los parches planos, que parecían facetas de la
   malla y no lo eran. **Ésa era la causa.**

> **Cómo se encontró, y cómo encontrar el siguiente:** renderizando el dino aislado en el editor
> a 644 px —el tamaño real de pantalla— y mirando el PNG. Es el mismo bucle que usa Fran para el
> arte en Blender, y **cuesta segundos en vez de los diez minutos de un APK**. Los dos primeros
> intentos se pagaron a compilación cada uno; el tercero salió a la primera porque dejé de
> compilar y me puse a mirar.

### Lo que se añadió

- **El dino salta** cuando encaja un golpe gordo —cascada, o jugada de cinco o más—. El rig no
  trae clip de salto, así que el brinco se hace moviendo la caja: medio seno, sin rebote, porque
  se está llevando un golpe. **La sombra no salta con él**: se queda en el suelo y encoge, que es
  lo que convierte «el dibujo ha subido» en «el bicho ha despegado».
- **Rugido grabado** (`Resources/Audio/Sfx/sfx_roar.mp3`), de Mixkit bajo su *Sound Effects Free
  License* —uso comercial, sin atribución—, igual que los tres sonidos que ya había. Elegido
  midiendo los dieciocho de su página de rugidos: duración y energía por debajo de 300 Hz. Está
  recortado a 2,55 s **con el pico en 0,98 s**, que es el fotograma donde la animación abre la
  boca del todo (`BossStage.RoarPeak` = 1,0 s). Y va en `DecompressOnLoad`: en *Streaming* —como
  viene por defecto— el clip se abre al pedirlo y el rugido llega tarde a su propia boca.

### Pendiente, y es de Fran

- Los otros tres efectos (`sfx_coin`, `sfx_crystal`, `sfx_rayo`) siguen en **Streaming**, que en
  un sonido corto mete el mismo retardo. No se tocaron porque funcionan y nadie se ha quejado;
  igualarlos son tres líneas.
- El `sfx_roar.mp3` es el fichero de **vista previa** de Mixkit, no el de su botón de descarga
  —que pide interacción con la página—. Es el mismo sonido y la licencia lo cubre; si se quiere
  el oficial, se baja de la página y se sustituye el archivo, sin tocar código.

## FrutiCity 4.0.0 · 15 de septiembre, tarde: el jefe en el móvil, y lo que sólo se ve allí

El jefe pasó por el móvil de Fran y aparecieron **dos fallos que el PC no podía enseñar**, más
una tanda de ajustes de sitio. Todo esto va después de la sesión de abajo.

### El dino no se veía en el móvil, y eran DOS cosas encadenadas

**1. El shader se caía de la compilación.** El material se armaba en tiempo de ejecución con
`Shader.Find("Universal Render Pipeline/Lit")`, y **Unity no mete en la build un shader que no
use ningún asset**: el enlazador se lo llevaba, `Shader.Find` devolvía null y la malla se
quedaba sin nada con que pintarse. El resto del teatro —decorado, reloj, barra, fruta— salía
perfecto, que es lo que despistaba. El log del móvil lo cantaba de otros shaders: *«is not
supported or has been stripped from the build»*.

Arreglado con un `.mat` de verdad en `Resources/Boss/DinoBoss_Skin.mat`: así el shader entra por
dependencia y no hay nada que buscar. **En Windows no pasaba**, y por eso pasó las capturas.

**2. Salía facetado y azulado.** Otra cosa distinta, y también sólo del móvil: el perfil de
calidad **Mobile usa dos huesos por vértice** y el de PC cuatro (medido: `QualitySettings` por
perfil). Un bicho de 27 huesos con cuello y cola articulados los necesita justo en las curvas.
Se fuerza `SkinnedMeshRenderer.quality = Bone4` en el propio renderer, que manda sobre el ajuste
global y no cambia el presupuesto del resto del juego. De paso se quitó la compresión de malla,
que cuantiza normales y UVs.

> **La lección, para la próxima:** una compilación de Windows **no** valida el móvil. El
> enlazador de shaders y los perfiles de calidad son distintos, y las dos cosas se manifiestan
> como «no se ve» sin un solo error en consola.

### El teatro se queda con la pantalla

Un móvil de 20:9 deja unos **120 px libres por arriba y otros tantos por abajo** (`hudSlack`).
Ahora el jefe se los queda los dos: el tablero y la botonera **bajan** (`boardDrop`) y el
escenario crece hacia arriba y hacia abajo. Pasa de 110 px a **300**, y el bicho de 104 a ~285.

Para eso `BoardTop` dejó de ser constante. Es estático porque `TileHome` y `TileCentre` lo son, y
esos dos traducen casilla → pantalla: **todo** lo que se dibuja sobre el tablero sale de ahí, así
que el tablero se mueve de una pieza. En un nivel normal `boardDrop` es cero a propósito: arriba
no hay nada que quiera ese hueco y bajarlo sólo abriría un claro.

El decorado se repintó a 2048×600 (300 px de diseño) y **se recorta en vertical con `uvRect`, no
se estira**: la franja de abajo es el empedrado y lo que sobra es cielo.

### El dino, a 30 segundos

Lo pidió Fran. Y tiene una consecuencia que hubo que calcular: cruzando en 30 y durando 90, hay
que empujarle **dos travesías enteras**. Con el empuje viejo salían 62 jugadas en minuto y medio
—una cada 1,4 s, imposible—, así que **el empuje va doblado**: 31 jugadas, una cada 2,9 s. Ese
número está elegido mirando el otro: los 15.000 puntos piden unas 45 jugadas, una cada 2,0 s. O
sea que **quien va a ritmo de ganar por puntos frena al bicho de sobra**. El dino mete la prisa;
el marcador sigue decidiendo.

El **ciclo de andar se calcula**, no se elige: los pies siguen lo que el bicho se desplaza MÁS lo
que corre la calle por debajo, y esa cuenta se rehace en cada móvil porque el tamaño depende de
la pantalla.

### Sitio de las cosas

- **Pausa** con icono dibujado (dos barras, no el carácter tipográfico) arriba a la derecha. El
  cartel ahora lleva reiniciar con su coste en rayos, salir, y el escaparate de lo que guarda el
  nivel —reutilizando `LootBoard`, que ya apaga lo cobrado—.
- **Mapa:** fuera la fila Decorar/Historia/Regalo/Ajustes (las cuatro están en Ciudad), fuera el
  «¡BIENVENIDO A FRUTICITY!» y la línea de las estrellas. Y el espacio se recupera **de verdad**:
  la banda del primer barrio no se queda vacía, **se colapsa** (`AreaTop`, paso variable), así
  que el camino empieza pegado arriba. Con marco de madera y `RectMask2D.softness` de 24 px.
- **Ajustes** vive sólo en Perfil.

### La versión ya no se pisa

`ProjectBuilder.ConfigureProject()` escribía `bundleVersion = "0.1.0"` en **cada** compilación:
el `3.0.0` no llegó nunca a un APK y además el repositorio quedaba sucio tras cada build. Estaba
anotado aquí como decisión pendiente de Fran, y la tomó al pedir la 4.0.0. La versión la manda
ahora el `ProjectSettings`, que es un archivo versionado y con historia.

## Sesión del 15 de septiembre: el JEFE, y el 3D real por fin dentro del Canvas

**Rama:** `efectos-combos-royal`. El décimo nivel de cada barrio —10, 20, 30, 40 y 50— deja de
ser un nivel de plátanos y pasa a ser un **nivel de jefe**: un dinosaurio cruza un teatrillo
encima del tablero mientras juegas.

### Lo que se hizo

1. **El dino entra en el juego de verdad, en 3D.** El rig vivía en el proyecto de al lado
   (`3dFruityCreator`, 27 huesos, 4 animaciones) y ahora está en
   `Resources/Boss/DinoBoss.fbx`, animado en vivo dentro de la pantalla.
2. **`UI/BossStage.cs`** — el puente 3D → Canvas (ver abajo, es la decisión que importa).
3. **`UI/MatchBoss.cs`** — el teatrillo: decorado que corre, barra, reloj, el paseo del bicho,
   el daño, el rugido, las pisadas y el coletazo final.
4. **`UI/MatchScoreBar.cs`** — la barra de dos vueltas, sacada del bonus para que la compartan
   las dos pantallas que acaban por reloj.
5. **Decorado** (`tools/escenario_jefe.py`) y **música** (Badinerie a 1,25x, encadenada).
6. **`BossLevelTests.cs`**, que mide el mínimo en veinte tableros e imprime el reparto.

### LA DECISIÓN QUE IMPORTA: cómo se dibuja una malla animada en un Canvas

Estaba anotado como bloqueo del rumbo «3D real en Unity»: **una malla con esqueleto no se
dibuja en un Canvas en Screen Space Overlay**, y este juego entero es eso. Las salidas
apuntadas eran pasar el Canvas a Screen Space Camera —que reparte las piezas en capas y toca
`PieceMotion`, dueño único del transform de cada ficha— o renderizar aparte.

**Se renderiza aparte, y el bloqueo queda resuelto sin tocar el tablero.** El dino vive en su
capa (la 8, `BossStage`), a 3.000 unidades del origen, con su cámara ortográfica y sus dos
luces, y sale por una `RenderTexture` que la interfaz enseña en un `RawImage`. Ni una línea de
`PieceMotion`, ni una capa nueva en el tablero.

Y el detalle que va contra el instinto: **el dino no anda por el mundo 3D, anda por el Canvas.**
La cámara lo tiene siempre centrado; quien se mueve es el `RawImage`, en píxeles de diseño. El
paseo tiene que cuadrar al píxel con un marco de interfaz, y todo lo demás en este juego ya se
mueve así.

### Las trampas que se pagaron aquí

**El ×5 que pidió Fran no cabía, y se supo midiendo.** El mínimo iba a ser cinco veces el del
bonus (30.000). Medido con el motor sobre veinte tableros a 36 jugadas: el reparto va de
**10.140 a 34.320**. O sea que 30.000 sólo lo saca el tablero más afortunado jugando de bot, y
la barra verde (60.000) es **inalcanzable**: ni 45 jugadas perfectas pasan de 39.240. Y el jefe
cierra el barrio, justo delante de una puerta de cristal **sin margen** (diez niveles a una
estrella = diez cristales = lo que cuesta la puerta), así que un jefe impasable **encierra al
jugador**. Se quedó en **15.000, plano para los cinco**: la variación entre tableros (3×) es
mucho mayor que cualquier rampa por barrio, y poner 15.000→19.000 habría sido precisión falsa.

**La escala del FBX miente.** `SkinnedMeshRenderer.bounds` en pose de reposo daba 236 unidades
para un bicho de 1,9: el FBX trae escala 100 en los hijos y `fileScale` 0,01. Las `localBounds`
se fijan a mano en `BossStage`, o Unity culea el bicho fuera de pantalla al acercar la cámara.

**El encuadre está medido, no estimado.** Se renderizaron los cuatro clips fotograma a
fotograma midiendo la caja del alfa: el dino ocupa **1,631 × 1,975 unidades**, centrado en el
origen. De ahí salen `Frame` y la proporción de la textura. Y agrandar al bicho es tocar DOS
números a la vez —la caja del `RawImage` y `BossStage.Frame`—: subir sólo la caja agranda el
aire de alrededor.

**Rig Legacy, no Generic.** El README del dino recomienda Generic, y para un proyecto normal
tiene razón. Aquí no: Legacy es el único rig que se conduce entero desde código sin un
`AnimatorController` guardado como asset, y esta aplicación no tiene **ni un solo** asset de
escena.

**Una textura que se repite no puede ser «no potencia de dos» sin decírselo a Unity.** El
decorado mide 2112×220 y Unity lo importaba como 2048×256: estirado a lo alto y con el espejo
descuadrado, que es justo lo que hacía que la costura empalmara. `npotScale = None` y
`wrapMode = Repeat`, y los dos ajustes viven en `FruitTextureImport.cs` para que regenerar el
PNG no se los lleve por delante.

**Una pista que se encadena no puede llevar desvanecidos.** La Badinerie a 1,25x dura 74,9 s y
el nivel 90, y el `AudioSource` de la música no repetía: los últimos quince segundos —los de
«llega o no llega»— se jugaban en silencio. Se rinde sin `afade` y se pone `loop` sólo para
este tema.

**El mobiliario de calle dibujado en PIL no casa con el pueblo pintado.** Fran pidió una parada
de autobús. Se dibujó dos veces —vector con la paleta de la interfaz, y silueta oscura con filo
de luz— y las dos quedaban pegadas encima o directamente parecían un fallo de carga. Está
apagado tras `MOBILIARIO = False` en `tools/escenario_jefe.py`, con el acta de lo probado. Una
parada de verdad pide un asset del mismo estilo, no formas de PIL.

**De propina, un fallo que ya estaba:** `GoalDescription` no sabía de las pantallas por reloj y
caía en la última rama, así que el nivel de bonus llevaba desde que existe anunciándose como
«Limpia 0 casillas de mermelada».

### Cómo se juega

El dino cruza en **60 segundos** si nadie le toca, y el nivel dura **90**. Cada combinación le
hace daño y le **empuja hacia atrás** (6 px de base, más por celdas y por cascada, tope 30), así
que hay que pegarle unas dieciséis veces en minuto y medio para que no llegue. Hay **dos
maneras de perder**: que se acabe el reloj sin llegar a 15.000, o que el bicho alcance a la
fruta y se la meriende de un coletazo —sincronizado al fotograma 21 del clip, 0,875 s, que es
donde el rig dice que la cola alcanza su punta de velocidad—.

El empuje **no decae**, y es a propósito: con tableros que varían 3× por semilla, hacerlo decaer
castigaría la mala suerte en vez de la dejadez.

## Sesión del 13–14 de septiembre: barrios de diez, nivel de bonus y la fiesta de combos

**Rama:** `efectos-combos-royal` en los dos repositorios, **todo subido**. El del juego va por
`99a7e54` y el externo por `222c24c`. 192/192 pruebas EditMode en verde (salvo el último
commit, ver más abajo).

### Lo que se hizo

1. **El barrio pasó de cinco niveles a diez** (`FrutiCity 3.0.0`, commit `af4b2b2`). Hubo un
   paso intermedio —barrio = dos «capítulos» de cinco— que Fran descartó al verlo: quería los
   diez niveles en una sola zona. El capítulo ya no existe ni como concepto; toda la geometría
   vive en `Core/AreaMap.cs`.
2. **Nivel de bonus** en el quinto de cada barrio (5, 15, 25, 35, 45): contrarreloj, barra
   estilo Tekken —roja hasta el mínimo, verde hasta el doble—, cinco frutas en vez de seis y
   música propia. Vive en `UI/MatchBonus.cs`.
3. **Los especiales atrapados ya no mueren callados** (commit `8fdfa36`), que era un fallo real
   del motor. Ver abajo.
4. **El rótulo de combo**, rehecho letra a letra y siguiendo a la jugada (`99a7e54`).

### Las trampas que se pagaron aquí

**El arte del mapa manda sobre la geometría.** `JourneyStops` son coordenadas medidas a mano
sobre el camino pintado de cada ilustración. Cambiar cuántas paradas tiene un barrio **no es
una refactorización**: o hay ilustraciones nuevas, o hay que fundir las que existen. Se optó
por fundirlas (`tools/merge_journey_art.py`), y por eso las diez ilustraciones viejas siguen en
`Resources/Art/Journey/` aunque el juego ya no las cargue: el compositor las necesita.

**Las ilustraciones del viaje no tienen generador.** Salieron de un `image_gen` con los prompts
de `JOURNEY_IMAGE_PROMPTS.json`. Sin esa herramienta no se pueden rehacer, sólo recomponer.

**Los cuartos de la reforma tienen cuatro etapas modeladas a mano** en `art/blender/reforma.py`.
Por eso un barrio de seis tareas reforma DOS cuartos de tres, y no uno de seis: añadir etapas es
amueblar, no subir un bucle.

**`ProjectBuilder.ConfigureProject()` pisa la versión.** La línea 57 escribe
`PlayerSettings.bundleVersion = "0.1.0"` en cada compilación, así que el `3.0.0` del
`ProjectSettings.asset` no llega nunca al APK. **Decisión pendiente de Fran.**

**Medir antes de ajustar, también el balance.** La puntuación del bonus se estimó a ojo en ~250
por jugada y la medida real son **982**. Hay una prueba que lo mide y lo imprime
(`BonusLevelTests.TwentyFourMovesTellWhetherTheMinimumIsReachable`); si se tocan los mínimos, se
mira ese número y no la intuición.

**`FindHint()` devuelve `From == To` cuando hay un especial**, y eso significa «toca este
especial», no «intercambia». Pasárselo a `TrySwap` lo rechaza. Cazó a la primera versión de la
prueba de medición, que parecía un tablero atascado.

### Corrección importante sobre el móvil

Se dijo —y era **falso**— que el texto se vería borroso en el móvil por la escala ×2,26 y que
hacía falta mover la escala de `design.localScale` a `scaler.scaleFactor`. Mirando la captura
del Redmi a 1:1, **el texto más pequeño de la pantalla sale con los bordes limpios**. Unity
resuelve la escala bien. **Ese refactor no hace falta y tocaba todas las pantallas: no rehacer
el análisis.**

### Lo que quedó pendiente, y es de Fran

1. **El APK de las 15:02 sin instalar**: el móvil se desconectó de `adb` justo antes. Trae el
   rótulo que sigue a la jugada. `adb install -r FrutiCity/Builds/Android/FrutiCity-development.apk`.
2. **Los números del bonus.** Están a 6.000 de mínimo y 1:00 porque los pidió Fran, pero la
   medida dice que el mínimo cae a las 6 de las 24 jugadas del minuto y el doble a las 12. La
   propuesta con el dato delante es 10.000 y 20.000, subiendo 2.000 por barrio. **Hay que
   jugarlo antes de decidir.**
3. **La versión `0.1.0`** de `ProjectBuilder.cs:57`.
4. **Peso del APK**: pasó de 123 a 139 MB porque `Resources/Art/Journey` guarda las diez
   ilustraciones viejas Y las cinco fundidas, y todo lo que está en `Resources/` entra en la
   compilación aunque nadie lo use. Sacar las viejas de `Resources` recorta unos 25 MB, pero
   mueve arte entre repositorios.
5. **El último commit (`99a7e54`) se compiló pero no pasó la suite.** Es puro pintado y ninguna
   prueba toca `Banner`, pero conviene dejarlo verificado.

### Unity MCP

Registrado ya en el `.mcp.json` del proyecto (antes sólo estaba en la configuración personal de
Codex). Para usarlo hacen falta **las dos patas**: una sesión nueva del cliente —los servidores
MCP se cargan al arrancar— y el Editor abierto con `FrutiCity/`, que es quien levanta el puente.
Las validaciones batch NO lo arrancan y además trabajan sobre la copia de `.validation`.

Merece la pena: el rótulo de combos y el mapa fundido se hicieron **a ciegas**, y cada retoque
visual costó veinte minutos de compilación de Android para ver si había quedado bien.

## Sesión del 7 de septiembre: combos, efectos 3D, mapa y música

Se trabajó con el vídeo de referencia de Royal Match delante (`iSaTx0T9GFw`, descargado
por trozos con `yt-dlp -f 230 --download-sections` y hojeado como contactos de ffmpeg;
el formato HLS 230 es el que baja en segundos, los DASH tardan una eternidad). Lo que
se copió de ahí está anotado en el código donde toca.

**Verificado:** 84/84 pruebas EditMode, compilación Windows correcta, y las doce
capturas miradas una a una. La receta de captura ahora incluye mapa, ficha de nivel y
tres fotos de combos en marcha (`CaptureEffects`), porque un rayo dura dos décimas y
ninguna prueba automática lo ve.

### Motor

`ComboKind` (en `MatchTypes.cs`) nombra qué pareja de especiales se ha cruzado. El
motor ya resolvía todas las combinaciones; lo único que faltaba era **decir cuál**, que
es lo que permite montar una puesta en escena distinta por combo. `NameCombo` lo
deduce y `TrySwap` lo cuelga del paso `Activate`.

**Trampa pagada:** el paso `Activate` propio SOLO se añade cuando hay pareja de verdad
(`combo != Single`). Un especial suelto lo dispara la cadena en `ClearWave`, y
anunciarlo además desde `TrySwap` hacía que el cohete se disparase dos veces.

### Efectos

En `GameFeel`: `Bar` (la barra girada de la que salen todos los rayos), `Beam` (estela
con núcleo blanco), `Bolt` (rayo quebrado plano), `Ray3D` (rayo con cuerpo, el modelo
de Blender estirado), `Starburst`, `Flash`, `Halo`, `Charge`, `Plume` (humo de cohete),
`Flames`, `Boom`, `Fly3D` y `Debris3D`.

Lo que se aprendió mirando el vídeo, y que conviene no deshacer:

- **El cohete no se para en el borde.** Sale del tablero y la estela sigue fuera. Pararlo
  en el marco lo convierte en una raya pintada.
- **La estela es humo, no una línea.** `Plume` siembra bocanadas a lo largo del recorrido,
  con fuego naranja en las primeras. Las bocanadas se solapan de sobra a propósito: con
  poco solape se leen como un collar de bolas.
- **El cohete apunta a donde vuela.** `Fly3D` acepta rumbo fijo, y el modelo se horneó
  mirando arriba-derecha, así que hay que descontar `RocketNoseAngle` = 45°.
- **Los rayos largos y finos, no gordos y cortos.** Y con núcleo blanco opaco dentro del
  halo de color: solo con el halo se desvanecen contra el tablero.
- **La hélice deja raya lisa; el zigzag es del arcoíris.** Mezclarlos borra la diferencia.
- **El rótulo de combo va sobre placa oscura y con mejor ajuste.** Dorado sobre tablero
  claro no se lee, y los nombres largos se partían en dos líneas fuera de la placa.
- **Un combo puede lanzar doce cohetes.** `FireRocket` acepta menos bocanadas para las
  tandas: a dieciséis cada uno son casi trescientos objetos en un fotograma.

### Arte 3D nuevo (Blender)

Tres modelos de efecto, con el mismo estudio que las trece piezas: `modelo_humo.py`,
`modelo_rayo3d.py`, `modelo_llama.py`. Se exportan con
`blender --background --python art/blender/exportar.py -- EFECTOS` y se copian a
`Resources/Art/` como `fx_humo.png`, `fx_rayo.png`, `fx_llama.png`. Van por
`UiKit.Asset`, **no** por `FruitModels`: así no hay que tocar `Names` ni `Count`.

**Trampa pagada (la de siempre, mirar el PNG):** la cámara mira desde −Y. El rayo se
montó primero en el plano XZ y salió como un tubo visto de punta; va en XY con
`ENCARA=(84,0,-6)`, igual que la pieza de energía. La llama se giró 86° y salió como una
bola naranja; una revolución sobre Z ya se ve de perfil sin encarar nada. Ninguno de los
dos dio error en consola.

### Interfaz

- **Mapa de niveles:** una tarjeta por capítulo con su número, título, estrellas del
  capítulo y cinco botones. Candado dibujado en los bloqueados, estrellas debajo de los
  jugados y un «▲ AQUÍ» en el que toca. Debajo de cada botón va **una** de las dos cosas,
  nunca las dos: se pisaban justo en el nivel que más se mira.
- **Título en una línea.** «Un mundo de combinaciones» se partía y la segunda línea caía
  encima del subtítulo. Ahora es «Camino de combos».
- **Ficha de nivel con receta de combo**, copiada de las pantallas de carga de Royal
  Match: dos especiales, una flecha y el resultado con halo. Una por nivel, en el orden
  en que merece la pena aprenderlas.

### Música

Tres temas clásicos de dominio público, sintetizados en el propio juego (no se importa
ninguna grabación): Himno de la alegría, Pequeña serenata nocturna y Marcha turca.
Rotan al empezar cada nivel y se pueden cambiar desde la pausa. El volumen sigue en
`.07`, que es lo que había; si suena bajo, es ahí donde se sube.

### Lo que no se pudo hacer

**Los efectos de la Asset Store de Unity.** No hay forma de descargarlos desde aquí: la
tienda exige cuenta e ir por el Package Manager, y aunque sean gratis hay que
«comprarlos» con una sesión iniciada. Además la mayoría son sistemas de partículas en
espacio de mundo, y este juego se dibuja entero en un Canvas de UGUI: no caerían en el
tablero sin rehacerlos. Por eso los efectos van por Blender. Si Fran importa un paquete
a mano, conectarlo sí es trabajo de una sesión.

---

Estado a 6 de septiembre de 2026, tras la sesión de arte 3D + motor + UI. Este documento existe para que otra sesión pueda seguir sin releer todo el historial. Dice qué está hecho, qué está verificado, qué decisiones conviene **no** deshacer y qué falta.

## 1. Estado verificado

| Comprobación | Resultado |
| --- | --- |
| Tests EditMode dentro de Unity | **78/78 correctos** |
| Compilación Windows | **Correcta, 0 errores, 3 avisos** |
| Ejecutable | `FrutiCity/Builds/Windows/FrutiCity.exe` |
| Horneado de una pieza 3D | 45–52 ms (presupuesto 220 ms, medido por prueba) |
| Las 13 piezas modeladas en Blender | Exportadas y revisadas una a una en el PNG |
| Combos tipo Royal Match (4, 5, L/T, cuadrado) | En el motor, con las 78 pruebas pasando |
| **UI nueva vista en el juego** | **NO. Quedó compilando; nadie la ha mirado todavía** |

Los tres avisos son previos a este trabajo: `FindFirstObjectByType` está marcado como obsoleto.

## 2. Riesgo abierto: nada está en git

> **Resuelto el 7 de septiembre.** `Assets/FrutiCity/` **ya está confirmado** en el repositorio anidado `FrutiCity/` (remoto `Fry009/FrutiCity-2026-09-05_14-24-42`). El aviso de abajo queda como historia; comprobar con `git status` antes de creérselo.

`Assets/FrutiCity/` aparecía **sin seguimiento** en el repositorio anidado `FrutiCity/`. Todo el código del juego —motor, pantallas, arte 3D, efectos— estaba sin confirmar. Un borrado accidental lo perdía entero.

```powershell
cd FrutiCity ; git status --short   # muestra "?? Assets/FrutiCity/"
```

## 3. Recetas de trabajo

**Comprobar que compila sin arrancar Unity (unos segundos, en vez de 6 minutos).** Es la herramienta que más tiempo ahorra al iterar:

```powershell
$dotnet='C:\Program Files\Unity\Hub\Editor\6000.6.0f1\Editor\Data\DotNetSdk\dotnet.exe'
$csc='C:\Program Files\Unity\Hub\Editor\6000.6.0f1\Editor\Data\DotNetSdk\sdk\8.0.318\Roslyn\bincore\csc.dll'
$data='C:\Program Files\Unity\Hub\Editor\6000.6.0f1\Editor\Data'
$sa='FrutiCity\Library\ScriptAssemblies'
$rt=@('-nologo','-target:library','-langversion:9.0','-nostdlib+','-noconfig','-nowarn:0169,0414,0618,0649','-out:preflight.dll')
Get-ChildItem "$data\Managed\UnityEngine" -Filter 'UnityEngine*.dll' | ForEach-Object { $rt += ('-r:' + $_.FullName) }
$rt += ('-r:' + "$data\NetStandard\ref\2.1.0\netstandard.dll")
foreach($n in @('UnityEngine.UI.dll','Unity.InputSystem.dll')){ $rt += ('-r:' + (Join-Path $sa $n)) }
Get-ChildItem 'FrutiCity\Assets\FrutiCity\Scripts' -Recurse -Filter '*.cs' | ForEach-Object { $rt += $_.FullName }
& $dotnet exec $csc $rt
```

**Validar de verdad** (copia aislada, no toca el editor abierto):

```powershell
powershell -ExecutionPolicy Bypass -File tools/Validate-Unity.ps1 -Action Tests
powershell -ExecutionPolicy Bypass -File tools/Validate-Unity.ps1 -Action BuildWindows
```

**Ver el juego sin jugarlo.** El ejecutable sabe capturarse solo. Es la única forma de detectar fallos visuales, y ya destapó tres que ninguna prueba automática podía ver:

```powershell
FrutiCity\Builds\Windows\FrutiCity.exe -fruticityCapture C:\ruta\salida -fruticityQuitAfterCapture -screen-width 540 -screen-height 960 -screen-fullscreen 0
```

Genera cinco PNG: casa, taller, puzle, decoración e historia.

## 3 bis. El arte 3D se hace en Blender

Las trece piezas se **modelan por script en Blender** y se exportan a PNG. Todo vive en `art/blender/`:

| Archivo | Para qué |
| --- | --- |
| `comun.py` | El estudio: luces, cámara, materiales y utilidades de malla. **Lo comparten las trece.** |
| `modelo_<pieza>.py` | Una ficha por pieza, solo sus mandos y lo suyo |
| `galeria.py` | Las trece en dos filas con la misma luz, para juzgar si la familia casa |
| `exportar.py` | Graba `assets/`: PNG 512, PNG 128 y `.blend` por pieza |
| `conectar.py` | Abre Blender con el servidor MCP y un vigilante que rehace la escena al guardar |

```powershell
blender --background --python art/blender/exportar.py -- TODAS
blender --background --python art/blender/galeria.py -- frutas salida.png
```

En la consola de Python de Blender quedan `cargar("cohete")`, `galeria()` y `PIEZAS`. Hay un acceso directo en el escritorio, «FrutiCity - Blender con Claude».

**Cuatro trampas ya pagadas, las cuatro invisibles en consola:**

1. **`bound_box` no sirve para medir.** El de una curva viene inflado (una mecha de 0,57 daba 2,46) y el de una malla ignora los modificadores. `comun._extremos()` mide los vértices de la malla evaluada. Con `bound_box`, `encajar()` encogió la bomba a la cuarta parte sin dar ningún error.
2. **En `--background` los objetos de `bpy.ops` no caen en `scene.collection`.** Deducir la pieza por colección funciona con interfaz y falla sin ella: el racimo de uvas se exportó midiendo 0,43 porque solo contó la hoja. `comun` lleva un registro (`_nace`/`_vivos`); toda ficha que cree un objeto a mano debe llamar a `comun._nace(ob)`.
3. **El visor miente sobre la luz.** Usa EEVEE con un HDRI de estudio; el render es Cycles con `view_transform='Standard'`, que recorta en seco. Con las luces originales el kiwi salía verde fluorescente y la caja casi blanca, y en el visor se veían bien. Están a 275/330/80/190.
4. **`terminar()` va sin argumentos.** Pasarle solo el cuerpo dejaba fuera los accesorios, y la corona de la fresa se salía del tile sin que ninguna medida lo delatara.

**El control de calidad es mirar el PNG.** Los cuatro fallos de arriba se detectaron solo así.

## 4. Decisiones que conviene no deshacer

**`UiKit.Label` usa `VerticalWrapMode.Overflow`, no `Truncate`.** Con `Truncate`, Unity borra la línea entera cuando la caja se queda un píxel corta. Estaba comiéndose títulos de pantalla y diálogos completos sin dar ningún error. Si alguien lo devuelve a `Truncate`, el texto vuelve a desaparecer.

**El arte 3D se hornea una sola vista por pieza, no una rotación.** Se probó con tiras de 16 fotogramas de giro y se descartó: cambiar de sprite a 9 fps se ve a saltos y limita la resolución. Ahora se hornea una vista buena a 128 px con supermuestreo ×3 e iluminación por píxel, y **todo el movimiento va por transformaciones a 60 fps**. Es lo que hacen los match-3 pulidos, y es lo que pidió Fran: que parezca 3D siendo 2D.

**`PieceMotion` es el único dueño del transform de una pieza.** Compone en `LateUpdate` la vida en reposo, los golpes de escala y los desplazamientos que le escribe el animador del tablero. Si otro código escribe `localScale` o `anchoredPosition` de una pieza, pelean y da tirones.

**La sacudida de pantalla se suma dentro de `Fit()`.** `Fit()` recoloca la raíz cada fotograma para el área segura; si la sacudida escribiese la posición por su cuenta, una de las dos ganaría de forma aleatoria.

**El arte de las piezas sale de Blender, no del rasterizador.** `Fruit3D.Front(kind)` carga `Resources/Fruti3D/<nombre>.png` y **solo** si falta cae al horneado por código. Ese respaldo es a propósito: un PNG que falte no puede romper el juego. Los nombres de archivo son los de `FruitModels.Names`, así que no se pueden renombrar por un lado sin el otro.

**El kiwi va cortado, no entero.** Un óvalo marrón no se distingue de una patata a 128 px.

**El rayo lleva el color por cara, no dos prismas encajados.** Su contorno no está centrado en el origen, así que escalarlo para hacer un alma más pequeña deja el borde gordo por un lado y nulo por el otro. Mismo truco que el kiwi.

**`UiKit.Plate` tiene labio inferior (`lip`).** La base oscura asoma **solo por abajo**: es lo que convierte un rectángulo redondeado en una tecla que apetece pulsar. Con el borde de grosor uniforme vuelve a parecer una pegatina. Ver [ESTILO_UI](#) y la hoja de referencia que dio Fran.

**Las piezas del tablero viven en su propia capa (`pieceLayer`).** Así una pieza puede cruzar por encima de las casillas vecinas durante un intercambio o una cascada sin quedar tapada.

## 5. Qué hay construido

- `Scripts/Art3D/` — modelos 3D procedurales (`Mesh3D`, `Shapes3D`, `FruitModels`), rasterizador por software con búfer de profundidad y contorno (`Rasterizer3D`), y caché de horneado (`Fruit3D`). Sin dependencia del pipeline de render: los mismos píxeles salen en editor, en jugador y en modo headless.
- `Editor/Art3DExporter.cs` — menú **FrutiCity → Art** que exporta mallas `.asset`, prefabs y hojas PNG. El juego no depende de esos archivos; sirven para inspeccionar o sustituir el arte.
- `UI/UiKit.cs` — `Plate` (placa moldeada con sombra, borde, degradado y brillo), `Recessed`, `BoardFrame`, `Gradient`, y sprites horneados por código: `Rounded`, `Ring`, `SoftGlow`, `BoardFloor`, `Jam`, `Ice`.
- `UI/GameFeel.cs` — marcador flotante, banner de combo, ondas, sacudida, recompensas voladoras y sonido sintetizado. Todo con reservas de objetos y todo obediente a «Reducir animaciones».
- `UI/MatchScreens.cs` — animación interpolada: intercambio deslizado, rebote en jugada inválida, estallido con squash-and-stretch y cascada donde cada pieza cae la distancia exacta de los huecos que tiene debajo.
- `UI/MergeScreens.cs`, `UI/HomeScreens.cs` — las cuatro pantallas que faltaban y que impedían compilar el proyecto entero.
- `UI/Ambience.cs` — capa ambiental, añadida por otra sesión.
- Tests en `Tests/Editor/Art3D/` — geometría, rasterizado, determinismo y presupuesto de horneado.
- `Resources/Fruti3D/` — las trece piezas renderizadas en Blender (512 px, alfa), que es lo que se ve en el tablero.
- `Match3/MatchGame.cs` — combos completos al estilo Royal Match: 4 en línea → cohete, 5 en línea → arcoíris, L o T → bomba, **cuadrado 2×2 → hélice**. La hélice vuela a un elemento al azar prefiriendo lo que pide el nivel, y combinada con otro poder hace tres vuelos cargados con él. La generación de tablero evita cuadrados, o nacería con una jugada servida.
- `UI/PieceMotion.cs` — además de la vida en reposo, ahora tiene `Spin` (giro dirigido) y `Bounce` (peso al aterrizar).
- `UI/MatchScreens.cs` — intercambio que se pasa y vuelve, cascada escalonada por columnas, rebote en todas las piezas que caen (más fuerte cuanto más cayeron) y presentación giratoria de la pieza con poder.
- `UI/UiKit.cs` — `Plate(..., lip)`, `Stroke`, `Card`, `Chip`, `HudPill`, `Stars`, `Title` perfilado y `NavBar`.

## 6. Trabajo en paralelo

Hubo dos sesiones editando a la vez y chocaron dos veces:

1. Una compilación cogió código a medio guardar (`StarsForWin` llamado antes de existir).
2. Dos compilaciones escribieron en `Builds/Windows` a la vez y Windows bloqueó el archivo.

Si vuelve a haber dos sesiones, que **solo una compile**. La otra puede usar la comprobación rápida de la sección 3, que no toca la carpeta de salida.

## 7. Siguiente paso

**Lo primero, y está a medias:** el refactor de UI se quedó **compilando y sin mirar**. Hay que construir, capturar y juzgar:

```powershell
powershell -ExecutionPolicy Bypass -File tools/Validate-Unity.ps1 -Action BuildWindows
FrutiCity\Builds\Windows\FrutiCity.exe -fruticityCapture C:\ruta\salida -fruticityQuitAfterCapture -screen-width 540 -screen-height 960 -screen-fullscreen 0
uta\salida -fruticityQuitAfterCapture -screen-width 540 -screen-height 960 -screen-fullscreen 0
```

Riesgo concreto que hay que comprobar en la captura: el labio inferior de `Plate` **encoge la cara del botón**, y los rótulos se recolocaron para centrarse en la cara y no en la caja. Si algún botón pequeño quedó con el texto apretado o pisando el labio, se ve ahí.

Después, y sin empezar hasta ver la captura:

- Aplicar `Card`, `Chip` y `Stars` a las pantallas que aún usan `Plate` a pelo (fichas de personaje, tarjetas de encargo, modal de fin de nivel).
- La hélice usa el rayo dorado (pieza 8) como icono provisional. Merece su propia pieza modelada en Blender; eso implica una decimocuarta entrada en `FruitModels.Names` y tocar `Count`.
- Nadie ha jugado con las animaciones nuevas. El rebote y la cascada escalonada alargan la caída de 0,24 s a 0,36 s: hay que sentir si eso mejora el ritmo o lo entorpece.

La dirección acordada es parecerse a Royal Match con frutas. Lo que falta después, por orden de impacto:

1. **Temas de barrio desbloqueables.** Reducir de 50 niveles sueltos a unos 20 bien equilibrados, ligados a zonas que se van abriendo. Fran pidió expresamente menos niveles y más cuidado en la experiencia.
2. **Pulir los efectos jugando.** El marcador, el banner, la sacudida y las monedas voladoras están conectados pero **nadie ha juzgado todavía si se sienten bien**: si el banner tapa el tablero, si la sacudida molesta, si el ritmo es correcto. Eso no sale en una captura estática; hay que abrir el juego.
3. **Detalle pendiente:** en las tarjetas de encargo del taller, la línea de recompensa queda muy pegada al botón.

Nada de esto está validado en un teléfono real. La matriz de dispositivos sigue en [QA.md](QA.md) y los resultados en [VALIDATION_RESULTS.md](VALIDATION_RESULTS.md).

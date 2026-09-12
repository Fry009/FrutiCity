# FrutiCity 2 — cambios

## 2.5.0 — la puerta de cristal

`bundleVersion` 2.4.0 → **2.5.0**, `AndroidBundleVersionCode` 7 → 8. Etiqueta `v2.5.0` en los dos repositorios.

**Los cristales ya tienen dónde gastarse.** Se ganaban, se contaban y se veían en el mapa desde la 2.2.0, y no había puerta: una moneda que sólo sube es una puntuación, no una moneda. Entre barrio y barrio hay ahora una puerta que cuesta **seis cristales**, y esa puerta es lo que convierte «saca tres estrellas en el nivel 7» en una decisión en vez de un capricho.

Las cuentas ya estaban hechas y probadas desde la 2.2.0 (`CrystalRules`): seis por puerta, nueve puertas, y el nivel de bonus pagando dos como mínimo — que es lo único que impide que la primera puerta encierre a quien juegue justito. Aquí sólo se pinta y se cobra. **No hay resta en ningún sitio**: el saldo se calcula restando lo que cuestan las puertas abiertas, así que subir el contador de puertas *es* el cobro.

### Dónde va, y por qué ahí

La puerta va **arriba del barrio al que da paso**, no al final del anterior — aunque en el rollo del mapa sea el mismo sitio. Al terminar un capítulo, el mapa salta al siguiente y lo primero que se ve es la puerta cerrada. Puesta al final del capítulo que acabas de jugar, se queda fuera de la vista justo cuando toca mirarla.

La ficha del capítulo **no se ha tocado**: baja entera dentro de un contenedor y la banda de la puerta se le suma por arriba. Así las doce medidas del capítulo —ilustración, paradas, viñetas, botón— siguen contadas desde cero, que es justo donde se cuela un despiste.

### La puerta cierra de verdad

No es decoración del mapa: un nivel detrás de una puerta cerrada **no se puede completar** aunque se llegue a él por otro camino. El botón grande de abajo pasa a decir «ABRIR EL BARRIO 2» en vez de mandarte a un nivel con candado, la pantalla de victoria no encadena con el nivel de detrás de la puerta, y las paradas del barrio cerrado llevan candado. Si se pudiera entrar por cualquiera de esos tres sitios, la puerta no estaría cerrando nada.

Tocar un nivel con candado **no suelta un aviso**: abre el cartel de la puerta, que es donde el jugador puede hacer algo. Y el cartel dice de dónde salen los cristales que le faltan —de las estrellas—, porque un cartel que sólo dice «te faltan 2» deja al jugador sin saber qué hacer con la tarde. El mapa, con sus chapitas, ya le dice en qué niveles están.

### La partida vieja

Una guardada antes de las puertas llega con medio mapa hecho y `gatesOpened` a cero: sin rescate, al actualizar se encontraría **el barrio en el que estaba jugando cerrado con llave**. Se abren las puertas de los barrios donde ya hay niveles superados, y **no se regalan cristales**: el saldo se recalcula solo y queda exactamente igual que el de quien hubiera jugado con las puertas puestas desde el principio.

El rescate mira los niveles **superados**, no `nextLevel`, y por eso puede ejecutarse en cada arranque sin marca en el guardado ni riesgo de ir sumando puertas. Con `nextLevel` habría regalado la primera puerta a todo el que terminase el primer barrio — que es exactamente lo que rompería el sistema entero. Hay prueba de las dos cosas.

### Trampas pagadas, mirando las capturas

- El marco, a 316 px de ancho, se leía como **una valla o un cartel**. Una puerta que no parece una puerta no se toca: ahora es más alta que ancha.
- La puerta abierta era **un marco de nada**. Lo que la hace una puerta es que por ella se vea el camino seguir: cielo arriba, camino abajo y dos tramos que se estrechan al fondo, que es toda la perspectiva que hace falta a ese tamaño.
- El candado, centrado y a 34 px, **se comía el número** y las cinco paradas se volvían cinco piedras grises iguales. Va en una esquina y más pequeño.
- El «¡AQUÍ!» sobre una parada con candado decía dos cosas a la vez —«es tu turno» y «está cerrado»— y la primera es mentira: mientras la puerta siga cerrada, el turno es de la puerta.

**174/174 EditMode** y build de Windows correcto. Capturas en `artifacts/puerta2/`: cerrada, su cartel y abierta.

## 2.4.0 — el reloj de los rayos

`bundleVersion` 2.3.0 → **2.4.0**, `AndroidBundleVersionCode` 6 → 7. Etiqueta `v2.4.0` en los dos repositorios.

**La energía era el único recurso que se regeneraba a escondidas.** El jugador veía «12/50» y no tenía forma de saber si el siguiente rayo llegaba en diez segundos o en cinco minutos. El único sitio que lo decía era el cartel de «te faltan rayos» — o sea, justo cuando ya era tarde. Un contador de espera que sólo aparece al bloquearte se lee como un castigo; puesto donde se ve siempre, se lee como una promesa.

Debajo de la píldora de rayos hay ahora un reloj con la cuenta atrás y una **barra de carga**, que dice lo mismo que el número sin tener que leerlo: de un vistazo se sabe si merece la pena esperar o irse a decorar. Con la barra llena pone **LLENO** en verde y no cuenta nada, porque no hay nada que contar.

### Los cinco minutos

Lo pidió Fran al pedir el reloj. **Eran tres**, y ese es justo el motivo de que el número no importase hasta ahora: no se veía en ningún sitio.

Lo que cambia: la barra entera pasa de **2 h 30 a 4 h 10**. Con 50 de tope y 5 por partida son diez partidas por barra, o sea unos **25 minutos por partida** — el ritmo de la referencia, donde una vida tarda media hora. Si alguna vez se quiere volver atrás, `EnergyIntervalSeconds` es el **único** número que hay que tocar.

Y ahí estaba escondido un defecto: el cartel de «te faltan rayos» decía «Vuelve un rayo cada 3 minutos» **escrito a mano**. Habría empezado a mentir en cuanto se tocase el intervalo, que es la clase de mentira que el jugador comprueba con un reloj de verdad. Ahora los minutos salen de la constante.

### Detalles

- **Los rayos no sueltan el «+1» cayendo**, como hacen las otras tres píldoras: ese hueco lo ocupa el reloj. El premio se escribe **encima del reloj** y el reloj da un bote — y es mejor así, porque el reloj es justo donde el jugador tenía puesto el ojo.
- Cinco pruebas nuevas sujetan la promesa: que el rayo entra **exactamente** cuando el reloj marca cero y no un segundo antes, que gastar desde el tope arranca la cuenta entera, que el tiempo fuera de la aplicación paga entero y **conserva la fracción** sobrante para el siguiente, y que una barra llena **no acumula tiempo a cuenta** (si lo hiciera, gastar un rayo soltaría otro al instante).
- La captura de revisión trae `26-reloj-rayos.png`. Hay que gastar energía a mano para sacarla: en modo captura las partidas no cobran, así que la barra está siempre llena y el reloj pondría LLENO.

**165/165 EditMode** y build de Windows correcto.

## 2.3.0 — el botín por nivel, y cobrar que se nota

`bundleVersion` 2.2.1 → **2.3.0**, `AndroidBundleVersionCode` 5 → 6. Etiqueta `v2.3.0` en los dos repositorios.

**Cada nivel es una veta, y paga cada cosa una sola vez.** Antes las tres recompensas se contaban en tres sitios distintos —las monedas en `ProgressionService`, los cristales en `CrystalRules`, las estrellas en ninguno— y el jugador no tenía forma de saber qué le quedaba por sacar de un nivel. Rejugar era una lotería: a veces pagaba y a veces no, y nunca se sabía por qué.

`Core/LevelLoot.cs` dice la regla **una vez** y la dice para las tres monedas: lo que hay dentro, lo que ya salió, y lo que queda. Ninguna de las tres cuentas se guarda: las tres se deducen de la mejor marca del nivel y de si está completado, que es lo mismo que ya hacían los cristales y la razón de que no se puedan desincronizar ni regalar dos veces.

### Lo que cambia al jugar

- **Las estrellas se extraen, no se regalan.** La primera victoria pagaba UNA estrella y las demás ninguna, jugases como jugases: bordar un nivel no valía nada y el jugador no podía saberlo. Ahora un nivel guarda tres y paga **las que falten** respecto a su mejor marca. Volver y hacerlo mejor suelta exactamente lo que quedaba; volver y hacerlo igual no suelta nada.
- **El suelo no baja**: la primera victoria sigue pagando como mínimo una estrella. Ninguna partida en curso se queda sin poder pagar sus reformas.
- **Los cristales se apuntan solos.** No se conceden en ningún sitio nuevo: salen de la marca que acaba de subir, recontados por `CrystalRules`. El cristal que faltaba aparece con la estrella que faltaba.

### Lo que se ve

- **La ficha de antes de entrar** (`LootBoard`) enseña las tres monedas del nivel, una a una, con **lo ya cobrado translúcido** y lo que sigue dentro a todo color, con halo y respirando. Y una línea que lo dice con palabras: «Aquí te quedan 1 estrella y 1 cristal». El cartel crece de 582 a 712 px.
- **La chapita del mapa** (`LootPill`) sustituye a la fila de tres estrellas sueltas bajo cada parada: ★2/3 y 💎1/2 en 88 px, sobre placa oscura. Dorado = aquí queda algo; verde = aquí no te queda nada. Es lo que permite elegir nivel desde lejos sin abrir ninguna ficha. Las estrellas sueltas contaban media historia —los cristales no salían por ningún lado— y encima iban sin fondo sobre la ilustración, así que sobre un tejado claro se perdían.
- **La victoria dice lo que ha soltado la veta**, no lo que se ha jugado: «+1 estrella · +1 cristal», o «Este nivel ya estaba vacío» si se repitió uno exprimido. Y los cristales **vuelan al HUD** por primera vez (`GameFeel.FlyTo` acepta ahora un sprite suelto; el cristal es un PNG y no pasa por `FruitModels`).

### Cobrar se ve y se oye, en las cuatro píldoras

Lo pidió Fran: que los cristales y los rayos se sumen con animación y sonido, «como las monedas». Al mirarlo, resultó que **las monedas tampoco lo tenían**: lo que tenían era que la pantalla de victoria y el regalo diario les mandaban monedas *volando*. El contador en sí sólo daba un respingo del icono.

`GainFx` va enganchado al **contador**, igual que el `SpendFx` que ya existía para lo que se paga, y esa es toda la gracia: da igual quién pague —un nivel, una compra, el regalo del día o el temporizador de los rayos—, si el número sube, la píldora **salta entera**, suelta **chispas de su color**, **canta su nota** y escribe **cuánto ha entrado**. No hay que acordarse de llamarlo desde cada sitio que premia.

- **La píldora salta entera** porque ahora cada una vive en su propio contenedor con el pivote centrado. Antes eran cinco piezas sueltas sobre la barra y sólo se podía mover el icono, que es lo que la hacía parecer muerta cuando el número cambiaba. El reparto no se movió ni un píxel: comprobado comparando las capturas antes y después.
- **Cada recurso tiene su voz.** El cristal sonaba con el tono de la bola de luz y la estrella con el de una fusión: prestados los dos, así que cobrar un cristal se oía igual que reventar un especial del tablero. La estrella es ahora una campana clara de tres notas ascendentes y el cristal es **vidrio**: un armónico que no es múltiplo entero de la fundamental (2,76) y una cola larga. Con un armónico al doble, como el resto, sonaba a moneda cara.
- **Las estrellas también salen volando al gastarse** hacia la mejora que las cobra. Eran las únicas de las cuatro que se iban del contador en silencio y sin moverse.
- El **«+3»** que se descuelga de la píldora cae **catorce** píxeles y no veintidós: el hueco es el que hay entre los 68 px donde acaba la píldora y los 96 donde empieza la fila de botones del barrio. Con veintidós se plantaba encima de «Decorar» y «Historia» y parecía una etiqueta de los botones. Medido en la captura.
- La captura de revisión trae `25-cobro.png`, con los cuatro cobros disparados a la vez y fotografiados a media vida — el caso peor, que es el único que merece la pena mirar.

### Trampas pagadas, mirando las capturas

- La línea de premio de la victoria **no cabe en una**: «12.480 puntos · +3 estrellas · +2 cristales» se pasa de los 442 px y el último premio se cae a un renglón suelto medio fuera del cartel. Van dos líneas.
- Por lo mismo, la frase de la vitrina **no nombra las monedas** aunque estén sin cobrar: con ellas se va a 58 letras y se parte. La columna de monedas ya las enseña con su cifra.
- El **cristal se pide más grande que la estrella** (42 px contra 32). El PNG es una gema alta y estrecha y `UiKit.Art` conserva la proporción: a 32 ocupaba catorce de ancho y al lado de una estrella cuadrada parecía un premio de segunda.
- La placa va **más oscura que el `Deep` de la casa**: con el tono normal, el degradado de `UiKit.Plate` aclara justo la mitad donde caen los iconos y el oro se quedaba a medio camino del fondo.
- El cartel de nivel **tenía que crecer y bajar el botón**: con el alto viejo, la frutita del pie —que se pega a 820— se quedaba montada encima del botón de jugar.

### Lo que hay que vigilar

**El ritmo de la reforma se acelera.** Las 30 tareas de la historia cuestan 45 estrellas y estaban calibradas con un reparto de 1 por nivel (50 en toda la temporada). Con hasta 3 por nivel, quien juegue bien puede tener las reformas pagadas por el nivel 15. Si eso va demasiado rápido, el número que hay que tocar son los `cost` de `EPISODES.json`, **no** el reparto de estrellas: el reparto es lo que hace que rejugar signifique algo.

Y sigue faltando lo de siempre para que los cristales sean jugables: **la puerta de capítulo en el mapa**. Ahora se ven, se cuentan y se sabe dónde quedan — pero todavía no hay dónde gastarlos.

**160/160 EditMode** y build de Windows correcto. Capturas en `artifacts/botin2/` (el botín) y `artifacts/cobro2/` (el cobro).

## 2.2.1 — los signos de más, dibujados

`bundleVersion` 2.2.0 → **2.2.1**, `AndroidBundleVersionCode` 4 → 5. Etiqueta `v2.2.1`.

El `+` era **un carácter de la fuente**, y un más tipográfico está pensado para leerse *dentro de una frase*: es fino, se apoya en la línea base y no está centrado en su caja. En un círculo de 28 px salía borroso y descolgado.

`UiKit.PlusButton` lo **dibuja**: dos barras redondeadas, centradas de verdad, con sombra propia y brillo arriba. Nítido a cualquier tamaño porque no depende del renderizado de texto.

**Y el arreglo destapó otro**: al quitar el ajuste de línea, «50/50» dejó de partirse pero empezó a meterse **por debajo** del `+`. Baja a cuerpo 17, y sólo ese contador: los rayos son el único con dos números, y encoger los cuatro para que quepa el más largo dejaría los otros tres pequeños sin motivo.

Es la tercera vez que la misma esquina da guerra. **Cada vez que se toque el ancho de la fila hay que volver a mirar el contador de rayos**, que es el que más caracteres lleva.

151/151 EditMode y build de Windows correcto.

## 2.2.0 — cristales, cuatro monedas y la historia enganchada

`bundleVersion` 2.1.0 → **2.2.0**, `AndroidBundleVersionCode` 3 → 4. Etiqueta `v2.2.0` en los dos repositorios. Sigue siendo **estable y autónoma, sin Firebase**.

- **Cristales morados**: reglas, arte 3D y contador. El saldo **se calcula en vez de guardarse**, así que la granja y el bloqueo son imposibles por construcción. Puertas de 6 con el bonus pagando 2 como mínimo — sin eso, la primera puerta encerraría al jugador de salida.
- **El HUD pasa a cuatro píldoras.** No fue añadir una: las tres viejas ocupaban de 18 a 522 de los 540 y hubo que rehacer la fila entera.
- **El gancho entre episodios**, que llevaba escrito en el contenido desde siempre y **no se leía en ningún sitio**. Era la causa de que cada capítulo pareciera empezar de la nada.
- **Compras idempotentes** por transacción, con memoria en el guardado: antes cada reintento de la tienda regalaba el pack otra vez.
- **Precios en euros escritos a mano, fuera.**
- **Cuentas**: arquitectura lista, en modo invitado, esperando credenciales.

**151/151 EditMode** y build de Windows correcto.

Falta para que los cristales sean jugables: **la puerta de capítulo en el mapa** y **el modo bonus** de dos minutos.

## 2.1.0 — estable, autónoma, **sin Firebase**

`bundleVersion` 2.0.0 → **2.1.0**, `AndroidBundleVersionCode` 2 → 3. Etiqueta `v2.1.0` en los dos repositorios (juego `00c7814`).

**Se puede instalar y jugar entera sin red y sin cuenta.** La partida se guarda en el propio dispositivo: no hay analítica, ni anuncios, ni cobros, ni copia en la nube, ni inicio de sesión. Lo que está enchufado es `OfflineIntegrations`, y sus cuatro servicios dicen que no a todo **a propósito**; la nota está escrita en el propio fichero, no sólo aquí, que es lo único que la pone delante de quien vaya a tocarlo.

La regla que no hay que romper: **nunca dar por bueno un anuncio, una compra, una subida o un premio que no ha ocurrido.** Devolver `true` en esos métodos para «probar» el flujo regalaría monedas de verdad en el guardado de verdad.

Sobre 2.0.0 entra el repaso de interfaz de más abajo. **115/115 EditMode** y build de Windows correcto.

## 2026-09-10 (noche) — repaso de interfaz pedido por Fran

- **La barra de recursos vuelve a estar siempre visible**, también jugando. Monedas y rayos estrenan un **`+`** que lleva a la tienda (y avisa antes de abandonar una partida en curso). Las estrellas no lo llevan: se ganan jugando, y un `+` ahí prometería un atajo que no existe.
- **Los botones de ayuda pierden el círculo.** La cara del botón mide 112×52 y el hueco de 56 empezaba en y=2: se salía seis píxeles y asomaba un gajo por debajo de la madera. El `+` se salía otros cuatro.
- **Fuera la barra de progreso** del tablero: decía lo mismo que la pastilla del objetivo con menos precisión y, vacía, se leía como una raya suelta. Ojo, `progressFill` **no** estaba protegido contra nulo en `UpdateMatchHud`: dejar de crearla sin quitar también su escritura habría reventado el HUD en el primer movimiento.
- **Fuera el fondo azul de la barra de navegación**, que tapaba el pueblo justo por donde el camino llega abajo.
- **La ciudad ocupa el alto real del móvil.** El botón de jugar estaba clavado en el diseño de 960 mientras `Fit()` empujaba las pestañas al borde: en un móvil alargado quedaba una franja muerta y el botón a media altura. Ahora el camino se estira con `hudSlack` y el botón va en un zócalo pegado abajo.
- **La receta de combo tiene dos líneas.** «Las hélices salen cargadas con la bomba» se partía y la segunda línea caía **fuera** de la tarjeta crema, porque `UiKit.Label` desborda en vertical a propósito.
- **Pestaña Perfil**, con datos reales, **volver a empezar de cero** (conserva las ayudas, y las enseña) y **borrar la partida** (borra todo, y lo dice). El verde es siempre el botón de arrepentirse.
- **Las estrellas del cartel de victoria ya no pisan el texto.** No era falta de sitio: `StarReveal` recentraba el pivote **sumando** medio alto en Y cuando `UiKit` ancla arriba-izquierda con la Y hacia abajo, así que cada estrella saltaba **56 px hacia arriba** al aparecer. Por el mismo motivo su estallido estaba clavado en una coordenada de una versión anterior, y en el mapa reventaba en mitad de la nada.
- **Gastar monedas y rayos se ve.** Va enganchado al contador y no a cada sitio que cobra, así que cualquier gasto que se añada después sale animado solo; vuela hacia el último botón pulsado, con piezas más pequeñas y rápidas que las de premio.

Sin login todavía: Google y usuario/contraseña necesitan Firebase Authentication y un proyecto con credenciales. La pantalla de Perfil queda preparada como su sitio.

## 2.0.0 — 10 de septiembre de 2026

Primera versión etiquetada. Recoge las fases 1 a 4 del plan.

`bundleVersion` 0.1.0 → **2.0.0**, `AndroidBundleVersionCode` 1 → 2. Etiqueta `v2.0.0` en los dos repositorios (juego `e099f20`).

**Verificado en esta versión:** 115/115 pruebas EditMode · build de Windows correcto · APK de Android **IL2CPP/ARM64 de 116 MB instalado y arrancado en un dispositivo real** (Redmi, Android 15, sin `FATAL` en logcat) · veinte capturas del ejecutable miradas una a una.

**Lo que esta versión NO trae**, para que el número no prometa de más: eventos, temporadas, álbum, compras dentro de la aplicación y Firebase. La tienda sigue siendo offline y no hay ningún cobro activado. El scroll de la ciudad recuerda dónde estabas al volver de un nivel, pero todavía no entre sesiones.

Un aviso que conviene no perder: **el atajo de Mono/ARMv7 del `ProjectBuilder` ya no sirve** para el móvil de Fran. Es un dispositivo de 64 bits puros (`abilist: arm64-v8a`, sin `armeabi-v7a`) y ese APK no se puede instalar ahí. Hay que ir por IL2CPP/ARM64 aunque tarde mucho más.

Y una corrección al registro: el build de Android **nunca falló por IL2CPP**. El log decía `java.io.IOException: Espacio en disco insuficiente`. Los «988 MiB» que la auditoría anotaba como problema de tamaño del APK eran un intermedio de un build fallido, no un APK: el real pesa 116 MB.

## 2026-09-10 (tarde, II) — fase 4 y minitutorial de mecánicas

- **Casa es la ciudad.** El camino de niveles deja de vivir en una ventanita de 530 px dentro de otra pestaña y pasa a ser la pantalla, con las utilidades fijas arriba y un solo botón grande abajo.
- La barra baja a **tres destinos**: Ciudad, Vecinos, Tienda. «Mapa» desaparece porque Casa ya es el mapa.
- **Minitutorial de comportamientos del tablero**, pedido por Fran: la primera vez que sale la mermelada, el hielo, la caja, la raíz o el chocolate, el juego se para y lo explica, con la muestra dibujada igual que en el tablero y un foco sobre las casillas afectadas al cerrar.
- Los textos del tutorial salen de leer `MatchGame.ResolveClears`, no de la intuición. **El hielo NO se rompe combinando al lado**: eso lo hacen caja, raíz y chocolate.
- `GameState.seenMechanics` guarda qué se ha explicado ya, sin subir `SaveVersion`.

Detalle en [phase-4.md](phase-4.md). Capturas en `screenshots/fase-4/`.

## 2026-09-10 (tarde) — fases 2 y 3

- **Revalidada la fase 1, que no se había visto.** Sus catorce capturas estaban en negro (`Camera.Render()` no funciona en URP y no da error); los tests eran 114/115 por caché de importación, no 115/115; y el build de Windows moría por disco lleno, no por código. Detalle en la corrección de [phase-1.md](phase-1.md).
- Canon resuelto por el usuario: **FrutiFriends**, la fruta chibi. `FrutiCast` se conserva íntegro.
- Portada convertida en cartel y no en clon del Home: Fresi delante, Pablo y Nora detrás, rótulo al 70 % del ancho, un solo CTA.
- La partida se queda la pantalla entera: fuera recursos y pestañas, tablero 37 px arriba, ayudas apoyadas en el borde. El HUD vuelve justo antes de cobrar el premio.
- El Home dice para qué sirven las estrellas, con el nombre real de la tarea, y `Decorar ★n` lleva el precio.
- La tarjeta de reforma estrena miniatura «ASÍ QUEDARÁ» y usa los treinta nombres de tarea de `EPISODES.json`, que estaban escritos y sin usar.
- **`bg_village.png` se dibuja por primera vez.** Llevaba en Resources sin usarse porque las dos llamadas a `SceneBackdrop` pasaban `dim=true` y caían al degradado plano. Ahora es el fondo de Historia, Vecinos y Reforma. El tablero conserva el degradado calmado a propósito.
- Navegación de cinco pestañas a cuatro; Reformar deja de ser pestaña.
- Cinta del martillo arreglada: salía partida en dos líneas.
- `Validate-Unity.ps1` poda y reutiliza snapshots: la validación baja de ~25 minutos a unos pocos.

Detalle completo en [phase-2-3.md](phase-2-3.md). Capturas en `screenshots/fase-2-3/`.

## 2026-09-10 — fases 0–1, arte del 8 conservado

- Auditoría actualizada antes de cambiar código; referencias históricas archivadas.
- Regla de oro recogida en AGENTS.md y art-direction.md: mejorar el arte existente sin cambiar canon.
- Recuperados Home y mapas ilustrados, paleta del 8 y frutas FrutiFriends. Portada con el mismo arte y CTA único. Fuentes y reparto articulado conservados.
- Fondo de portada/Home y oscurecimiento de modal adaptados al viewport; controles en área segura.
- Corregidos labio de botón, desactivados, dimensiones internas de tarjetas y creación de CanvasGroup de los modales. Celebraciones de vecinos funcionales con ambos sistemas de animación.
- Nueva assembly de pruebas UI; 115/115 EditMode aprobadas mediante Unity MCP. Captura ampliada a Ajustes y Regalo.
- Confirmadas conexiones de Unity y Blender MCP. Herramienta local de inspección de Blender de solo lectura.
- Sin cambios en motor, saves, economía, niveles, PNG, FBX ni música. Sin nuevos paquetes, cobros o backend.

Resultados de builds, capturas, archivos y límites en [phase-1.md](phase-1.md). Próximas fases y plan por archivos en [audit.md](audit.md).

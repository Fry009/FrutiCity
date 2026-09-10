# FrutiCity 2 — cambios

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

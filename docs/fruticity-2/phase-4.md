# Fase 4 — la ciudad es el menú, y el tablero se explica solo

10 de septiembre de 2026. Continúa [phase-2-3.md](phase-2-3.md). Sigue sin sustituirse ni regenerarse un solo asset.

## La ciudad es el menú (§9–11, §16)

Había **dos sitios para la misma pregunta**. Una portada estática con el logo, el lema y cuatro frutas posando, y en otra pestaña el camino de niveles metido en una ventanita de 530 px con un título encima. El jugador tenía que saber que el sitio donde de verdad pasan las cosas se llamaba «Mapa».

El camino ya era casi todo lo que pedía el plan: un scroll vertical de diez segmentos ilustrados, unos 9700 px —diez pantallas—, con las paradas colocadas a mano sobre el camino pintado de cada ilustración, y con memoria de dónde estabas al volver de un nivel. Lo que le faltaba era **ser la pantalla**.

- `Casa` renderiza la ciudad. La portada conserva el cartel, que es donde un cartel sirve de algo.
- El scroll pasa de 530 a 576 px de alto y se queda con el centro de la pantalla.
- Fila fija de utilidades arriba: `Decorar ★n`, `Historia`, `Regalo`, `Ajustes`. Ninguna es un destino: son cosas que se hacen y se cierran.
- Una sola línea de texto suelta, la que dice para qué sirven las estrellas: **«★1 más para: El plan de Mona»**.
- Un solo botón grande abajo, y dice a dónde lleva: **JUGAR NIVEL n**. Va fijo por encima del scroll, así que se puede pasear por el barrio sin perder de vista dónde se sigue.
- El pueblo ilustrado asoma por los márgenes del camino: los bordes tampoco son un color plano.

**La barra baja a tres destinos**: Ciudad, Vecinos, Tienda. «Mapa» desaparece porque Casa ya es el mapa. Historia, reforma y nivel iluminan Ciudad, que es de donde se entra a las tres y a donde se vuelve.

### Lo que esta fase NO hace

La memoria del scroll sigue viviendo en la sesión, no en el guardado. Volver de un nivel te deja donde estabas, que es el caso que importa; cerrar y reabrir el juego te lleva al capítulo del nivel actual. Persistirlo toca `GameState` y no se ha querido mezclar con la migración de esta sesión.

Tampoco hay vida ambiental sobre el camino (§45): los personajes que se ven son los que están pintados en cada ilustración.

## Minitutorial de comportamientos del tablero (§53–54)

Pedido por Fran en esta sesión. La primera vez que el tablero se comporta de una manera nueva, se para y se explica. Antes el jugador se encontraba la mermelada, el hielo o el chocolate sin que nadie le dijera nada, perdía dos o tres intentos averiguando por qué una fruta no se movía, y eso se lee como que el juego está roto, no como un reto.

- Se dispara la **primera vez** que un nivel va a poner un obstáculo que no se ha visto. El contenido ya lo tenía escalonado solo: **caja en el 3, mermelada en el 4, hielo en el 21, raíz en el 31 y chocolate en el 41**.
- La tarjeta sale **sobre el tablero ya montado**, no antes: así el obstáculo de verdad está detrás del texto.
- La muestra se dibuja con **las mismas piezas y colores que el tablero**, no con un icono aparte. Un dibujo que no se parece a lo que hay en pantalla obliga a traducir en vez de a mirar.
- Al cerrarla, **el foco**: las casillas que llevan ese obstáculo dan un respingo y sueltan un anillo, en tandas de tres para que se lea como un recorrido y no como un fogonazo.
- Se marca como vista **al cerrar**, no al abrir: si el jugador sale del juego con la tarjeta puesta, la vuelve a ver en vez de perdérsela para siempre.

### La detección repite el criterio del motor

`ObstaclesOfLevel` no se limita a leer `obstacles` del contenido: el objetivo mete el suyo, igual que hace `MatchGame.PlaceObstacles`. Sin esa segunda parte el nivel 3 saldría con cajas sin haberlas presentado, porque su lista de obstáculos está vacía y la caja la pone el objetivo `break_boxes`.

### Los textos salen del motor, no de la intuición

Verificado en `MatchGame.ResolveClears` antes de escribirlos:

| Obstáculo | Qué hace de verdad |
| --- | --- |
| Caja | No se mueve ni combina. Se rompe combinando **al lado**. |
| Mermelada | La fruta de encima **sí se mueve** (`Tile.CanSwap` la permite) y la mermelada se va con ella. |
| Hielo | Sujeta la fruta. **NO** se rompe combinando al lado: sólo cuando esa casilla entra en una combinación o la alcanza un especial. |
| Raíz | Sujeta la fruta. Se corta combinando **al lado**. |
| Chocolate | Dos capas. Combinar al lado **dos veces**. |

**Aviso.** El bucle de vecinos de `ResolveClears` sólo daña `Box`, `Root` y `StickyChoco`; el hielo está deliberadamente fuera, y el comentario de la clase lo confirma. Si algún día se decide que el hielo se derrita rompiendo al lado, es una línea en ese bucle **y hay que cambiar el texto de la tarjeta con ella**, además de rejugar el balance de los niveles 21–30.

### Guardado

`GameState.seenMechanics` es una lista de texto, no una máscara de bits, porque los obstáculos ya se nombran por texto en el contenido y añadir uno nuevo no debe obligar a repartir bits. **No sube `SaveVersion`**: una partida vieja llega sin la clave, la lista sale vacía y el jugador ve las presentaciones a partir de donde esté. Sigue el mismo patrón de guardas que el resto de listas en `Normalize`.

## Archivos

Nuevos: `Scripts/UI/MechanicIntro.cs`. Modificados: `Scripts/Core/GameState.cs`, `Scripts/Core/GameServices.cs`, `Scripts/UI/FrutiCityApp.cs`, `Scripts/UI/EpisodeJourney.cs`, `Scripts/UI/MatchScreens.cs`.

La captura automática incorpora las dos tarjetas de comportamiento, que el modo captura salta a propósito para no bloquear el recorrido: si no se piden a mano, nadie las mira hasta que aparecen en el móvil de un jugador.

## Pruebas

- **115/115 EditMode aprobadas**, Unity 6000.6.0f1, con la ciudad y el minitutorial dentro.
- **Build de Windows correcto**, salida 0.
- **Diecisiete capturas del ejecutable recién construido**, 540×960, en `screenshots/fase-4/`.
- Comprobación rápida de Roslyn limpia tras cada cambio.

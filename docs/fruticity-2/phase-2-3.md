# Fases 2 y 3 — la partida manda, y los menús pisan el pueblo

10 de septiembre de 2026. Continúa [phase-1.md](phase-1.md), cuya corrección al final explica por qué esta sesión empezó revalidando en vez de avanzando.

La regla de oro sigue en pie: **no se ha sustituido ni regenerado un solo asset**. Todo lo de aquí es composición, jerarquía y conexión de contenido que ya existía.

## Lo primero: la fase 1 no se había visto

Tres cosas que los documentos daban por buenas y no lo eran. Están detalladas en la corrección de phase-1.md:

1. Las catorce capturas de la fase 1 estaban **en negro**. `Camera.Render()` no funciona en URP y no da error.
2. Los tests eran **114/115**, no 115/115. El fallo era caché de importación, no un asset roto.
3. El build de Windows moría por **disco lleno**, no por código.

Hasta arreglar lo primero no había forma de juzgar nada, así que fue lo primero que se tocó.

## Canon

El usuario ha resuelto la ambigüedad que la auditoría dejó abierta: **FrutiFriends**, la fruta chibi. Es lo que el código ya hacía (`FruitFriends.UseArticulatedCast => false`). `FrutiCast`, sus FBX, retratos, shader e importador **se conservan íntegros**.

## Cambios

### Portada (§14–15)

Era un clon exacto del Home: mismo fondo, mismo rótulo y las mismas cuatro frutas en las mismas coordenadas. Pulsar JUGAR no parecía llevar a ninguna parte.

Ahora es un cartel: Fresi delante a 350 px, Pablo y Nora un paso detrás y más pequeños, el orden de creación haciendo de profundidad. El rótulo baja de 440 a 380 px de ancho (el 70 % de los 540) para leerse como logotipo y no como titular. Un solo CTA. El lema decorativo se queda aquí, que es donde sirve.

### La partida se queda la pantalla entera (§17)

Fuera monedas, estrellas, rayos y las cinco pestañas mientras se juega: no deciden nada y le roban sitio y atención al tablero. El tablero sube 37 px y la cabecera respira en el hueco. Las ayudas bajan a apoyarse en el borde, porque al quitar la barra de pestañas se quedaron colgadas con 95 px de degradado vacío debajo.

La salida sigue estando en Pausa → «Salir del nivel». **El HUD vuelve justo antes de que vuelen las monedas del premio**: sin eso, `FlyTo(...CoinChip)` mandaba ocho monedas hacia una píldora que no estaba en pantalla.

El rótulo de combo sube los mismos 37 px para seguir cayendo en el cuarto de arriba. **Se queda a 488 px de ancho y no a los 290 que pide el megaprompt**: los nombres en castellano no entran en una placa más estrecha, y estrecharla ya partió el rótulo en dos líneas fuera de la placa una vez. Se respeta la intención (zona superior), no la cifra.

La cinta del martillo salía partida: «MARTILL» arriba y una «O» suelta debajo, pisando la chapa de la cuenta. `UiKit.Label` ajusta línea por defecto; en una cinta de una sola línea es mejor que un nombre largo asome un píxel por los lados.

### Para qué sirven las estrellas (§59–60)

El Home tenía un contador de estrellas subiendo y ningún sitio que dijera para qué. Ahora, donde estaba el lema, dice **«Te faltan 2 ★ para: Un rincón para empezar»**, con el nombre de la tarea de verdad. El botón lleva el precio (`Decorar ★1`) y se pone verde cuando se puede pagar.

La tarjeta de la reforma incorpora la **miniatura del cuarto terminado** con el rótulo «ASÍ QUEDARÁ». La fase 0 es literalmente un cajón vacío: sin la miniatura, el jugador mira una habitación sin nada y no sabe hacia dónde va.

### El contenido que estaba escrito y no se usaba (§65)

`EPISODES.json` trae **treinta nombres de tarea** («Un rincón para empezar», «Leer la etiqueta imposible», «Preparar el primer directo»). La pantalla de reforma los ignoraba y reciclaba una tabla de nueve genéricos con `episode%3`, así que el episodio 4 y el 1 pedían literalmente lo mismo. Ahora sale el nombre real; la tabla se conserva sólo como respaldo por si un JSON llegase incompleto.

### El pueblo, que llevaba meses sin dibujarse (§74)

`Resources/Art/bg_village.png` —una ilustración vertical de un pueblo con fuente, café, plaza y camino— **no se había dibujado nunca**. `SceneBackdrop(bool dim)` se iba al degradado plano cuando `dim` era `true`, y las dos únicas llamadas pasaban `true`. Historia y Vecinos llevaban desde siempre saliendo sobre el azul vacío que el §74 prohíbe, con el pueblo guardado al lado.

Ahora es el fondo de Historia, Vecinos y Reforma, por `SceneArtwork` para que cubra el viewport sin deformarse, con un velo crema al 34 % que mantiene legible el texto de las tarjetas sobre los tejados.

**El tablero no lo usa, a propósito.** Un pueblo lleno de detalle detrás de sesenta y cuatro frutas se come la legibilidad, y el §17 dice que en partida manda el tablero.

En la reforma, además, el resplandor lavanda pasa a luz de miel: el morado enfriaba el cuarto y no está en la paleta del barrio.

### Navegación (§16)

Cinco pestañas pasan a cuatro: Casa, Mapa, Vecinos, Tienda. **Reformar deja de ser pestaña** porque la reforma no es un sitio al que se va, sino algo que le pasa a un rincón concreto; se entra por «Decorar ★n», que además dice lo que cuesta. Estando en la reforma se ilumina Casa.

## Herramienta

`tools/Validate-Unity.ps1` hacía una copia completa del proyecto por ejecución y no borraba ninguna. Treinta y cinco copias llenaron el disco. Ahora:

- **Poda** las carpetas con nombre automático y conserva las bautizadas a mano.
- **Reutiliza** el snapshot con la `Library` caliente, en vez de obligar a Unity a reimportar ~6500 assets de paquetes cada vez. La validación baja de unos veinticinco minutos a unos pocos. Con `-FreshSnapshot` se fuerza la copia limpia.
- Copia con `/MIR` y no `/E`: al reutilizar, un script borrado en el proyecto sobreviviría en la copia y Unity compilaría la clase dos veces.

`ReviewCapture.cs` vuelve a captura síncrona al final del fotograma.

## Archivos modificados

`Scripts/UI/`: `FrutiCityApp.cs`, `MatchScreens.cs`, `CoverScreen.cs`, `RenovationScreen.cs`, `GameFeel.cs`, `ReviewCapture.cs`. `tools/Validate-Unity.ps1`. Documentación en `docs/fruticity-2/`.

Ningún PNG, FBX, fuente, pieza, nivel ni audio tocado. Sin paquetes nuevos, sin cobros, sin backend.

## Pruebas

- **115/115 EditMode aprobadas**, Unity 6000.6.0f1, con todos los cambios de estas fases dentro (`artifacts/editmode-results.xml`).
- **Build de Windows correcto** (`artifacts/unity-buildwindows.log`, salida 0).
- **Las quince capturas salen del juego**, 540×960, en `screenshots/fase-2-3/`. No son montajes: se generan con `-fruticityCapture` sobre el ejecutable recién construido, en el slot VisualQA, sin tocar la partida del usuario.
- Comprobación rápida de Roslyn limpia tras cada cambio.

Aviso para la próxima sesión: `CastAssetTests.ArticulatedCastImportsWithCorrectScaleAndFace` falla de forma intermitente cuando la caché de importación de Unity pierde el artefacto de una textura (`UDS acquire returned invalid read handle`). Es infraestructura, no el asset: se repite la ejecución y pasa. Sólo hay que preocuparse si falla dos veces seguidas.

## Lo que NO entra en estas fases

Ciudad scrollable unificada (§9–11), eventos y temporadas (§25–26), álbum (§27), IAP y tienda con hero (§30–34), Firebase y analytics (§35–38). La reforma sigue siendo una pantalla aparte con la habitación como diorama: la integración «victoria → ciudad → reforma sobre el escenario» es la fase 5 y requiere migración del estado del mapa.

No se atribuye nota comercial ni 60 fps sin medirlo en un dispositivo.

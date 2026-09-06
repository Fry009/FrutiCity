# Punto de continuación

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

`Assets/FrutiCity/` aparece **sin seguimiento** en el repositorio anidado `FrutiCity/`. Todo el código del juego —motor, pantallas, arte 3D, efectos— está sin confirmar. Un borrado accidental lo pierde entero. Es lo primero que debería resolverse.

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

# Punto de continuación

Estado a 6 de septiembre de 2026. Este documento existe para que otra sesión pueda seguir sin releer todo el historial. Dice qué está hecho, qué está verificado, qué decisiones conviene **no** deshacer y qué falta.

## 1. Estado verificado

| Comprobación | Resultado |
| --- | --- |
| Tests EditMode dentro de Unity | **78/78 correctos** |
| Compilación Windows | **Correcta, 0 errores, 3 avisos** |
| Ejecutable | `FrutiCity/Builds/Windows/FrutiCity.exe` |
| Horneado de una pieza 3D | 45–52 ms (presupuesto 220 ms, medido por prueba) |

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

## 4. Decisiones que conviene no deshacer

**`UiKit.Label` usa `VerticalWrapMode.Overflow`, no `Truncate`.** Con `Truncate`, Unity borra la línea entera cuando la caja se queda un píxel corta. Estaba comiéndose títulos de pantalla y diálogos completos sin dar ningún error. Si alguien lo devuelve a `Truncate`, el texto vuelve a desaparecer.

**El arte 3D se hornea una sola vista por pieza, no una rotación.** Se probó con tiras de 16 fotogramas de giro y se descartó: cambiar de sprite a 9 fps se ve a saltos y limita la resolución. Ahora se hornea una vista buena a 128 px con supermuestreo ×3 e iluminación por píxel, y **todo el movimiento va por transformaciones a 60 fps**. Es lo que hacen los match-3 pulidos, y es lo que pidió Fran: que parezca 3D siendo 2D.

**`PieceMotion` es el único dueño del transform de una pieza.** Compone en `LateUpdate` la vida en reposo, los golpes de escala y los desplazamientos que le escribe el animador del tablero. Si otro código escribe `localScale` o `anchoredPosition` de una pieza, pelean y da tirones.

**La sacudida de pantalla se suma dentro de `Fit()`.** `Fit()` recoloca la raíz cada fotograma para el área segura; si la sacudida escribiese la posición por su cuenta, una de las dos ganaría de forma aleatoria.

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

## 6. Trabajo en paralelo

Hubo dos sesiones editando a la vez y chocaron dos veces:

1. Una compilación cogió código a medio guardar (`StarsForWin` llamado antes de existir).
2. Dos compilaciones escribieron en `Builds/Windows` a la vez y Windows bloqueó el archivo.

Si vuelve a haber dos sesiones, que **solo una compile**. La otra puede usar la comprobación rápida de la sección 3, que no toca la carpeta de salida.

## 7. Siguiente paso

La dirección acordada es parecerse a Royal Match con frutas. Lo que falta, por orden de impacto:

1. **Temas de barrio desbloqueables.** Reducir de 50 niveles sueltos a unos 20 bien equilibrados, ligados a zonas que se van abriendo. Fran pidió expresamente menos niveles y más cuidado en la experiencia.
2. **Pulir los efectos jugando.** El marcador, el banner, la sacudida y las monedas voladoras están conectados pero **nadie ha juzgado todavía si se sienten bien**: si el banner tapa el tablero, si la sacudida molesta, si el ritmo es correcto. Eso no sale en una captura estática; hay que abrir el juego.
3. **Detalle pendiente:** en las tarjetas de encargo del taller, la línea de recompensa queda muy pegada al botón.

Nada de esto está validado en un teléfono real. La matriz de dispositivos sigue en [QA.md](QA.md) y los resultados en [VALIDATION_RESULTS.md](VALIDATION_RESULTS.md).

# Arquitectura de FrutiCity

## Estructura

```text
FrutiCity/                         ← raíz del proyecto Unity
  Assets/FrutiCity/
    Scenes/FrutiCity.unity          ← cámara + punto de entrada
    Scripts/
      Core/                        ← contenido, economía, progreso, guardado, servicios
      Merge/                       ← reglas del tablero 7 × 9
      Match3/                      ← motor puro de puzzles y resultados de cascadas
      Art3D/                       ← modelos 3D procedurales, rasterizador y horneado de sprites
      UI/                          ← pantallas, controles y presentación
      FrutiCity.Runtime.asmdef
    Art3D/                         ← shader de color por vértice y destino del exportador
    Resources/
      Content/                     ← JSON del pack y catálogo opcional
      Art/                         ← arte y tipografía
    Editor/                        ← preparación, menús y compilación
    Tests/                         ← pruebas EditMode en assemblies separados
  Packages/                        ← dependencias fijadas por Unity
  ProjectSettings/                 ← ajustes Android y editor
docs/                              ← diseño, arquitectura, QA y publicación
tools/Validate-Unity.ps1            ← validación mediante copia aislada
Frutinovelas_Pro_Pack_v1/            ← material original preservado
```

## Separación de responsabilidades

`GameState` contiene el progreso serializable: monedas, estrellas, energía, inventario, celdas merge, pedidos, profesiones, muebles, niveles, episodios, misiones, recompensa diaria y ajustes. La UI presenta ese estado; las reglas de economía y tableros viven en servicios o modelos de C#.

`GameContent` carga los cinco JSON y valida el catálogo. Conserva los IDs del pack y proporciona búsquedas. `ContentCatalog` es un ScriptableObject opcional que permite asignar TextAssets desde el Inspector. Si se crea, debe estar en `Assets/FrutiCity/Resources/Content/FrutiCityCatalog.asset`; un campo vacío usa el JSON del mismo nombre incluido en Resources. Los datos de contenido se editan fuera del código de gameplay.

`EconomyService` rechaza gastos inválidos, limita saldos y regenera energía a partir de un reloj inyectable. `MergeBoard` conoce posiciones, generadores, recetas 2→1, objetos terminales y consumo de pedidos. La capa que coordina la partida enlaza estas operaciones con recompensas y guardado.

`MatchGame` no depende de Unity. Recibe `MatchConfig` y produce un `MoveResult` con una secuencia de `MatchStep`: intercambio, eliminación, caída, especial o mezcla. Cada paso incluye una instantánea del tablero para animar la misma operación que resolvió el motor. `FindHint` permite indicar movimientos legales; el modelo gestiona victoria, derrota y objetivos. El inventario y el coste de boosters pertenecen al estado de partida, separados de su efecto sobre el puzzle.

`FrutiCityApp` es el componente de entrada que monta la interfaz en tiempo de ejecución. La escena no necesita referencias manuales a decenas de prefabs para empezar. `ProjectBuilder` crea la escena de forma aditiva y la cierra tras guardarla, conservando la escena abierta del usuario. Los builders construyen únicamente esta escena.

## Arte 3D y presentación 2.5D

`Mesh3D` es una malla de triángulos con color por vértice: datos puros, sin `UnityEngine.Mesh`, sin escena y sin dispositivo gráfico. `Shapes3D` construye las primitivas (revolución, esfera, cilindro, cono, disco, caja, prisma extruido con recorte de orejas y tubo con transporte paralelo). `FruitModels` compone con ellas los trece modelos del juego —seis frutas y siete objetos— y los normaliza a la esfera unidad para que todos encuadren igual.

`Rasterizer3D` dibuja esas mallas por software: búfer de profundidad, luz principal fija, iluminación por vértice interpolada, contorno por casco invertido, sombra de contacto y suavizado por supermuestreo. Al no depender del pipeline de render, los mismos píxeles salen en el editor, en un jugador y en una ejecución headless de validación.

`Fruit3D` hornea cada modelo en una tira de dieciséis fotogramas de rotación dentro de una sola textura y los reparte como sprites. `Spin3D` reproduce esa tira sobre un `Image` con fase propia por pieza: eso es el 2.5D, geometría y luz reales presentadas por el lienzo 2D existente. Compartir textura mantiene el batching; la escala queda libre para los golpes de `GameFeel`; con «Reducir animaciones» las piezas se congelan de frente.

Los índices de modelo coinciden con los de `FruitArt`, que sigue sirviendo las partículas, más baratas en 2D. `Art3DExporter` («FrutiCity → Art») escribe mallas `.asset`, prefabs y hojas PNG bajo `Assets/FrutiCity/Art3D/` para poder inspeccionar o sustituir el arte; el juego no depende de esos archivos.

## Guardado

`SaveService` escribe `fruticity-save.json` bajo el directorio que le proporciona el juego (`Application.persistentDataPath` en ejecución). Usa un sobre con versión, JSON y checksum SHA-256; primero escribe un archivo temporal y mantiene una copia `.bak` del estado anterior válido. La recuperación intenta la copia de seguridad si el principal está dañado. Un formato de una versión posterior se protege contra sobrescritura.

El checksum detecta corrupción accidental; no es una medida contra trampas, ni cifra los datos. El guardado local no sincroniza dispositivos. Las pruebas de suspensión Android deben verificar que los puntos de guardado de la UI están conectados a los eventos de aplicación.

## Servicios

`IAnalyticsService`, `IAdsService`, `IIapService` e `ICloudSaveService` son los límites de integración. `OfflineIntegrations` informa que los servicios no están disponibles y devuelve fallo para anuncios, compras y subida de guardado. No entrega premios ni simula transacciones remotas. Los adaptadores reales se incorporan después con configuración de cuenta y pruebas específicas.

## Rendimiento y ampliación

El catálogo pequeño se carga desde Resources para simplificar la entrega. Addressables, múltiples escenas aditivas y descarga remota no son necesarios para este volumen. Los modelos de tablero reutilizan su estado; las instantáneas de cascadas, reconstrucciones de pantallas y efectos generan trabajo y asignaciones que deben medirse en dispositivos reales antes de fijar presupuestos.

El objetivo de 60 FPS no se da por conseguido por compilar. Para ampliación: perfilar UI y texturas, convertir arte a atlas por pantalla, reutilizar las vistas que más se reconstruyan, medir memoria tras diez minutos de juego y evaluar batching con Unity Profiler. No introducir SDKs remotos en las clases puras del motor.

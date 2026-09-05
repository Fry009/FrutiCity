# Resultados de validación

Fecha de trabajo: 5 de septiembre de 2026. Entorno: Windows 11 y Unity 6000.6.0f1.

## Comprobaciones completadas durante la implementación

- Auditoría del Pro Pack: seis personajes, tres cadenas de siete objetos, cincuenta niveles, tres habitaciones/diez slots/treinta variantes y diez episodios.
- Motor match-3 compilado con Roslyn y ejecutado con Mono/NUnit: **26/26 pruebas correctas**. Incluye aperturas jugables sin matches, determinismo, intercambios inválidos, cascadas, creación/encadenado de especiales, cinco obstáculos, boosters y victoria/derrota.
- Los objetivos de cajas y mermelada del pack se validan aunque la lista original de obstáculos no los enumere.

## Integración ejecutada el 5 de septiembre de 2026

Las cuatro pantallas que faltaban (`MergeScreen`, `Rooms`, `StoryScreen`, `Shop`) estaban referenciadas pero no existían, de modo que el proyecto no compilaba y no se podía ejecutar nada. Implementadas, la integración se validó por primera vez de extremo a extremo con `tools/Validate-Unity.ps1` sobre copias aisladas:

- **Tests EditMode dentro de Unity: 78/78 correctos** (`artifacts/editmode-results.xml`). Incluye las 26 pruebas del motor match-3, que hasta ahora solo se habían ejecutado fuera del editor, y 52 nuevas de geometría y rasterizado 3D.
- **Compilación Windows: correcta, 0 errores, 3 avisos**, 110 MB, ejecutable en `FrutiCity/Builds/Windows/FrutiCity.exe` (`artifacts/unity-buildwindows.log`).
- **Horneado de una pieza 3D: 45 ms** a 128 px con supermuestreo ×3, medido por la prueba de presupuesto. Las trece piezas se reparten a una por fotograma al arrancar.
- Los paquetes añadidos (Memory Profiler 1.1.12, Android Logcat 1.4.7, Profile Analyzer 1.4.0) se resuelven y descargan correctamente.
- La licencia de Unity se resuelve en modo batch sin intervención (`Successfully resolved entitlement details`).
- **Capturas del ejecutable revisadas**: `FrutiCity.exe -fruticityCapture <carpeta> -fruticityQuitAfterCapture` genera las cinco pantallas y sale con código 0. Mirarlas destapó tres defectos que ninguna prueba automática podía ver: `Label` con `Truncate` borraba títulos y diálogos enteros cuando la caja se quedaba corta, `EPISODES.json` tenía 119 acentos convertidos en `?` por una codificación errónea, y los nombres de hueco de decoración se mostraban con su identificador en inglés. Los tres corregidos.

Los avisos de compilación son previos a este trabajo: `FindFirstObjectByType` está marcado como obsoleto en `FrutiCityApp` y `ProjectBuilder`.

La instalación original de Unity tenía módulos Windows y WebGL. Se inició la instalación de Android Build Support y sus dependencias mediante Unity Hub. Un módulo descargándose no equivale a un APK generado.

## Sin validar en esta estación

- Aspecto y tacto reales del juego en marcha: las pruebas comprueban geometría, píxeles y compilación, no si la animación se percibe fluida ni si el arte alcanza el listón visual buscado. Eso se juzga jugando.
- Comportamiento táctil y rendimiento de un teléfono Android físico.
- Safe areas reales, accesibilidad asistida, temperatura y memoria en gama media.
- Balance humano y tasas de victoria de los cincuenta niveles.
- Firma de producción, subida a Play Console y revisión de tienda.
- SDKs y consolas reales de Firebase/AdMob, consentimientos y despliegue de Cloudflare.

Los registros temporales se escriben en `artifacts/` y los ejecutables en `FrutiCity/Builds/`; ambos se excluyen de Git. La matriz y el recorrido de aceptación están en [QA.md](QA.md).

# QA de FrutiCity

## Cómo reproducir la validación

En Unity: Window → General → Test Runner → EditMode → Run All. Las pruebas se organizan en assemblies de Editor separados del juego. Alternativamente, `tools/Validate-Unity.ps1 -Action Tests` crea una copia aislada y escribe `artifacts/editmode-results.xml`.

`tools/Validate-Unity.ps1 -Action BuildWindows` compila en una copia aislada y entrega el ejecutable en `FrutiCity/Builds/Windows/`. El registro completo está en `artifacts/unity-buildwindows.log`; el resumen del builder está junto a la carpeta de salida. El script no cierra ni reutiliza la instancia de Unity del usuario.

## Recorrido manual de aceptación

1. **Primera sesión:** arranque limpio, bienvenida de Mona y siguiente acción comprensible; no hay botones fuera de pantalla ni textos recortados.
2. **Taller:** generar, seleccionar/arrastrar, fusionar, mover a una celda vacía, intentar una fusión inválida y comprobar el nivel máximo. Completar un pedido consume exactamente sus objetos y concede el premio una sola vez.
3. **Economía:** gastar con saldo exacto y saldo insuficiente; volver tras suspensión; comprobar que cambiar el reloj hacia atrás no produce energía adicional. Ningún saldo se vuelve negativo.
4. **Puzzle:** intercambio válido e inválido, cascadas, cohete, bomba, arcoíris, cada obstáculo y objetivo; ganar en el último movimiento, perder, reintentar y volver a casa. La animación debe bloquear nuevas jugadas durante su resolución.
5. **Ayudas:** usar cada booster con inventario disponible y agotado; pista válida; mezcla que deja una jugada posible sin regalar progreso del objetivo.
6. **Casa e historia:** colocar un mueble, cambiar su variante, cambiar de habitación, avanzar episodio y reabrir el juego. La elección y la tarea deben conservarse sin cobrar dos veces.
7. **Diario y tienda:** reclamar una vez, intentar reclamar otra vez, comprobar los siete días y las misiones. Las compras con monedas reflejan el coste antes de confirmar.
8. **Ajustes:** sonido, música, vibración y movimiento reducido; salir y entrar para confirmar persistencia. Atrás/Escape cierra primero el panel activo.
9. **Guardado:** cerrar después de un premio, reabrir y revisar estado. Sobre una copia de prueba, corromper el principal y comprobar recuperación desde `.bak`; no usar la partida personal para esta prueba.
10. **Sesión larga:** alternar todas las pantallas durante diez minutos, jugar varios niveles, suspender/reanudar y vigilar errores, memoria y fluidez.

## Matriz de dispositivo

| Entorno | Validación necesaria |
| --- | --- |
| Windows 540 × 960 | Arranque, controles con ratón, pantalla vertical y captura |
| Android 16:9, 720p | Lectura de textos y tamaño de toque |
| Android 19.5:9 / 20:9 con recorte | Safe area, barras del sistema, diálogos y navegación |
| Tableta Android | Escalado y proporciones sin estirar ilustraciones |
| Android con 3–4 GB RAM | FPS, memoria, temperatura y reanudación |
| Android API 26 y API 36 | Compatibilidad mínima/objetivo, audio, escritura y botones del sistema |
| Dispositivo con ajustes de accesibilidad | Lectura, formas distinguibles sin depender solo de color, movimiento reducido |

Las pruebas automáticas de lógica no sustituyen interacción táctil, accesibilidad, perfilar 60 FPS, equilibrio de los 50 niveles ni revisión de personas de diferentes edades.

## Estado de validación

Este documento distingue el procedimiento de sus resultados. Los resultados ejecutados y sus limitaciones se registran en `docs/VALIDATION_RESULTS.md` al finalizar la integración. No se debe interpretar esta lista de comprobación como una lista ya superada.

# FrutiCity 2 — cambios

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

# FrutiCity · Unity

Un barrio tropical, seis frutas con personalidad y una casa que vuelve a la vida. FrutiCity conecta puzzles match-3, un taller de fusiones, encargos, decoración e historias cortas. Proyecto Android vertical basado en el **Frutinovelas Pro Pack v1** original; la marca y el paquete definitivos son **FrutiCity** y **`com.khamesoul.fruticity`**.

## Abrir y jugar

1. En Unity Hub abre **la carpeta `FrutiCity/` que contiene `Assets`, `Packages` y `ProjectSettings`**, dentro de este repositorio.
2. Usa **Unity 6000.6.0f1**, la versión ya instalada. Espera a que termine la importación y compilación.
3. Elige **FrutiCity → Open game**. La escena es `Assets/FrutiCity/Scenes/FrutiCity.unity`.
4. En Game, selecciona un formato **9:16** (540 × 960 o 1080 × 1920) y pulsa **Play**.

La escena inicial se genera al importar los scripts, conservando la escena que tengas abierta. La interfaz se construye al jugar; por eso la jerarquía de la escena es pequeña. Los controles admiten ratón en PC y interacción táctil en móvil.

Las frutas y los objetos son modelos 3D construidos por código y horneados en tiras de rotación, que la interfaz reproduce con fase propia por pieza: de ahí el aspecto 2.5D. Se puede desactivar el movimiento en **Ajustes → Reducir animaciones**.

## Compilar

- **FrutiCity → Build → Windows preview** crea `FrutiCity/Builds/Windows/FrutiCity.exe` para probar el juego inmediatamente en PC. Conserva toda la carpeta junto al ejecutable al compartirlo.
- **FrutiCity → Build → Android development APK** crea un APK de pruebas cuando esté instalado Android Build Support, con SDK, NDK y OpenJDK.
- **FrutiCity → Build → Android signed App Bundle** crea el AAB con tu clave de subida configurada fuera del repositorio. No sube ni publica nada en Play Console.
- **FrutiCity → Capture preview** guarda una captura de Game durante Play en `FrutiCity/Builds/Screenshots/`.
- **FrutiCity → Art → Export 3D models** escribe las mallas y los prefabs de los trece modelos en `Assets/FrutiCity/Art3D/`, y **Export turnaround sheets** guarda sus hojas de rotación en PNG. El juego genera todo eso en memoria al arrancar: exportar sirve para mirarlo, retocarlo o sustituirlo por arte propio.

Para validar sin cerrar tu Editor se puede ejecutar `tools/Validate-Unity.ps1`. El script prepara una copia aislada bajo `.validation/` y guarda registros en `artifacts/`. Los resultados de cada ejecución deben revisarse; la presencia de tests no significa por sí sola que hayan pasado.

```powershell
powershell -ExecutionPolicy Bypass -File tools/Validate-Unity.ps1 -Action Tests
powershell -ExecutionPolicy Bypass -File tools/Validate-Unity.ps1 -Action BuildWindows
```

## Documentación

- [Punto de continuación: estado, recetas y siguiente paso](docs/HANDOFF.md)
- [Auditoría del Pro Pack y decisiones de alcance](docs/PRO_PACK_AUDIT.md)
- [Arquitectura y edición del contenido](docs/ARCHITECTURE.md)
- [QA, dispositivos y estado de validación](docs/QA.md)
- [Android, Play Store, Firebase, AdMob y Cloudflare](docs/ANDROID_AND_SERVICES.md)

Esta entrega se valida como juego local. La publicación, firma de producción, pruebas en dispositivos y conexión a tus cuentas son fases diferenciadas y quedan identificadas en la documentación. El prototipo funciona sin anuncios obligatorios, compras reales ni servidor.

# FrutiCity Diorama — pipeline de arte

Fase 1, 2026-09-09. El canon procedural se incorpora en `art/blender/diorama_style.py`. Importarlo no importa `bpy`, no crea objetos y no cambia escenas. Los generadores antiguos siguen intactos; sus renders y los personajes que usa Unity **todavía no están migrados**.

## Fuente y uso

La paleta `PALETTE` reproduce los colores del encargo. `linear_color` convierte sRGB a valores lineales de Blender con la transferencia sRGB exacta. `tonal_family` ofrece guías shadow/base/highlight con valor HSV ×0,80 / ×1 / ×1,12, limitando el highlight a 1. La luz sigue siendo suave: no se aplica una cuantización de tres bandas.

Desde un generador Blender que tenga `art/blender` en `sys.path`:

```python
import diorama_style as style

skin = style.material("Fresi / fruit", "fresi", "fruit")
shirt = style.material("Pablo / shirt", "blue", "clothes")
facade = style.material("Market / facade", "cream", "building")
wood = style.material("Market / crates", "wood_light", "wood")
lights = style.lighting_rig(target=(0, 0, 1), namespace="market")
# Solo si este generador controla la configuración de render:
style.configure_render(bpy.context.scene)
```

Los materiales y luces llevan etiquetas de propiedad `FrutiCity.Diorama.v1`; las llamadas repetidas actualizan sus propios datablocks. Un material del usuario con el mismo nombre visible no se reutiliza ni se modifica. Cada rig pertenece a una escena y namespace. No se borran luces ajenas, ni se vacía la escena: el generador debe decidir explícitamente qué hacer con su iluminación anterior para evitar sumar dos rigs.

## Materiales y luz

| Categoría | Metallic | Roughness | Specular IOR Level | Coat Weight |
|---|---:|---:|---:|---:|
| Fruta | 0 | 0,37 | 0,31 | 0,02 |
| Ropa | 0 | 0,53 | 0,235 | 0 |
| Madera | 0 | 0,51 | 0,21 | 0 |
| Edificios | 0 | 0,52 | 0,21 | 0 |

Los nombres de sockets se comprobaron en Blender **5.2.1 LTS**: `Specular IOR Level`, `Coat Weight`, `Coat Roughness`, `Subsurface Weight` y `Transmission Weight`. Fruta sin metallic, transmisión ni subsurface. Las cantidades están dentro de los intervalos solicitados; los defaults anteriores no se cambian silenciosamente.

El frente del personaje mira hacia −Y. Key cálida a 35° laterales y 45° elevados; fill ligeramente turquesa; rim cálida discreta. Las tres luces AREA comparten distancia y tamaño de emisor. Energías relativas **1 / 0,425 / 0,20**. Al cambiar `scale`, las posiciones y tamaños escalan linealmente y la energía al cuadrado. La potencia base puede ajustarse al encuadre; no cambia la relación. `configure_render` usa Cycles, denoising y Standard sin look, exposición 0 y gamma 1.

La guía de sombra de contacto queda declarada como `CONTACT_SHADOW`: opacidad 24 %, desplazamiento vertical 6 px y blur 11 px a anchura visual 540. Son parámetros para composición PNG/UI: el rig no añade una sombra falsa a los renders ni los aplica todavía al runtime. La muestra usa sombras físicas para comparar volúmenes.

## Regenerar la muestra

Desde la raíz del repositorio:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --factory-startup --python 'art\blender\diorama_style.py' -- --preview
```

`--output 'ruta.png'` cambia únicamente la salida. La muestra crea una escena propia, conserva la escena activa del usuario y vuelve a ella al terminar. Comprueba parámetros reales de material, reutilización de materiales/luces y conservación de objetos previos. Emite `DIORAMA_VALIDATION` con el resultado. Las muestras planas inferiores usan emisión para mostrar los hex sRGB exactos; los cuatro volúmenes superiores sí usan Principled y el rig canónico.

Resultado: [muestra de materiales](screenshots/phase-1/00-material-canon.png), 1500 × 1050. Es una lámina de dirección técnica; no es una captura de gameplay.

## Integración por fases

En fase 2, adaptar `frutis.py` / `fresita_sheet.py` al canon y revisar la portada antes de exportar a Unity. `export_cast_fbx.py` sigue exportando el reparto v3 y debe corregirse durante esa migración: los modelos que carga `CastPortrait` prevalecen sobre sus PNG. Mantener rig y expresiones v5, sustituyendo progresivamente el reparto antiguo.

Después, aplicar el mismo módulo a edificios y props de la ciudad. Conservar `comun.py` para primitivas geométricas; sustituir sus materiales y luces de forma explícita al revisar cada generador. Los valores de color de UI están en el tema Unity; ambos lados se contrastan contra la paleta del encargo, sin añadir por ahora otro manifiesto JSON redundante.

El pipeline existente `python art/blender/hacer.py` continúa generando caras → modelos → esqueletos → renders → composiciones. No se ha ejecutado esa regeneración completa en fase 1. Tampoco se han cambiado FBX, sprites existentes, importers de Unity, música ni archivos de referencia.

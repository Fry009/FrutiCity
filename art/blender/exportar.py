"""Graba los assets: por cada pieza, un PNG master a 512, la prueba real
a 128 y su .blend.

Se ejecuta en Blender headless, una pieza por proceso:

    blender --background --python exportar.py -- manzana
    blender --background --python exportar.py -- TODAS

**Cycles, no EEVEE.** En `--background` EEVEE puede escupir un PNG vacio
sin dar ningun error; Cycles no. Es una trampa ya pagada.

Y el control de calidad es MIRAR el PNG de 128: camaras apuntando al
suelo, normales del reves y hojas vistas de canto no dan error en
consola, solo salen mal en la imagen.
"""
import bpy, os, sys, runpy, traceback

AQUI = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
SALIDA = os.path.join(AQUI, "assets")

FRUTAS = ["manzana", "platano", "fresa", "naranja", "uvas", "kiwi"]
ESPECIALES = ["estrella", "moneda", "energia", "caja", "bomba", "cohete", "martillo"]
TODAS = FRUTAS + ESPECIALES

MUESTRAS = 220
TAMANOS = (512, 128)


def preparar():
    S = bpy.context.scene
    S.render.engine = 'CYCLES'
    S.cycles.samples = MUESTRAS
    S.cycles.use_denoising = True
    S.render.film_transparent = True            # el tile va sobre el tablero
    S.render.image_settings.file_format = 'PNG'
    S.render.image_settings.color_mode = 'RGBA'
    S.view_settings.view_transform = 'Standard'  # sin Filmic: los colores son los que son
    return S


def una(nombre):
    modelo = os.path.join(AQUI, "modelo_%s.py" % nombre)
    if not os.path.exists(modelo):
        print("[exportar] no existe", modelo)
        return False
    runpy.run_path(modelo, run_name="__main__")
    S = preparar()
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    for px in TAMANOS:
        S.render.resolution_x = S.render.resolution_y = px
        S.render.filepath = os.path.join(SALIDA, "%s_%d.png" % (nombre, px))
        bpy.ops.render.render(write_still=True)
        print("[exportar] PNG", nombre, px)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(SALIDA, "%s.blend" % nombre))
    print("[exportar] BLEND", nombre)
    return True


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if AQUI not in sys.path: sys.path.insert(0, AQUI)
    pedidas = argv or ["manzana"]
    if len(pedidas) == 1 and pedidas[0].upper() == "TODAS":
        pedidas = TODAS
    fallos = []
    for n in pedidas:
        try:
            if not una(n): fallos.append(n)
        except Exception:
            traceback.print_exc()
            fallos.append(n)
    print("[exportar] hechas:", len(pedidas) - len(fallos), "de", len(pedidas))
    if fallos:
        print("[exportar] FALLARON:", ", ".join(fallos))

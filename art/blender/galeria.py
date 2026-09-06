"""Las seis frutas a la vez, en fila y con la misma luz.

Es la unica vista que sirve para juzgar si la familia casa: una fruta
suelta siempre parece correcta, y solo al ponerlas juntas se ve que una
brilla mas que las otras o que una pesa menos en el tile.

Truco necesario: cada modelo_*.py recarga comun.py al importarse, asi que
el parche que protege lo ya montado hay que ponerlo DESPUES del reload,
no antes. Puesto antes, cada fruta borraba a la anterior.
"""
import os, sys, importlib, bpy
from mathutils import Matrix, Vector

_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)

FRUTAS = ["manzana", "platano", "fresa", "naranja", "uvas", "kiwi"]
ESPECIALES = ["estrella", "moneda", "energia", "caja", "bomba", "cohete", "martillo"]
PASO = 2.15                  # separacion entre piezas
FILA = 2.35                  # separacion entre filas
CAM = ((0, -26.0, 0.0), 50)  # posicion y lente para que quepan las trece


def montar(filas=None):
    """filas: lista de listas. Por defecto, frutas arriba y especiales abajo."""
    filas = filas or [FRUTAS, ESPECIALES]
    plano = [n for f in filas for n in f]
    comun.limpiar()
    for c in list(bpy.data.collections): bpy.data.collections.remove(c)
    gal = bpy.data.collections.new("Galeria")
    bpy.context.scene.collection.children.link(gal)

    def limpiar_salvo():
        prot = set(gal.all_objects)
        for o in list(bpy.data.objects):
            if o not in prot: bpy.data.objects.remove(o, do_unlink=True)
        for col in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
            for d in list(col):
                if d.users == 0: col.remove(d)

    for fi, fila in enumerate(filas):
        dz = ((len(filas) - 1) / 2.0 - fi) * FILA
        for i, n in enumerate(fila):
            m = importlib.import_module("modelo_" + n)
            importlib.reload(m)              # esto recarga comun por dentro...
            comun.limpiar = limpiar_salvo    # ...asi que el parche va DESPUES
            m.construir()
            # normalizar aqui, no en la ficha: en el tile de verdad cada
            # pieza la encuadra su propia camara, asi que el tamano solo
            # importa cuando se ven unas al lado de otras.
            propias = comun._vivos()      # no por coleccion: ver comun._nace
            comun.encajar(propias)
            T = Matrix.Translation(((i - (len(fila) - 1) / 2.0) * PASO, 0, dz))
            for o in propias:
                o.matrix_world = T @ o.matrix_world
                for c in list(o.users_collection): c.objects.unlink(o)
                gal.objects.link(o)

    importlib.reload(comun)                  # deja comun.limpiar como estaba
    comun.luces()
    cam = comun.camara()
    cam.location, cam.data.lens = CAM[0], CAM[1]
    cam.rotation_quaternion = (Vector((0, 0, 0.1)) - cam.location).to_track_quat('-Z', 'Y')

    for area in (bpy.context.screen.areas if bpy.context.screen else []):
        if area.type != 'VIEW_3D': continue
        area.spaces[0].shading.type = 'MATERIAL'
        for region in area.regions:
            if region.type != 'WINDOW': continue
            with bpy.context.temp_override(area=area, region=region):
                bpy.ops.view3d.view_camera()
    print("[galeria]", ", ".join(plano))
    return gal


def renderizar(ruta, ancho=1800, alto=700, muestras=200):
    """Saca la galeria a PNG con Cycles. El visor usa otro motor y otra
    luz, asi que una captura del visor no vale para juzgar el resultado:
    hay que renderizar lo mismo que se va a exportar."""
    S = bpy.context.scene
    S.render.engine = 'CYCLES'
    S.cycles.samples = muestras
    S.cycles.use_denoising = True
    S.render.film_transparent = False
    S.world.color = (1.0, 1.0, 1.0)
    S.render.image_settings.file_format = 'PNG'
    S.view_settings.view_transform = 'Standard'
    S.render.resolution_x, S.render.resolution_y = ancho, alto
    S.render.filepath = ruta
    bpy.ops.render.render(write_still=True)
    print("[galeria] renderizada en", ruta)
    return ruta


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    solo_frutas = "frutas" in argv
    montar([FRUTAS] if solo_frutas else None)
    destino = [a for a in argv if a.lower().endswith(".png")]
    if destino:
        renderizar(destino[0])

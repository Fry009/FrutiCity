"""Renders de portada y de las pantallas de victoria y derrota.

Todo sale del mismo sitio: los .blend con rig de fresita_v5. La pose se
elige poniendo un fotograma de la accion Fresita_Demo, y el humor se elige
cambiando la imagen del calco de la cara. No hay modelos aparte para
ganar o perder.

    Fresita_Demo:  1-60 respirar | 61-110 saludar | 111-170 saltar
                   171-230 derrota

Uso (por personaje, porque cada uno vive en su .blend):
    blender -b fresita_v5/fresi_rig.blend --python escenas.py -- portada
    blender -b fresita_v5/fresi_rig.blend --python escenas.py -- victoria
    blender -b fresita_v5/fresi_rig.blend --python escenas.py -- derrota
"""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import fresita_sheet as F

OUT = HERE / 'fresita_v5'
ESCENAS = OUT / 'escenas'
ESCENAS.mkdir(exist_ok=True)

# pose de portada por personaje: (fotograma, expresion, giro de camara)
PORTADA = {
    "fresi": (132, "alegre", 0),      # en el aire, brazos arriba
    "pablo": (88, "alegre", -14),     # saludando
    "nora":  (30, "guino", 12),       # de pie, respirando
}


def quien():
    return Path(bpy.data.filepath).stem.replace("_rig", "") or "fresita"


def camara(alto=0.86, ancho=2.10, giro=0.0):
    s = bpy.context.scene
    cam = bpy.data.objects.get("CamEscena")
    if cam is None:
        cd = bpy.data.cameras.new("CamEscena")
        cd.type = 'ORTHO'
        cam = bpy.data.objects.new("CamEscena", cd)
        s.collection.objects.link(cam)
    cam.data.ortho_scale = ancho
    s.camera = cam
    a = math.radians(giro)
    cam.location = (6.0 * math.sin(a), -6.0 * math.cos(a), alto)
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector((0, 0, alto)) - Vector(cam.location)).to_track_quat('-Z', 'Y')
    return cam


def motor(rapido):
    s = bpy.context.scene
    if rapido:
        for m in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE', 'CYCLES'):
            try:
                s.render.engine = m
                break
            except Exception:
                continue
    else:
        s.render.engine = 'CYCLES'
        s.cycles.samples = 64
        s.cycles.use_denoising = True


def portada():
    """Un recorte grande y limpio de cada personaje, con alfa, para
    montarlo luego sobre el fondo."""
    nombre = quien()
    frame, expresion, giro = PORTADA.get(nombre, (1, "idle", 0))
    F.poner_cara(expresion)
    s = bpy.context.scene
    s.frame_set(frame)
    F.escena_render()
    motor(False)
    s.render.resolution_x, s.render.resolution_y = 900, 1400
    camara(alto=0.86, ancho=2.05, giro=giro)
    s.render.filepath = str(ESCENAS / ("portada_%s.png" % nombre))
    bpy.ops.render.render(write_still=True)
    print("PORTADA", s.render.filepath, flush=True)


def tira(clase, desde, hasta, expresion, paso=3, alto=0.90, ancho=2.20):
    nombre = quien()
    F.poner_cara(expresion)
    s = bpy.context.scene
    F.escena_render()
    motor(True)
    s.render.resolution_x, s.render.resolution_y = 340, 470
    camara(alto=alto, ancho=ancho)
    for fr in range(desde, hasta + 1, paso):
        s.frame_set(fr)
        s.render.filepath = str(ESCENAS / ("%s_%s_%03d.png" % (nombre, clase, fr)))
        bpy.ops.render.render(write_still=True)
    print("TIRA %s %s" % (nombre, clase), flush=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["portada"]
    if "portada" in argv:
        portada()
    if "victoria" in argv:
        tira("victoria", 112, 170, "alegre")
    if "derrota" in argv:
        tira("derrota", 172, 230, "triste")
    print("ESCENAS LISTAS", flush=True)


if __name__ == "__main__":
    main()

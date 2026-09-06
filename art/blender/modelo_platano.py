"""Ficha de platano - FrutiCity. Estilo Royal Match.
La unica de las seis que no es de revolucion: es un barrido de seccion a
lo largo de un arco. La seccion es un triangulo redondeado, que es lo que
distingue un platano de una salchicha amarilla.
"""
import os, sys, math, importlib
from mathutils import Vector
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *
import bmesh

# ============ MANDOS ============
COLOR_PIEL  = "FFC62E"   # amarillo maduro
COLOR_PUNTA = "6E4A1B"   # las dos puntas oscuras
BRILLO      = 0.80
RUGOSIDAD   = 0.33

CURVA    = 0.95     # radio del arco. MENOR = mas curvado
ABRE     = 116.0    # grados de arco: cuanto abraza la sonrisa
GORDO    = 0.325    # radio maximo de la seccion
AFILADO  = 0.52     # como adelgaza hacia las puntas (bajo = poco)
PUNTA    = 0.055    # radio minimo en las puntas (0 = pico, feo al suavizar)
ARISTAS  = 0.17     # cuanto se nota el triangulo. 0 = tubo redondo
GIRO     = -28.0    # inclinacion en el tile, para que llene el cuadrado
# ================================

PASOS, SEG = 44, 24
BORDE = 2           # anillos de cada extremo que van en color punta


def cuerpo():
    bm = bmesh.new()
    a = math.radians(ABRE) / 2.0
    anillos = []
    for i in range(PASOS + 1):
        t = i / PASOS
        th = -a + 2.0 * a * t
        # centro del arco: sonrisa (los extremos suben)
        c = Vector((CURVA * math.sin(th), 0.0, CURVA * (1.0 - math.cos(th))))
        fuera = Vector((math.sin(th), 0.0, -math.cos(th)))   # normal del arco
        lado = Vector((0.0, 1.0, 0.0))
        r = GORDO * max(PUNTA, math.sin(math.pi * t) ** AFILADO)
        anillo = []
        for j in range(SEG):
            phi = 2.0 * math.pi * j / SEG
            k = 1.0 + ARISTAS * math.cos(3.0 * phi)   # triangulo redondeado
            anillo.append(bm.verts.new(c + (fuera * math.cos(phi) +
                                            lado * math.sin(phi)) * (r * k)))
        anillos.append(anillo)

    oscuras = []
    for i in range(PASOS):
        for j in range(SEG):
            j2 = (j + 1) % SEG
            f = bm.faces.new((anillos[i][j], anillos[i][j2],
                              anillos[i + 1][j2], anillos[i + 1][j]))
            if i < BORDE or i >= PASOS - BORDE:
                oscuras.append(f)
    oscuras.append(bm.faces.new(list(reversed(anillos[0]))))
    oscuras.append(bm.faces.new(anillos[-1]))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in oscuras:
        f.material_index = 1

    # centrar: el arco nace en el origen, no centrado en el
    xs = [v.co.x for v in bm.verts]; zs = [v.co.z for v in bm.verts]
    dx = -(max(xs) + min(xs)) / 2.0; dz = -(max(zs) + min(zs)) / 2.0
    for v in bm.verts:
        v.co.x += dx; v.co.z += dz

    me = bpy.data.meshes.new("Platano"); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new("Platano", me)
    bpy.context.scene.collection.objects.link(ob)
    return comun._nace(ob)      # que cuente para medir y encuadrar


def construir():
    empezar()
    ob = cuerpo()
    ob.data.materials.append(mat("Piel", hexcol(COLOR_PIEL), RUGOSIDAD, BRILLO))
    ob.data.materials.append(mat("Punta", hexcol(COLOR_PUNTA), .70))
    suave(ob, 2)
    ob.rotation_euler = (0, math.radians(GIRO), 0)
    encajar([ob])          # es la unica alargada: sin esto se sale del tile

    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return ob


if __name__ == "__main__":
    construir()

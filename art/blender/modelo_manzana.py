"""Ficha de manzana - FrutiCity / Frutinovelas. Estilo Royal Match.
Guardar este archivo hace que Blender lo reconstruya solo si live.py corre.
El perfil NO son puntos a mano: se genera con una funcion, para que la
curvatura sea continua y no salgan escalones ni tramos rectos.
"""
import bpy, bmesh, math
from mathutils import Vector

# ============ MANDOS ============
COLOR_PIEL   = "F0453C"   # rojo caramelo
COLOR_HOJA   = "4FA83A"   # verde hoja, no lima
COLOR_TALLO  = "6B4423"
BRILLO       = 0.85       # barniz: el brillo gordo de Royal Match
BRILLO_NITIDO= 0.10       # bajo = highlight definido
RUGOSIDAD    = 0.30

REDONDEZ     = 0.72       # <1 ensancha (mas gordita). 1.0 = esfera
ALTO         = 0.88       # escala vertical
HOYUELO      = 0.24       # profundidad del hoyuelo de arriba
HOYUELO_CULO = 0.15       # el de abajo, siempre menor
HOYUELO_ANCHO= 0.46       # ESTRECHO = hoyuelo. Ancho = tapa de bote.
ANCHO        = 0.84

LOBULOS      = 5
LOBULO_FUERZA= 0.018      # bajo: un surco en la silueta parece abolladura
LOBULO_FASE  = 36.0       # grados, aparta los surcos del borde visible
CARA         = False
LUZ_CLAVE    = 500
LUZ_PUNTO    = 700
LUZ_CONTRA   = 340
# ================================

PASOS, SEG = 40, 64

def perfil():
    """Ovoide con hoyuelo arriba y abajo. Un solo maximo -> sin barril."""
    pts = []
    for i in range(PASOS + 1):
        phi = math.pi * i / PASOS          # 0 = polo norte, pi = polo sur
        r = math.sin(phi) ** REDONDEZ
        z = math.cos(phi) * ALTO
        # el hoyuelo hunde el eje y se desvanece hacia el ecuador
        caida = math.exp(-(r / HOYUELO_ANCHO) ** 2)
        z -= caida * (HOYUELO if z >= 0 else -HOYUELO_CULO)
        pts.append((r, z))
    return pts

def hexcol(h, a=1.0):
    h = h.lstrip("#")
    return tuple((int(h[i:i+2], 16) / 255.0) ** 2.2 for i in (0, 2, 4)) + (a,)

def limpiar():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(name, rgba, rough, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba
    b.inputs["Roughness"].default_value = rough
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = BRILLO_NITIDO
    return m

def cuerpo():
    bm = bmesh.new(); prev = None
    for r, z in perfil():
        v = bm.verts.new((r * ANCHO, 0.0, z))
        if prev is not None: bm.edges.new((prev, v))
        prev = v
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    bmesh.ops.spin(bm, geom=list(bm.verts) + list(bm.edges), angle=math.radians(360),
                   steps=SEG, axis=(0, 0, 1), cent=(0, 0, 0), use_merge=False)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    for v in bm.verts:
        x, y, z = v.co
        r = math.hypot(x, y)
        if r < 1e-5: continue
        t = max(0.0, min(1.0, (0.45 - z) / 1.2))
        ang = math.atan2(y, x) + math.radians(LOBULO_FASE)
        k = 1.0 + LOBULO_FUERZA * (t ** 1.5) * math.cos(LOBULOS * ang)
        v.co.x, v.co.y = x * k, y * k
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("TileManzana"); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new("Manzana", me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat("Piel", hexcol(COLOR_PIEL), RUGOSIDAD, BRILLO))
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.shade_smooth()
    s = ob.modifiers.new("Sub", 'SUBSURF'); s.levels = 2; s.render_levels = 2
    return ob

def hoja(largo=.58, ancho=.125, nervio=.032, curva=.12):
    """ancho = SEMIancho. Relacion ~2.3:1 largo/ancho para que lea a hoja."""
    N, bm = 14, bmesh.new()
    filas = []
    for i in range(N + 1):
        t = i / N
        w = ancho * math.sin(math.pi * t) ** 0.62      # puntiaguda en t=0 y t=1
        alza = curva * (t ** 1.6)                       # se dobla hacia la punta
        fila = []
        for j in (-1, 0, 1):
            z = alza + (nervio * math.sin(math.pi * t) if j == 0 else 0.0)
            fila.append(bm.verts.new((t * largo, j * w, z)))
        filas.append(fila)
    for i in range(N):
        for k in (0, 1):
            a, b = filas[i][k], filas[i][k + 1]
            c, d = filas[i + 1][k + 1], filas[i + 1][k]
            try: bm.faces.new((a, b, c, d))
            except ValueError: pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("Hoja"); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new("Hoja", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def luz(name, energia, loc, tam):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = energia; d.size = tam
    o = bpy.data.objects.new(name, d); o.location = loc
    bpy.context.scene.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y')

def construir():
    limpiar()
    ob = cuerpo()
    suelo = ALTO - HOYUELO      # fondo del hoyuelo: ahi nace el rabito

    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=.095, radius2=.080,
                                    depth=.30, location=(0, 0, suelo + .11))
    st = bpy.context.object; st.name = "Rabito"
    st.rotation_euler = (math.radians(5), 0, math.radians(-7))
    st.data.materials.append(mat("Tallo", hexcol(COLOR_TALLO), .85))
    bpy.ops.object.shade_smooth(); st.modifiers.new("Sub", 'SUBSURF').levels = 1

    lf = hoja()
    lf.location = (.07, -.07, suelo + .07)
    lf.rotation_euler = (math.radians(90), math.radians(-40), math.radians(12))
    lf.data.materials.append(mat("Hoja", hexcol(COLOR_HOJA), .50, .30))
    bpy.context.view_layer.objects.active = lf
    lf.select_set(True); bpy.ops.object.shade_smooth(); lf.select_set(False)
    sol = lf.modifiers.new("Grosor", 'SOLIDIFY'); sol.thickness = .022; sol.offset = 0
    lf.modifiers.new("Sub", 'SUBSURF').levels = 1

    if CARA:
        for sx in (-.27, .27):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12,
                                                 radius=.115, location=(sx, -.74, .10))
            e = bpy.context.object; e.name = "Ojo"; e.scale = (1.0, .55, 1.25)
            e.data.materials.append(mat("Ojo", hexcol("3A2320"), .30, .5))
            bpy.ops.object.shade_smooth()

    luz("Key",  LUZ_CLAVE,  (-2.8, -4.4, 3.8), 8)
    luz("Spec", LUZ_PUNTO,  (-1.5, -3.2, 3.4), 1.1)
    luz("Fill", 130,        ( 3.8, -3.0, 0.4), 9)
    luz("Rim",  LUZ_CONTRA, (-1.8,  3.2, 1.6), 5)

    cd = bpy.data.cameras.new("Cam"); cd.lens = 105
    cam = bpy.data.objects.new("Cam", cd)
    bpy.context.scene.collection.objects.link(cam)
    loc = (0.9, -8.6, 1.9); cam.location = loc
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector((0, 0, -.02)) - Vector(loc)).to_track_quat('-Z', 'Y')
    bpy.context.scene.camera = cam
    return ob

if __name__ == "__main__":
    construir()

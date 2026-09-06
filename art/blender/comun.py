"""Estudio comun de FrutiCity. Estilo Royal Match.

Aqui vive todo lo que NO es de una fruta concreta: las luces, la camara,
los materiales y las utilidades de malla. Cada ficha de fruta importa de
aqui y solo declara lo suyo.

El motivo de que esto no se copie por fruta: si cada archivo lleva sus
propias luces, en cuanto se retoca una la familia deja de casar y el
tablero se ve desparejo. La luz y el encuadre son de la familia, no de
la pieza.
"""
import bpy, bmesh, math, random
from mathutils import Vector, Euler, Matrix

# ============ EL ESTUDIO (comun a las 6) ============
LUZ_CLAVE, LUZ_PUNTO, LUZ_RELLENO, LUZ_CONTRA = 275, 330, 80, 190
CAM_LOC, CAM_LENTE = (0.9, -8.6, 1.9), 105
BRILLO_NITIDO = 0.10          # bajo = highlight definido, el barniz de RM
CAJA = 1.90                   # ancho/alto util: mas grande y se sale del tile
MARGEN = 0.12                 # aire alrededor de la pieza dentro del tile

# paleta de las piezas especiales. Sale de FruitModels.cs: si aqui se
# inventan otros colores, el arte 3D y el arte por codigo dejan de casar.
ORO, ORO_CLARO, CREMA, CORAL = "EFA218", "FFD24A", "FFF9EB", "ED7966"
MADERA, MADERA_OSCURA, MADERA_CLARA = "B0763A", "82522A", "D8A85E"
# ====================================================


_CREADOS = []      # lo que lleva construido la pieza actual


def _nace(ob):
    """Apunta cada objeto segun se crea.

    No vale deducir la pieza mirando una coleccion: en `--background` los
    objetos que nacen de `bpy.ops` no caen en `scene.collection`, asi que
    medir por coleccion se dejaba fuera todos los granos de uva y el
    racimo salia midiendo 0.43. Llevar la cuenta funciona igual con UI y
    sin ella.
    """
    _CREADOS.append(ob)
    return ob


def _vivos():
    fuera = []
    for ob in _CREADOS:
        try:
            if ob.type in ('MESH', 'CURVE'): fuera.append(ob)
        except ReferenceError:
            pass                       # lo borro limpiar(): ya no cuenta
    if fuera:
        return fuera
    # red de seguridad: si una ficha creo objetos sin pasar por aqui,
    # mas vale medir de mas que devolver una pieza vacia
    return [o for o in bpy.data.objects if o.type in ('MESH', 'CURVE')]


def hexcol(h, a=1.0):
    h = h.lstrip("#")
    return tuple((int(h[i:i+2], 16) / 255.0) ** 2.2 for i in (0, 2, 4)) + (a,)


def limpiar():
    """Vacia la escena. Borra tambien luces y camaras: si no, cada recarga
    en vivo deja datablocks huerfanos y el archivo engorda sin parar."""
    for o in list(bpy.data.objects):   bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):    bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    for l in list(bpy.data.lights):    bpy.data.lights.remove(l)
    for c in list(bpy.data.cameras):   bpy.data.cameras.remove(c)


def mat(nombre, rgba, rugosidad, barniz=0.0):
    m = bpy.data.materials.new(nombre); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba
    b.inputs["Roughness"].default_value = rugosidad
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = barniz
        b.inputs["Coat Roughness"].default_value = BRILLO_NITIDO
    return m


def poro(m, escala=110.0, fuerza=0.12, detalle=2.0):
    """Piel picada (naranja, corteza de kiwi). Va por bump, no por
    geometria: a 128 px el relieve real no se ve y si cuesta vertices."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    ruido = nt.nodes.new("ShaderNodeTexNoise")
    ruido.inputs["Scale"].default_value = escala
    ruido.inputs["Detail"].default_value = detalle
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = fuerza
    nt.links.new(ruido.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def hoyitos(ob, puntos, radio, hondo):
    """Hunde la malla alrededor de cada punto.

    Las pepitas de una fresa van METIDAS en un hoyo, no pegadas encima.
    Es lo que mas delata a una fresa de juguete: con las pepitas sobre la
    piel parecen granitos, y el ojo lo nota aunque no sepa por que.
    """
    me = ob.data
    Mi = ob.matrix_world.inverted()
    locales = [Mi @ Vector(p) for p in puntos]
    normales = [v.normal.copy() for v in me.vertices]   # antes de tocar nada
    r2 = radio * radio
    for i, v in enumerate(me.vertices):
        mejor = 0.0
        for p in locales:
            d2 = (v.co - p).length_squared
            if d2 < r2:
                k = 1.0 - math.sqrt(d2) / radio
                if k > mejor: mejor = k
        if mejor > 0.0:
            v.co -= normales[i] * (hondo * (mejor ** 1.4))
    me.update()
    return ob


def carne(m, peso=0.16, radio=(0.34, 0.12, 0.08)):
    """Deja pasar algo de luz por dentro. Sin esto una fruta es pintura
    sobre plastico: el rojo se queda en la superficie y no respira."""
    b = m.node_tree.nodes["Principled BSDF"]
    if "Subsurface Weight" in b.inputs:
        b.inputs["Subsurface Weight"].default_value = peso
        try: b.inputs["Subsurface Radius"].default_value = radio
        except Exception: pass
    return m


def degradado(m, color_a, color_b, eje=2, desde=-1.0, hasta=1.0):
    """Mezcla dos colores a lo largo de un eje del objeto (0=X, 1=Y, 2=Z).
    Un solo color plano es lo que hace que la pieza parezca de plastico;
    con dos tonos, el volumen se lee sin depender del brillo."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mapa = nt.nodes.new("ShaderNodeMapRange")
    mapa.inputs["From Min"].default_value = desde
    mapa.inputs["From Max"].default_value = hasta
    rampa = nt.nodes.new("ShaderNodeValToRGB")     # estable entre versiones
    rampa.color_ramp.elements[0].color = color_a
    rampa.color_ramp.elements[1].color = color_b
    nt.links.new(coord.outputs["Object"], sep.inputs["Vector"])
    nt.links.new(sep.outputs[eje], mapa.inputs["Value"])
    nt.links.new(mapa.outputs["Result"], rampa.inputs["Fac"])
    nt.links.new(rampa.outputs["Color"], b.inputs["Base Color"])
    return m


def revolucion(pts, ancho=1.0, seg=64, nombre="Cuerpo",
               lobulos=0, lobulo_fuerza=0.0, lobulo_fase=0.0, lobulo_hasta=0.45):
    """Barre un perfil (r, z) alrededor del eje Z. Los lobulos son
    opcionales: dan los surcos suaves de manzana y naranja."""
    bm = bmesh.new(); prev = None
    for r, z in pts:
        v = bm.verts.new((r * ancho, 0.0, z))
        if prev is not None: bm.edges.new((prev, v))
        prev = v
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    bmesh.ops.spin(bm, geom=list(bm.verts) + list(bm.edges), angle=math.radians(360),
                   steps=seg, axis=(0, 0, 1), cent=(0, 0, 0), use_merge=False)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    if lobulos:
        for v in bm.verts:
            x, y, z = v.co
            r = math.hypot(x, y)
            if r < 1e-5: continue
            t = max(0.0, min(1.0, (lobulo_hasta - z) / 1.2))
            ang = math.atan2(y, x) + math.radians(lobulo_fase)
            k = 1.0 + lobulo_fuerza * (t ** 1.5) * math.cos(lobulos * ang)
            v.co.x, v.co.y = x * k, y * k
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nombre); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    return _nace(ob)


def suave(ob, niveles=2):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_smooth()
    ob.select_set(False)
    if niveles:
        s = ob.modifiers.new("Sub", 'SUBSURF'); s.levels = niveles; s.render_levels = niveles
    return ob


def suave_auto(ob, angulo=40.0):
    """Suaviza solo donde la curvatura lo pide. En un cilindro, suave() a
    secas redondea tambien el borde de la tapa y la pieza pierde el canto."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    try:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(angulo))
    except Exception:
        bpy.ops.object.shade_smooth()
    ob.select_set(False)
    return ob


def esfera(nombre, radio, loc, escala=(1, 1, 1), seg=24, anillos=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=anillos,
                                         radius=radio, location=loc)
    ob = bpy.context.object; ob.name = nombre; ob.scale = escala
    return _nace(ob)


def bisel(ob, ancho=.035, seg=2, angulo=32.0):
    """En Royal Match no existe la arista viva: todo tiene el canto
    redondeado. Es lo que separa una pieza de juego de un cubo de Blender."""
    b = ob.modifiers.new("Bisel", 'BEVEL')
    b.width = ancho; b.segments = seg
    b.limit_method = 'ANGLE'; b.angle_limit = math.radians(angulo)
    b.miter_outer = 'MITER_ARC'
    return ob


def aplicar_escala(ob):
    """El bisel trabaja en espacio local: sin aplicar la escala, una caja
    achatada sale con el canto ovalado."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.select_set(False)
    return ob


def prisma(pts, grosor, nombre="Prisma", canto=.035, seg=2):
    """Extruye un contorno 2D (lista de (x, y)) a lo largo de Z."""
    bm = bmesh.new()
    h = grosor / 2.0
    abajo = [bm.verts.new((x, y, -h)) for x, y in pts]
    arriba = [bm.verts.new((x, y, h)) for x, y in pts]
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((abajo[i], abajo[j], arriba[j], arriba[i]))
    bm.faces.new(list(reversed(abajo)))
    bm.faces.new(arriba)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nombre); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    if canto: bisel(ob, canto, seg)
    return _nace(ob)


def estrella(puntas=5, fuera=1.0, dentro=.44, giro=90.0):
    """Contorno de estrella, listo para prisma(). giro=90 deja una punta
    arriba, que es como se lee una estrella."""
    pts = []
    for i in range(puntas * 2):
        a = math.pi * i / puntas + math.radians(giro)
        r = fuera if i % 2 == 0 else dentro
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def caja(nombre, dims, loc=(0, 0, 0), rot=(0, 0, 0), canto=.045, seg=2):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.object; ob.name = nombre
    ob.scale = dims
    aplicar_escala(ob)
    ob.rotation_euler = tuple(math.radians(a) for a in rot)
    if canto: bisel(ob, canto, seg)
    return _nace(ob)


def cilindro(nombre, radio, alto, loc=(0, 0, 0), rot=(0, 0, 0), caras=28, canto=.04):
    bpy.ops.mesh.primitive_cylinder_add(vertices=caras, radius=radio, depth=alto,
                                        location=loc)
    ob = bpy.context.object; ob.name = nombre
    ob.rotation_euler = tuple(math.radians(a) for a in rot)
    suave_auto(ob)
    if canto: bisel(ob, canto, 2)
    return _nace(ob)


def cono(nombre, r1, r2, alto, loc=(0, 0, 0), rot=(0, 0, 0), caras=24, canto=.03):
    bpy.ops.mesh.primitive_cone_add(vertices=caras, radius1=r1, radius2=r2,
                                    depth=alto, location=loc)
    ob = bpy.context.object; ob.name = nombre
    ob.rotation_euler = tuple(math.radians(a) for a in rot)
    suave_auto(ob)
    if canto: bisel(ob, canto, 2)
    return _nace(ob)


def cuerda(nombre, puntos, radio, resolucion=4):
    """Un tubo que sigue una lista de puntos. Para la mecha de la bomba:
    hacerlo con malla a mano no compensa, una curva con grosor basta."""
    cu = bpy.data.curves.new(nombre, 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('POLY'); sp.points.add(len(puntos) - 1)
    for i, p in enumerate(puntos):
        sp.points[i].co = (p[0], p[1], p[2], 1.0)
    cu.bevel_depth = radio; cu.bevel_resolution = resolucion; cu.resolution_u = 6
    ob = bpy.data.objects.new(nombre, cu)
    bpy.context.scene.collection.objects.link(ob)
    return _nace(ob)


def hoja(largo=.58, ancho=.125, nervio=.032, curva=.12, nombre="Hoja"):
    """ancho = SEMIancho. Relacion ~2.3:1 largo/ancho para que lea a hoja."""
    N, bm = 14, bmesh.new()
    filas = []
    for i in range(N + 1):
        t = i / N
        w = ancho * math.sin(math.pi * t) ** 0.62      # puntiaguda en t=0 y t=1
        alza = curva * (t ** 1.6)                      # se dobla hacia la punta
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
    me = bpy.data.meshes.new(nombre); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    return _nace(ob)


def hoja_puesta(material, loc, rot, largo=.58, ancho=.125, grosor=.022, nombre="Hoja"):
    """La hoja entera: malla, material, suavizado y grosor. Es lo que se
    repite tal cual en manzana, naranja, fresa y uvas."""
    lf = hoja(largo, ancho, nombre=nombre)
    lf.location = loc
    lf.rotation_euler = tuple(math.radians(a) for a in rot)
    lf.data.materials.append(material)
    suave(lf, 0)
    sol = lf.modifiers.new("Grosor", 'SOLIDIFY'); sol.thickness = grosor; sol.offset = 0
    lf.modifiers.new("Sub", 'SUBSURF').levels = 1
    return lf


def tallo(material, loc, rot=(0, 0, 0), r_base=.095, r_punta=.080, alto=.30,
          nombre="Rabito", caras=16):
    bpy.ops.mesh.primitive_cone_add(vertices=caras, radius1=r_base, radius2=r_punta,
                                    depth=alto, location=loc)
    st = bpy.context.object; st.name = nombre
    st.rotation_euler = tuple(math.radians(a) for a in rot)
    st.data.materials.append(material)
    suave(st, 1)
    return _nace(st)


def girar(objetos, euler_grados):
    """Rota un grupo entero alrededor del origen. Para piezas que se montan
    comodas en local (el kiwi en corte) y luego hay que encarar a camara."""
    bpy.context.view_layer.update()     # si no, matrix_world va un paso atras
    R = Euler(tuple(math.radians(a) for a in euler_grados), 'XYZ').to_matrix().to_4x4()
    for ob in objetos:
        ob.matrix_world = R @ ob.matrix_world
    return objetos


def _luz(nombre, energia, loc, tam):
    d = bpy.data.lights.new(nombre, 'AREA'); d.energy = energia; d.size = tam
    o = bpy.data.objects.new(nombre, d); o.location = loc
    bpy.context.scene.collection.objects.link(o)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat('-Z', 'Y')
    return o


def luces():
    _luz("Key",  LUZ_CLAVE,   (-2.8, -4.4, 3.8), 8)
    _luz("Spec", LUZ_PUNTO,   (-1.5, -3.2, 3.4), 1.1)
    _luz("Fill", LUZ_RELLENO, ( 3.8, -3.0, 0.4), 9)
    _luz("Rim",  LUZ_CONTRA,  (-1.8,  3.2, 1.6), 5)


def camara(mirar=(0, 0, -.02), tamano=None):
    """mirar = el punto al que apunta. tamano = cuanto mide la pieza en su
    lado largo; si se pasa, la lente se calcula para que llene el tile.

    Apuntar siempre al origen partia las piezas altas (la corona de la
    fresa se salia por arriba) y dejaba la mitad del tile vacio en las
    bajas. Encuadrando sobre el centro real, las trece llenan igual."""
    cd = bpy.data.cameras.new("Cam"); cd.lens = CAM_LENTE
    cam = bpy.data.objects.new("Cam", cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = CAM_LOC
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector(mirar) - Vector(CAM_LOC)).to_track_quat('-Z', 'Y')
    if tamano:
        d = (Vector(mirar) - Vector(CAM_LOC)).length
        cd.lens = d * cd.sensor_width / (tamano * (1.0 + MARGEN))
    bpy.context.scene.camera = cam
    return cam


def _extremos(obs):
    """Caja y centro reales, con los modificadores YA aplicados.

    Se miden los VERTICES de la malla evaluada, no el `bound_box`. El
    bound_box de un objeto de curva (la mecha de la bomba) viene inflado:
    daba 2.46 de alto para una mecha de 0.57, y `encajar` encogia la
    bomba a la cuarta parte sin que nada diese error.
    """
    dg = bpy.context.evaluated_depsgraph_get()
    xs, ys, zs = [], [], []
    fuente = obs if obs else _vivos()
    for ob in fuente:
        M = ob.matrix_world
        try:
            ev = ob.evaluated_get(dg)
            malla = ev.to_mesh()
        except Exception:
            ev, malla = ob, None
        if malla is not None and len(malla.vertices):
            for v in malla.vertices:
                w = M @ v.co
                xs.append(w.x); ys.append(w.y); zs.append(w.z)
            ev.to_mesh_clear()
        else:
            for c in ob.bound_box:
                w = M @ Vector(c)
                xs.append(w.x); ys.append(w.y); zs.append(w.z)
    if not xs: return None, None
    caja = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    centro = ((max(xs) + min(xs)) / 2.0,
              (max(ys) + min(ys)) / 2.0,
              (max(zs) + min(zs)) / 2.0)
    return caja, centro


def medir(*obs):
    """Medir antes de tocar. Imprime la caja real que ocupa la pieza, para
    poder comparar piezas entre si en vez de ajustar a ojo."""
    bpy.context.view_layer.update()
    caja_, _ = _extremos(obs)
    if not caja_: return None
    print("[medida] ancho %.2f  fondo %.2f  alto %.2f   (util <= %.2f)"
          % (caja_ + (CAJA,)))
    return caja_


def encajar(objetos, caja=None, alrededor_de=None):
    """Escala el grupo para que quepa justo en la caja del tile.
    Es lo que iguala de verdad el tamano aparente entre frutas: una pieza
    alargada (el platano) y una redonda (la naranja) no se igualan con el
    mismo numero de mandos, se igualan midiendo."""
    caja = CAJA if caja is None else caja
    bpy.context.view_layer.update()
    m, _ = _extremos(alrededor_de or objetos)
    if not m: return 1.0
    k = caja / max(m[0], m[2])          # ancho y alto: el fondo da igual
    S = Matrix.Scale(k, 4)
    for ob in objetos:
        ob.matrix_world = S @ ob.matrix_world
    print("[encaje] escalado x%.3f" % k)
    return k


def empezar():
    limpiar()
    del _CREADOS[:]
    random.seed(7)          # el desorden de las uvas tiene que salir igual siempre


def terminar(*principales):
    luces()
    bpy.context.view_layer.update()
    caja_, centro = _extremos(principales)
    if caja_:
        print("[medida] ancho %.2f  fondo %.2f  alto %.2f   (util <= %.2f)"
              % (caja_ + (CAJA,)))
        camara(centro, max(caja_[0], caja_[2]))
    else:
        camara()
    return caja_

"""Fresita segun la hoja de personaje (art/fresita-character-sheet.png).

Diferencia clave con personaje_fresita.py: alli el cuerpo ENTERO era una
fresa. En la hoja la fresa es solo la CABEZA, y debajo hay un cuerpo
humanoide chibi con top rosa, pantalon corto rosa y zapatillas.

Proporciones medidas sobre el panel "FRENTE" de la hoja (altura total 1.60,
plantas de los pies en z=0):

    suela            0.00      rodilla          0.24
    tobillo          0.11      bajo del short   0.38
    cadera ancha     0.44      cintura          0.50
    pecho            0.66      hombros          0.79
    barbilla         0.83      centro cabeza    1.16
    cima cabeza      1.50      punta de hoja    1.62

La cabeza mide 0.67 de alto sobre 1.60: el 42%. Es mucho, y es a proposito:
en la hoja la cabeza es mas ancha que los hombros. Si se "arregla" a
proporciones humanas deja de parecerse al dibujo.

Uso:
    blender --background --python fresita_sheet.py                 # construye + render
    blender --background --python fresita_sheet.py -- solo-blend   # sin render
"""
import bpy, bmesh, math, sys, os, random
from pathlib import Path
from mathutils import Vector, Matrix, Euler

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import comun as c

OUT = HERE / 'fresita_v5'
OUT.mkdir(exist_ok=True)

# --- paleta sacada del muestrario de la hoja ----------------------------
SKIN      = "D8392F"   # rojo fresa
SKIN_DK   = "A82018"
SEED      = "E9B54A"
LEAF      = "8CBB5C"
LEAF_DK   = "6B9B43"
TOP       = "F5A2C0"   # top rosa
SHORT     = "F192B6"   # short rosa
TRIM      = "FFFFFF"
SHOE      = "F3A8C6"
SOLE      = "FFFFFF"

# --- alturas (z) --------------------------------------------------------
Z_SUELA, Z_TOBILLO, Z_RODILLA = 0.00, 0.115, 0.24
Z_SHORT_BAJO, Z_CADERA, Z_CINTURA = 0.38, 0.44, 0.50
Z_PECHO, Z_HOMBRO, Z_CUELLO = 0.66, 0.79, 0.84
Z_BARBILLA, Z_CABEZA, Z_CIMA = 0.83, 1.16, 1.50
X_PIERNA, X_HOMBRO = 0.105, 0.158
R_CABEZA = 0.34

MATS = {}


def log(m):
    print(m, flush=True)


# ============ utilidades de forma =======================================

def capsula(nombre, a, b, r1, r2, mat, seg=20):
    """Tronco de cono con las dos tapas redondeadas, tendido de a hasta b.

    Los brazos y piernas de la hoja no son bolas apiladas: son un solo
    volumen que se estrecha. Con esferas sueltas se ven los escalones en
    la silueta, que es justo lo que delata a un monigote de Blender.
    """
    a, b = Vector(a), Vector(b)
    d = b - a
    L = d.length
    pts = []
    N = 6
    for i in range(N + 1):                      # tapa de abajo
        t = math.pi / 2 * i / N
        pts.append((r1 * math.sin(t), -r1 * math.cos(t)))
    pts.append((r2, L))                         # cuerpo
    for i in range(1, N + 1):                   # tapa de arriba
        t = math.pi / 2 * i / N
        pts.append((r2 * math.cos(t), L + r2 * math.sin(t)))
    ob = c.revolucion(pts, seg=seg, nombre=nombre)
    ob.data.materials.append(mat)
    c.suave(ob, 1)
    ob.location = a
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = d.to_track_quat('Z', 'Y')
    return ob


def elipsoide(nombre, loc, escala, mat, seg=24, anillos=14, suavizado=1):
    o = c.esfera(nombre, 1.0, loc, escala, seg, anillos)
    o.data.materials.append(mat)
    c.suave(o, suavizado)
    return o


def pepitas(ob, n, z_min, z_max, evitar_cara=None, radio=.020, seed=11):
    """Siembra pepitas doradas sobre la superficie de ob, metidas en su
    hoyo. evitar_cara = (z0, z1, medio_angulo) para dejar limpia la cara."""
    rnd = random.Random(seed)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    inv = ob.matrix_world.inverted()
    puestas = []
    intentos = 0
    while len(puestas) < n and intentos < n * 12:
        intentos += 1
        z = rnd.uniform(z_min, z_max)
        ang = math.radians(rnd.uniform(0, 360))
        if evitar_cara:
            z0, z1, medio = evitar_cara
            # la cara mira a -Y: angulo -90 grados
            da = abs((math.degrees(ang) + 90) % 360)
            da = min(da, 360 - da)
            if z0 < z < z1 and da < medio:
                continue
        origen = Vector((3 * math.cos(ang), 3 * math.sin(ang), z))
        dirn = Vector((-math.cos(ang), -math.sin(ang), 0))
        hit = ev.ray_cast(inv @ origen, inv.to_3x3() @ dirn)
        if not hit[0]:
            continue
        p = ob.matrix_world @ hit[1]
        n_ = (ob.matrix_world.to_3x3() @ hit[2]).normalized()
        if any((p - q).length < radio * 4.2 for q in puestas):
            continue
        puestas.append(p)
        # lenteja tumbada, no pincho: aplastada contra la piel y alargada
        # en la vertical de la superficie (Y local sale de to_track_quat).
        s = elipsoide("Pepita", p - n_ * .002,
                      (radio * .78, radio * 1.25, radio * .42),
                      MATS['seed'], 12, 8, 0)
        s.rotation_mode = 'QUATERNION'
        s.rotation_quaternion = n_.to_track_quat('Z', 'Y')
    if puestas:
        c.hoyitos(ob, puestas, radio * 2.6, radio * .38)
    return len(puestas)


# ============ materiales ================================================

def materiales():
    m = {}
    m['skin'] = c.mat("Piel", c.hexcol(SKIN), .40, .30)
    c.degradado(m['skin'], c.hexcol(SKIN_DK), c.hexcol(SKIN), eje=2, desde=-0.1, hasta=1.5)
    c.carne(m['skin'], .14, (0.35, 0.10, 0.07))
    m['skin_liso'] = c.mat("PielLisa", c.hexcol(SKIN), .40, .30)
    c.carne(m['skin_liso'], .14, (0.35, 0.10, 0.07))
    m['seed']   = c.mat("Pepita", c.hexcol(SEED), .38, .20)
    m['leaf']   = c.mat("Hoja",   c.hexcol(LEAF), .46, .10)
    c.degradado(m['leaf'], c.hexcol(LEAF_DK), c.hexcol(LEAF), eje=0, desde=0.0, hasta=0.30)
    m['top']    = c.mat("Top",    c.hexcol(TOP),   .68, .02)
    m['short']  = c.mat("Short",  c.hexcol(SHORT), .68, .02)
    m['trim']   = c.mat("Ribete", c.hexcol(TRIM),  .60, .02)
    m['shoe']   = c.mat("Zapa",   c.hexcol(SHOE),  .52, .12)
    m['sole']   = c.mat("Suela",  c.hexcol(SOLE),  .55, .06)
    MATS.clear(); MATS.update(m)
    return m


# ============ cabeza ====================================================

PERFIL_CABEZA = [(0.000, Z_BARBILLA),
                 (0.075, 0.845), (0.155, 0.885), (0.240, 0.950),
                 (0.298, 1.030), (0.330, 1.120), (0.340, 1.210),
                 (0.322, 1.300), (0.268, 1.380), (0.190, 1.442),
                 (0.095, 1.482), (0.000, Z_CIMA)]
CARA_Z0, CARA_Z1, CARA_PLANO = 0.93, 1.36, 0.20


def _radio_cabeza(z):
    for (r0, z0), (r1, z1) in zip(PERFIL_CABEZA, PERFIL_CABEZA[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / max(1e-6, z1 - z0)
            return r0 + (r1 - r0) * t
    return 0.0


def _aplanado(y, r, z):
    """Cuanto se hunde hacia atras un punto del frente. La cara de la hoja
    no es un casquete de esfera: es un frente ligeramente aplastado, y sin
    eso los ojos grandes no caben sin salirse por el lateral."""
    if y >= 0 or r < 1e-6:
        return 0.0
    frontal = min(1.0, -y / r)
    zf = (min(1.0, max(0.0, (z - CARA_Z0) / 0.10))
          * min(1.0, max(0.0, (CARA_Z1 - z) / 0.10)))
    return CARA_PLANO * (frontal ** 2) * zf


def _y_cara(x, z):
    """La 'y' de la piel de la cara en (x, z). Todo lo que va en la cara se
    coloca contra esto; poner los ojos y la boca a una y fija los deja
    flotando delante del morro o enterrados, segun la altura."""
    r = _radio_cabeza(z)
    if r <= 1e-6 or abs(x) >= r:
        return 0.0
    y = -math.sqrt(r * r - x * x)
    return y * (1.0 - _aplanado(y, r, z))


def cabeza(semillas=34, curva=0.0, mat=None, lobulos=0, lobulo_fuerza=0.0):
    """La cabeza de la fruta, con el frente aplanado para que quepa la cara.

    `semillas` son las pepitas de la fresa (0 para las demas frutas) y
    `curva` desplaza en X segun la altura: es lo que dobla al platano sin
    tener que modelar otra malla.
    """
    h = c.revolucion(PERFIL_CABEZA, seg=64, nombre="Cabeza",
                     lobulos=lobulos, lobulo_fuerza=lobulo_fuerza,
                     lobulo_hasta=PERFIL_CABEZA[-1][1])
    h.data.materials.append(mat or MATS['skin'])
    z0, z1 = PERFIL_CABEZA[0][1], PERFIL_CABEZA[-1][1]
    zc, hh = (z0 + z1) / 2.0, (z1 - z0) / 2.0
    for v in h.data.vertices:
        r = math.hypot(v.co.x, v.co.y)
        v.co.y *= (1.0 - _aplanado(v.co.y, r, v.co.z))
        if curva:
            v.co.x += curva * ((v.co.z - zc) / hh) ** 2
    h.data.update()
    c.suave(h, 2)
    n = 0
    if semillas:
        n = pepitas(h, semillas, 0.90, 1.42, evitar_cara=(0.96, 1.34, 66),
                    radio=.016, seed=11)
    log("  cabeza: %.2f de ancho, %d pepitas" % (2 * max(r for r, _ in PERFIL_CABEZA), n))
    return h


def corona():
    """Calice verde: hojas caidas hacia delante, como un flequillo."""
    hojas = []
    N = 9
    for k in range(N):
        ang = 360.0 / N * k - 90.0
        # las de delante caen mas (hacen de flequillo), las de atras se abren
        da = abs(((ang + 90) % 360 + 180) % 360 - 180)
        caida = 78 - 30 * (da / 180.0)
        largo = .34 - .05 * (da / 180.0)
        lf = c.hoja_puesta(MATS['leaf'], (0, 0, 1.432), (caida, -8, ang),
                           largo=largo, ancho=.098, grosor=.016, nombre="Hoja")
        hojas.append(lf)
    # segunda corona mas corta y mas erguida: da espesor al flequillo
    for k in range(5):
        ang = 360.0 / 5 * k - 54.0
        lf = c.hoja_puesta(MATS['leaf'], (0, 0, 1.478), (46, -6, ang),
                           largo=.20, ancho=.070, grosor=.014, nombre="HojaAlta")
        hojas.append(lf)
    t = c.tallo(MATS['leaf'], (0, .01, 1.545), rot=(6, 0, 0),
                r_base=.030, r_punta=.020, alto=.13, caras=12, nombre="Rabito")
    log("  corona: %d hojas + rabito" % len(hojas))
    return hojas + [t]


EXPRESION = "idle"
CARA_YAW = 55.0             # medio angulo que abarca el calco
CARA_ZA, CARA_ZB = 0.95, 1.34
CARAS = HERE / 'fresita_v5' / 'caras'


def nariz():
    """Lo unico de la cara que sigue siendo volumen. Un boton de 3 cm que
    rompe la planitud del calco sin pelearse con el dibujo."""
    return elipsoide("Nariz", (0, _y_cara(0, 1.078) - .012, 1.078),
                     (.030, .026, .024), MATS['skin_liso'], 18, 12, 1)


def _punto_cara(yaw, z, fuera=0.005):
    """Un punto de la piel de la cara a un angulo y una altura, separado
    `fuera` hacia delante. Mismo aplanado que la malla de la cabeza."""
    r = _radio_cabeza(z)
    x = r * math.sin(yaw)
    y = -r * math.cos(yaw)
    y *= (1.0 - _aplanado(y, r, z))
    n = Vector((x, y, 0.0))
    n = n.normalized() if n.length > 1e-6 else Vector((0, -1, 0))
    return Vector((x, y, z)) - n * fuera


def _mat_cara(ruta):
    m = bpy.data.materials.new("CaraSprite")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.62
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = 0.22
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.name = tex.label = "CaraTex"
    img = bpy.data.images.load(str(ruta), check_existing=True)
    img.alpha_mode = 'STRAIGHT'
    tex.image = img
    tex.interpolation = 'Cubic'
    tex.extension = 'CLIP'
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
    # el nombre de estos ajustes cambia entre versiones de EEVEE
    for attr, val in (("blend_method", 'BLEND'), ("shadow_method", 'NONE'),
                      ("surface_render_method", 'BLENDED')):
        try:
            setattr(m, attr, val)
        except Exception:
            pass
    return m


def cara_sprite(cabeza_ob, expresion=None, nu=48, nv=48, fuera=0.006):
    """Un calco curvo con la cara dibujada encima.

    Cada vertice se coloca lanzando un rayo contra la cabeza YA evaluada
    (con su subsurf) y separandolo `fuera` por la normal. Calcular la
    superficie con la formula del perfil no vale: el subsurf mueve la piel
    unos milimetros y el calco se queda por DENTRO. Medido: las cejas
    entraban 7 mm y la boca 4, y por eso solo se veian los ojos, que
    asomaban por la cuenca.
    """
    expresion = expresion or EXPRESION
    ruta = CARAS / ("cara_%s.png" % expresion)
    if not ruta.exists():
        raise FileNotFoundError("falta %s - corre antes caras_fresita.py" % ruta)

    dg = bpy.context.evaluated_depsgraph_get()
    ev = cabeza_ob.evaluated_get(dg)
    M = cabeza_ob.matrix_world
    inv = M.inverted()

    def sobre_piel(yaw, z):
        d = Vector((math.sin(yaw), -math.cos(yaw), 0.0))
        hit = ev.ray_cast(inv @ Vector((3 * d.x, 3 * d.y, z)),
                          inv.to_3x3() @ (-d))
        if not hit[0]:
            return _punto_cara(yaw, z, fuera)
        p = M @ hit[1]
        n = (M.to_3x3() @ hit[2]).normalized()
        return p + n * fuera

    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new("UVMap")
    rej = []
    for j in range(nv + 1):
        v = j / nv
        z = CARA_ZA + (CARA_ZB - CARA_ZA) * v
        rej.append([sobre_piel(
            math.radians(-CARA_YAW + 2 * CARA_YAW * (i / nu)), z)
            for i in range(nu + 1)])
        rej[-1] = [bm.verts.new(q) for q in rej[-1]]
    bm.verts.ensure_lookup_table()
    for j in range(nv):
        for i in range(nu):
            f = bm.faces.new((rej[j][i], rej[j][i + 1],
                              rej[j + 1][i + 1], rej[j + 1][i]))
            uvs = ((i / nu, j / nv), ((i + 1) / nu, j / nv),
                   ((i + 1) / nu, (j + 1) / nv), (i / nu, (j + 1) / nv))
            for lo, uv in zip(f.loops, uvs):
                lo[uvl].uv = uv
    bm.faces.ensure_lookup_table()
    if bm.faces[0].normal.y > 0:       # que mire hacia fuera, a -Y
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    me = bpy.data.meshes.new("Cara"); bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new("Cara", me)
    bpy.context.scene.collection.objects.link(ob)
    c._nace(ob)
    ob.data.materials.append(_mat_cara(ruta))
    c.suave(ob, 0)
    ob.visible_shadow = False        # un calco no proyecta sombra sobre la piel
    log("  cara: calco '%s' (%dx%d) sobre la piel" % (expresion, nu, nv))
    return ob


def poner_cara(expresion):
    """Cambia la expresion en caliente: solo cambia la imagen del nodo."""
    ob = bpy.data.objects.get("Cara")
    if ob is None:
        return None
    ruta = CARAS / ("cara_%s.png" % expresion)
    tex = ob.data.materials[0].node_tree.nodes.get("CaraTex")
    tex.image = bpy.data.images.load(str(ruta), check_existing=True)
    tex.image.alpha_mode = 'STRAIGHT'
    return ob


# ============ cuerpo ====================================================

# Perfil (radio, z) del tronco. La ropa se saca de este mismo perfil
# desplazado hacia fuera, que es lo unico que hace que ciña de verdad:
# una cascara con radio constante sale como una tabla pegada al pecho.
PERFIL_TORSO = [(0.000, 0.318),
                (0.104, 0.334), (0.168, 0.372), (0.196, 0.412),
                (0.205, Z_CADERA), (0.174, 0.478), (0.149, Z_CINTURA),
                (0.158, 0.560), (0.178, 0.612), (0.187, Z_PECHO),
                (0.181, 0.722), (0.166, Z_HOMBRO), (0.130, 0.812),
                (0.082, Z_CUELLO), (0.072, 0.880)]
APLASTA_Y = 0.86      # el torso es mas ancho que hondo, pero no una tabla


def _radio_torso(z):
    """Interpola el radio del tronco a una altura dada."""
    for (r0, z0), (r1, z1) in zip(PERFIL_TORSO, PERFIL_TORSO[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / max(1e-6, z1 - z0)
            return r0 + (r1 - r0) * t
    return PERFIL_TORSO[-1][0]


def _cascara(nombre, z0, z1, holgura, mat, grosor, pasos=7, escote=0.0):
    """Cilindro que sigue el perfil del torso, separado `holgura`.

    `escote` baja el borde de arriba por delante y por detras dejandolo
    alto en los hombros. Sin eso la prenda se corta en horizontal y de
    frente se ve el canto y el hueco: parece una caja abierta, no ropa.
    """
    pts = [(_radio_torso(z0 + (z1 - z0) * i / pasos) + holgura,
            z0 + (z1 - z0) * i / pasos) for i in range(pasos + 1)]
    ob = c.revolucion(pts, seg=48, nombre=nombre)
    ob.data.materials.append(mat)
    for v in ob.data.vertices:
        v.co.y *= APLASTA_Y
    if escote:
        zmax = max(v.co.z for v in ob.data.vertices)
        for v in ob.data.vertices:
            if abs(v.co.z - zmax) < 1e-4:
                ang = math.atan2(v.co.y, v.co.x)     # 0 = costado
                v.co.z -= escote * (math.sin(ang) ** 2)
    ob.data.update()
    m = ob.modifiers.new("Grosor", 'SOLIDIFY'); m.thickness = grosor; m.offset = 1
    c.suave(ob, 2)
    return ob


def ribete_borde(cascara, mat, radio=.013, arriba=True):
    """Un cordon que recorre el borde real de la prenda y tapa el canto."""
    vs = [v.co.copy() for v in cascara.data.vertices]
    z_ref = max(v.z for v in vs) if arriba else min(v.z for v in vs)
    # el borde ya no es plano por el escote: se coge el vertice mas alto
    # (o mas bajo) de cada columna angular
    por_ang = {}
    for v in vs:
        k = round(math.degrees(math.atan2(v.y, v.x)) / 7.5)
        q = por_ang.get(k)
        if q is None or (v.z > q.z if arriba else v.z < q.z):
            por_ang[k] = v
    pts = [por_ang[k] for k in sorted(por_ang)]
    if len(pts) < 8:
        return None
    ob = c.cuerda(cascara.name + "Ribete", [(p.x, p.y, p.z) for p in pts], radio, 4)
    ob.data.splines[0].use_cyclic_u = True
    ob.data.materials.append(mat)
    return ob


def anillo(nombre, z, radio, grosor, mat, y=0.0, aplasta=1.0):
    """Ribete: un aro fino de verdad, no un disco. `aplasta` lo pone
    ovalado como el tronco; si no, el aro sobresale por delante."""
    bpy.ops.mesh.primitive_torus_add(major_radius=radio, minor_radius=grosor,
                                     major_segments=44, minor_segments=8,
                                     location=(0, y, z))
    ob = bpy.context.object; ob.name = nombre
    ob.scale = (1.0, aplasta, 1.0)
    ob.data.materials.append(mat)
    c.suave(ob, 0)
    return ob


def torso():
    t = c.revolucion(PERFIL_TORSO, seg=48, nombre="Torso")
    t.data.materials.append(MATS['skin'])
    for v in t.data.vertices:
        v.co.y *= APLASTA_Y
    t.data.update()
    c.suave(t, 2)
    return t


def brazos():
    obs = []
    for sgn, nom in ((-1, "L"), (1, "R")):
        # los brazos se abren un poco: pegados al costado no hay silueta y
        # la figura se lee como un bolo
        obs.append(elipsoide("Hombro%s" % nom, (X_HOMBRO * sgn, 0, 0.764),
                             (.078, .072, .080), MATS['skin_liso'], 20, 12, 1))
        obs.append(capsula("BrazoAlto%s" % nom,
                           (X_HOMBRO * sgn, 0, 0.770), (0.228 * sgn, .004, 0.608),
                           .069, .052, MATS['skin_liso']))
        obs.append(capsula("BrazoBajo%s" % nom,
                           (0.228 * sgn, .004, 0.618), (0.258 * sgn, .006, 0.472),
                           .054, .040, MATS['skin_liso']))
        mano = elipsoide("Mano%s" % nom, (0.263 * sgn, .006, 0.432),
                         (.046, .034, .058), MATS['skin_liso'], 20, 14, 1)
        obs.append(mano)
        for i in range(4):
            obs.append(capsula("Dedo%s%d" % (nom, i + 1),
                               (0.263 * sgn + (i - 1.5) * .022, .004, 0.396),
                               (0.263 * sgn + (i - 1.5) * .024, .006, 0.348),
                               .014, .011, MATS['skin_liso'], 10))
        obs.append(capsula("Pulgar%s" % nom,
                           (0.237 * sgn, -.014, 0.424), (0.207 * sgn, -.030, 0.398),
                           .015, .012, MATS['skin_liso'], 10))
    return obs


def piernas():
    obs = []
    for sgn, nom in ((-1, "L"), (1, "R")):
        obs.append(capsula("Muslo%s" % nom,
                           (X_PIERNA * sgn, 0, 0.435), (0.118 * sgn, 0, Z_RODILLA),
                           .107, .076, MATS['skin_liso']))
        obs.append(capsula("Gemelo%s" % nom,
                           (0.118 * sgn, 0, 0.252), (0.122 * sgn, -.004, Z_TOBILLO),
                           .082, .046, MATS['skin_liso']))
    return obs


def zapatillas():
    obs = []
    # Zapatilla chunky de la hoja: caña baja rosa, suela blanca gorda y
    # puntera redonda. En el render anterior salian de juguete de playmobil
    # porque eran mas estrechas que el tobillo.
    for sgn, nom in ((-1, "L"), (1, "R")):
        z = c.caja("Zapa%s" % nom, (.152, .270, .120),
                   (0.124 * sgn, -.038, 0.108), canto=.052, seg=4)
        z.data.materials.append(MATS['shoe'])
        c.suave_auto(z, 46)
        obs.append(z)
        s = c.caja("Suela%s" % nom, (.166, .292, .062),
                   (0.124 * sgn, -.038, 0.031), canto=.028, seg=4)
        s.data.materials.append(MATS['sole'])
        c.suave_auto(s, 46)
        obs.append(s)
        # puntera y talon en blanco, pequeños: si se comen media zapatilla
        # la pieza deja de leerse rosa
        p = elipsoide("Puntera%s" % nom, (0.124 * sgn, -.152, 0.072),
                      (.062, .036, .034), MATS['sole'], 20, 14, 1)
        obs.append(p)
        tl = elipsoide("Talon%s" % nom, (0.124 * sgn, .090, 0.112),
                       (.056, .026, .044), MATS['sole'], 20, 14, 1)
        obs.append(tl)
        for i in range(3):
            cd = capsula("Cordon%s%d" % (nom, i),
                         (0.124 * sgn - .044, -.098 + i * .036, 0.164),
                         (0.124 * sgn + .044, -.098 + i * .036, 0.164),
                         .009, .009, MATS['sole'], 8)
            obs.append(cd)
    return obs


def ropa():
    """Top corto y short: cascaras que siguen el perfil del tronco."""
    obs = []
    # top: del pecho al borde de debajo del busto
    top = _cascara("Top", 0.590, 0.756, .015, MATS['top'], .014, escote=.034)
    obs.append(top)
    obs.append(ribete_borde(top, MATS['top'], .014, arriba=True))
    obs.append(ribete_borde(top, MATS['top'], .013, arriba=False))
    # tirantes: por encima del hombro, uno delante y otro detras
    for sgn, nom in ((-1, "L"), (1, "R")):
        tr = capsula("Tirante%s" % nom,
                     (0.112 * sgn, -.100, 0.746), (0.124 * sgn, .078, 0.760),
                     .019, .019, MATS['top'], 10)
        obs.append(tr)
    # busto y gluteo. La hoja los tiene bien marcados en el panel LADO;
    # una cascara de revolucion sola deja el perfil como una tabla.
    for sgn, nom in ((-1, "L"), (1, "R")):
        obs.append(elipsoide("Busto%s" % nom, (0.062 * sgn, -.155, 0.645),
                             (.098, .046, .050), MATS['top'], 22, 14, 1))
    # short: de la cintura al medio muslo
    sh = _cascara("Short", Z_SHORT_BAJO, 0.502, .017, MATS['short'], .016)
    obs.append(sh)
    obs.append(anillo("ShortCinturilla", 0.496, _radio_torso(0.496) + .022,
                      .011, MATS['trim'], aplasta=APLASTA_Y))
    # perneras: tubo corto y ceñido al muslo, con su vivo blanco en el borde
    for sgn, nom in ((-1, "L"), (1, "R")):
        pn = capsula("Pernera%s" % nom,
                     (0.104 * sgn, 0, 0.432), (0.112 * sgn, 0, 0.358),
                     .112, .100, MATS['short'], 28)
        pn.scale = (1, .92, 1)
        obs.append(pn)
        bpy.ops.mesh.primitive_torus_add(major_radius=.096, minor_radius=.009,
                                         major_segments=32, minor_segments=8,
                                         location=(0.112 * sgn, 0, 0.360))
        rb = bpy.context.object; rb.name = "PerneraRibete%s" % nom
        rb.scale = (1, .92, 1)
        rb.data.materials.append(MATS['trim'])
        c.suave(rb, 0)
        obs.append(rb)
    for sgn, nom in ((-1, "L"), (1, "R")):
        obs.append(elipsoide("Gluteo%s" % nom, (0.080 * sgn, .140, 0.430),
                             (.092, .062, .070), MATS['short'], 22, 14, 1))
    # lazada del short: dos gotas pequeñas y dos cabos
    for sgn in (-1, 1):
        lz = elipsoide("Lazo%s" % ("L" if sgn < 0 else "R"),
                       (0.026 * sgn, -.176, 0.474), (.024, .012, .015),
                       MATS['trim'], 14, 10, 1)
        obs.append(lz)
        cb = capsula("Cabo%s" % ("L" if sgn < 0 else "R"),
                     (0.010 * sgn, -.178, 0.468), (0.030 * sgn, -.180, 0.436),
                     .008, .006, MATS['trim'], 8)
        obs.append(cb)
    log("  ropa: top ceñido, tirantes, short con vivos y lazada")
    return obs


# ============ construccion ==============================================

def construir():
    c.empezar()
    materiales()
    h = cabeza()
    corona()
    cara_sprite(h)
    nariz()
    t = torso()
    pepitas(t, 20, 0.42, 0.78, radio=.013, seed=23)
    brazos(); piernas(); zapatillas(); ropa()
    bpy.context.view_layer.update()
    return h, t


# ============ camara, luces y render ====================================

def escena_render():
    s = bpy.context.scene
    s.render.film_transparent = True
    # AgX (el de serie desde Blender 4) desatura a proposito para que la
    # foto parezca real. En un personaje de juego se come el color: el rojo
    # de la fresa salia rosa palo y el naranja, melocoton.
    try:
        s.view_settings.view_transform = 'Standard'
        s.view_settings.look = 'None'
    except Exception:
        pass
    s.render.resolution_x = 640
    s.render.resolution_y = 900
    try:
        s.render.engine = 'CYCLES'
        s.cycles.samples = 40
        s.cycles.use_denoising = True
    except Exception:
        pass
    # con Standard la luz quema antes: menos energia que con AgX
    for nombre, energia, loc, tam in (
            ("Key",  520, (-2.6, -4.2, 3.4), 7),
            ("Fill", 190, (3.4, -3.0, 1.2), 8),
            ("Rim",  300, (-1.4, 3.4, 2.6), 5)):
        d = bpy.data.lights.new(nombre, 'AREA'); d.energy = energia; d.size = tam
        o = bpy.data.objects.new(nombre, d); o.location = loc
        bpy.context.scene.collection.objects.link(o)
        o.rotation_mode = 'QUATERNION'
        o.rotation_quaternion = (Vector((0, 0, 0.85)) - Vector(loc)).to_track_quat('-Z', 'Y')


def vista(nombre, angulo_grados, alto=0.85, ancho=2.05):
    """Camara ortografica dando la vuelta al personaje, como el turnaround.
    `alto` es la altura a la que mira y `ancho` cuanto abarca: con los dos
    se saca tanto el cuerpo entero como un primer plano de la cara."""
    s = bpy.context.scene
    cam = bpy.data.objects.get("CamVista")
    if cam is None:
        cd = bpy.data.cameras.new("CamVista")
        cd.type = 'ORTHO'
        cam = bpy.data.objects.new("CamVista", cd)
        s.collection.objects.link(cam)
    cam.data.ortho_scale = ancho
    s.camera = cam
    a = math.radians(angulo_grados)
    d = 6.0
    cam.location = (d * math.sin(a), -d * math.cos(a), alto)
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector((0, 0, alto)) - Vector(cam.location)).to_track_quat('-Z', 'Y')
    ruta = str(OUT / ("fresita_%s%s.png" % (nombre, SUFIJO)))
    s.render.filepath = ruta
    bpy.ops.render.render(write_still=True)
    log("RENDER %s" % ruta)


SUFIJO = ""


def main():
    global SUFIJO, EXPRESION
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    for a in argv:
        if a.startswith("sufijo="):
            SUFIJO = a[7:]
        elif a.startswith("expresion="):
            EXPRESION = a[10:]
    h, t = construir()
    caja, centro = c._extremos(None)
    log("[medida] ancho %.3f  fondo %.3f  alto %.3f  centro z %.3f"
        % (caja[0], caja[1], caja[2], centro[2]))
    blend = str(OUT / "fresita.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    log("BLEND %s" % blend)
    if "solo-blend" in argv:
        return
    escena_render()
    for nombre, ang in (("frente", 0), ("lado", 90), ("espalda", 180)):
        vista(nombre, ang)
    vista("cara", 0, alto=1.16, ancho=0.80)
    log("FRESITA_LISTA")


if __name__ == "__main__":
    main()

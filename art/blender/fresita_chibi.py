"""Fresita chibi - FrutiCity. LA FRUTA ES EL CUERPO.

Hecha desde cero mirando la lamina que paso Fran (el panel 7: la fresa de
pie, saludando). No es la Fresita de `fresita_sheet.py`, que es otra cosa:
alli la fresa es la CABEZA de una chica con cuerpo humano y ropa. Aqui no
hay cuerpo debajo. La fresa entera es el personaje, y de ella salen cuatro
churros: dos brazos con manopla y dos piernas con zapatilla.

Esa es toda la diferencia, y es la que decide el resto:

- No hay cuello ni hombros, asi que los brazos NACEN del costado de la
  fruta, a la altura del ecuador, y no de un torso.
- La cara es enorme y va PUESTA SOBRE la curva, no en un plano: ojos,
  cejas y boca se colocan calculando el radio del perfil a esa altura y
  empujandolos hacia fuera. Pegados en un plano, a la que la camara se
  mueve tres grados se despegan de la piel.
- Las pepitas esquivan la cara. Sembradas por toda la fruta, la primera
  cae sobre un ojo y parece una verruga.

El estudio (luces, camara, materiales) es el de `comun.py`, como todas las
piezas de la familia: si cada ficha se trae sus luces, en cuanto se retoca
una el reparto deja de casar.

Uso:
    blender --background --python fresita_chibi.py
    blender --background --python fresita_chibi.py -- 720   (tamano PNG)
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import bpy
from mathutils import Vector
import comun; importlib.reload(comun)
from comun import *

SALIDA = os.path.join(AQUI, "fresita_chibi")

# ============ MANDOS ============
# El perfil de la fresa, de la punta de abajo (z=0) a la cima. Ancha y alta
# arriba, punta redondeada abajo: si la punta se hace afilada de verdad, de
# pie parece un trompo y no un personaje.
PERFIL = [(0.000, 0.000), (0.150, 0.055), (0.285, 0.155), (0.410, 0.310),
          (0.510, 0.490), (0.577, 0.680), (0.615, 0.880), (0.625, 1.080),
          (0.610, 1.250), (0.560, 1.390), (0.470, 1.490), (0.330, 1.552),
          (0.170, 1.585), (0.000, 1.595)]
SUELO_CUERPO = 0.34          # a que altura flota el cuerpo: debajo van las patas

PIEL, PIEL_DK = "E03A2F", "A82018"
PEPITA        = "F7CE4B"
VERDE, VERDE_DK = "57BE4A", "2F8C36"
GUANTE, SUELA = "FFFBF2", "FFFBF2"
ZAPA, ZAPA_DK = "E34438", "A82018"
OJO, PUPILA, BRILLO = "FFFFFF", "241A18", "FFFFFF"
CEJA, BOCA, LENGUA = "5A2A1C", "6E1A1A", "E8637A"
DIENTE = "FFFDF6"

PEPITAS = 42                 # por toda la fruta menos la cara
R_PEPITA = 0.032             # pequenas: a 0.045 se leian como lunares pegados

# La cara. Las alturas son sobre el cuerpo (antes de subirlo a SUELO_CUERPO).
Z_OJOS, SEP_OJOS, R_OJO = 1.075, 0.212, 0.196
Z_CEJAS = 1.335
Z_BOCA = 0.735               # baja: pegada a los ojos se leia como un hocico
SALE_OJO = 0.085             # cuanto asoma el ojo por delante de la piel
# ================================


def _radio(z):
    """El radio del cuerpo a esa altura, interpolando el perfil. Es lo que
    permite poner cualquier cosa SOBRE la piel sin adivinar."""
    z = max(PERFIL[0][1], min(PERFIL[-1][1], z))
    for (r0, z0), (r1, z1) in zip(PERFIL, PERFIL[1:]):
        if z0 <= z <= z1:
            t = 0.0 if z1 == z0 else (z - z0) / (z1 - z0)
            return r0 + (r1 - r0) * t
    return PERFIL[-1][0]


def _en_piel(x, z, fuera=0.0):
    """Punto de la superficie a la altura z y desplazamiento lateral x, con
    `fuera` de margen hacia delante. El frente es -Y (de ahi mira la camara)."""
    r = _radio(z)
    y = -math.sqrt(max(r * r - x * x, 0.0)) - fuera
    return (x, y, z)


def cuerpo(m_piel):
    ob = revolucion(PERFIL, seg=72, nombre="Fresa")
    ob.data.materials.append(m_piel)
    suave(ob, 2)
    return ob


def pepitas(m_pepita):
    """Sembradas en espiral para que no salgan en filas, y saltando la cara.
    Van METIDAS a medias en la piel: una pepita entera encima es un grano."""
    fuera = []
    n = PEPITAS
    for i in range(n):
        t = (i + 0.5) / n
        z = 0.22 + t * 1.18
        ang = math.radians(137.5 * i)                 # angulo de oro: reparte solo
        frente = math.cos(ang)                        # 1 = de cara a la camara
        if frente > 0.45 and 0.55 < z < 1.45:
            continue                                  # ahi va la cara
        r = _radio(z)
        x, y = r * math.sin(ang), -r * math.cos(ang)
        s = esfera("Pepita%02d" % i, R_PEPITA, (x * 0.97, y * 0.97, z),
                   escala=(1.0, 1.0, 1.55), seg=12, anillos=8)
        s.rotation_euler = (0.0, 0.0, -ang)
        s.data.materials.append(m_pepita)
        suave(s, 1)
        fuera.append(s)
    return fuera


def corona(m_verde, m_verde_dk):
    """Seis hojas y el rabito. Las hojas se abren hacia fuera y hacia
    ARRIBA: caidas sobre la fruta parecen un gorro, y lo que queremos es
    que se lea el pelo verde de la lamina."""
    cima = PERFIL[-1][1]
    piezas = []
    for i in range(7):
        a = 360.0 / 7 * i + 12.0
        rad = math.radians(a)
        piezas.append(hoja_puesta(
            m_verde, (0.125 * math.cos(rad), 0.125 * math.sin(rad), cima - 0.055),
            (0.0, -44.0, a), largo=0.38, ancho=0.150, grosor=0.026,
            nombre="Hoja%d" % i))
    rab = tallo(m_verde_dk, (0.0, 0.0, cima + 0.085), (0, 0, 0),
                r_base=0.062, r_punta=0.040, alto=0.20, nombre="Rabito")
    piezas.append(rab)
    return piezas


def ojo(lado, m_ojo, m_pupila, m_brillo):
    x = SEP_OJOS * lado
    bx, by, bz = _en_piel(x, Z_OJOS, fuera=-0.075)     # el centro va METIDO
    piezas = []
    o = esfera("Ojo%+d" % lado, R_OJO, (bx, by, bz), escala=(0.92, 0.78, 1.06))
    o.data.materials.append(m_ojo); suave(o, 2); piezas.append(o)
    # La pupila no va centrada: mirando un pelin al centro, la cara enfoca a
    # quien la mira. Centradas del todo, los dos ojos miran en paralelo y la
    # expresion se vuelve de muneco de escaparate.
    px, py, pz = bx - 0.022 * lado, by - R_OJO * 0.62, bz - 0.012
    p = esfera("Pupila%+d" % lado, R_OJO * 0.62, (px, py, pz), escala=(0.92, 0.62, 1.02))
    p.data.materials.append(m_pupila); suave(p, 2); piezas.append(p)
    b = esfera("Brillo%+d" % lado, R_OJO * 0.22,
               (px - 0.045 * lado, py - 0.055, pz + 0.062), escala=(1, 0.6, 1))
    b.data.materials.append(m_brillo); suave(b, 1); piezas.append(b)
    return piezas


def cejas(m_ceja):
    piezas = []
    for lado in (-1, 1):
        x = SEP_OJOS * lado
        cx, cy, cz = _en_piel(x, Z_CEJAS, fuera=0.012)
        c = caja("Ceja%+d" % lado, (0.185, 0.055, 0.048), (cx, cy, cz),
                 rot=(0, 0, 0), canto=0.020, seg=3)
        # El signo IMPORTA y es la diferencia entre simpatica y borde: con la
        # punta de dentro caida hacia el centro, la cara se enfada sola. Mirado
        # en el render, no calculado.
        # El giro que cuenta es el de Y, que es el eje de la camara: es el que
        # inclina la ceja EN LA PANTALLA. Con la punta de dentro caida, la cara
        # se enfada sola por mucho que la boca sonria. Mirado en el render.
        c.rotation_euler = (math.radians(-8.0), math.radians(14.0 * lado),
                            math.radians(-7.0 * lado))
        c.data.materials.append(m_ceja)
        piezas.append(c)
    return piezas


def boca(m_boca, m_lengua, m_diente):
    """Sonrisa abierta: el hueco oscuro y la lengua al fondo. La lengua es
    lo que la separa de un agujero pintado."""
    # METIDA en la fruta (fuera negativo y grande): asomando, la boca deja de
    # ser un hueco y se convierte en un morro pegado a la cara.
    bx, by, bz = _en_piel(0.0, Z_BOCA, fuera=-0.115)
    # Y ALTA, no una raja: a 0.40 de escala en Z el hueco medio dedo y la boca
    # se leia cerrada, una linea oscura. Una sonrisa abierta necesita hueco.
    hueco = esfera("Boca", 0.300, (bx, by, bz), escala=(1.05, 0.46, 0.66))
    hueco.data.materials.append(m_boca); suave(hueco, 2)
    lx, ly, lz = bx, by - 0.020, bz - 0.085
    lengua = esfera("Lengua", 0.165, (lx, ly, lz), escala=(1.0, 0.52, 0.44))
    lengua.data.materials.append(m_lengua); suave(lengua, 2)
    # La banda de dientes arriba. Es un detalle de nada y hace la mitad del
    # trabajo: sin ella, el hueco oscuro se lee como una boca desdentada.
    dx, dy, dz = bx, by - 0.020, bz + 0.098
    dientes = esfera("Dientes", 0.190, (dx, dy, dz), escala=(1.12, 0.50, 0.26))
    dientes.data.materials.append(m_diente); suave(dientes, 2)
    return [hueco, lengua, dientes]


def brazo(lado, arriba, m_piel, m_guante):
    """Un churro que sale del costado. `arriba` levanta la mano: en la
    lamina una saluda y la otra cuelga, y esa asimetria es la mitad de la
    gracia del personaje."""
    z0 = 0.92
    r = _radio(z0)
    ang = math.radians(74.0)
    x0, y0 = lado * r * math.sin(ang) * 0.88, -r * math.cos(ang) * 0.88
    if arriba:
        pts = [(x0, y0, z0), (lado * (r + 0.16), y0 - 0.05, z0 + 0.18),
               (lado * (r + 0.30), y0 - 0.10, z0 + 0.46),
               (lado * (r + 0.34), y0 - 0.12, z0 + 0.70)]
        mano = (lado * (r + 0.36), y0 - 0.13, z0 + 0.82)
    else:
        pts = [(x0, y0, z0), (lado * (r + 0.17), y0 - 0.04, z0 - 0.16),
               (lado * (r + 0.26), y0 - 0.08, z0 - 0.40),
               (lado * (r + 0.27), y0 - 0.10, z0 - 0.56)]
        mano = (lado * (r + 0.28), y0 - 0.11, z0 - 0.68)
    br = cuerda("Brazo%+d" % lado, pts, 0.062)
    br.data.materials.append(m_piel)
    g = esfera("Guante%+d" % lado, 0.135, mano, escala=(1.0, 0.92, 1.06))
    g.data.materials.append(m_guante); suave(g, 2)
    # El pulgar: una bolita pegada. Sin el, la manopla es una pelota.
    pul = esfera("Pulgar%+d" % lado, 0.058,
                 (mano[0] - 0.10 * lado, mano[1] - 0.045, mano[2] + 0.03))
    pul.data.materials.append(m_guante); suave(pul, 1)
    return [br, g, pul]


def pierna(lado, m_piel, m_zapa, m_suela):
    x = 0.225 * lado
    pts = [(x * 0.7, 0.0, SUELO_CUERPO + 0.10), (x, 0.0, SUELO_CUERPO - 0.02),
           (x, -0.01, 0.115)]
    pn = cuerda("Pierna%+d" % lado, pts, 0.070)
    pn.data.materials.append(m_piel)
    # La zapatilla: caja redondeada, puntera y suela. Mirando de frente lo
    # unico que se ve es la puntera, asi que ahi es donde va el volumen.
    z = caja("Zapa%+d" % lado, (0.300, 0.470, 0.185), (x, -0.090, 0.130),
             canto=0.065, seg=3)
    z.data.materials.append(m_zapa)
    punta = esfera("Punta%+d" % lado, 0.152, (x, -0.255, 0.115),
                   escala=(1.0, 0.95, 0.82))
    punta.data.materials.append(m_zapa); suave(punta, 2)
    s = caja("Suela%+d" % lado, (0.330, 0.545, 0.080), (x, -0.100, 0.042),
             canto=0.034, seg=3)
    s.data.materials.append(m_suela)
    # Los pies se abren un poco hacia fuera. Paralelos y de frente, el
    # personaje se planta como un soldado y pierde toda la guasa.
    for pieza in (z, punta, s):
        pieza.rotation_euler = (0.0, 0.0, math.radians(-13.0 * lado))
    return [pn, z, punta, s]


def construir():
    empezar()
    m_piel = carne(mat("Piel", hexcol(PIEL), 0.34, 0.30))
    m_piel_dk = mat("PielOscura", hexcol(PIEL_DK), 0.40, 0.10)
    m_pepita = mat("Pepita", hexcol(PEPITA), 0.30, 0.35)
    m_verde = mat("Verde", hexcol(VERDE), 0.38, 0.20)
    m_verde_dk = mat("VerdeOscuro", hexcol(VERDE_DK), 0.42, 0.10)
    m_ojo = mat("Ojo", hexcol(OJO), 0.20, 0.55)
    m_pupila = mat("Pupila", hexcol(PUPILA), 0.24, 0.45)
    m_brillo = mat("Brillo", hexcol(BRILLO), 0.12, 0.60)
    m_ceja = mat("Ceja", hexcol(CEJA), 0.46, 0.05)
    m_boca = mat("Boca", hexcol(BOCA), 0.42, 0.10)
    m_lengua = mat("Lengua", hexcol(LENGUA), 0.34, 0.25)
    m_diente = mat("Dientes", hexcol(DIENTE), 0.24, 0.45)
    m_guante = mat("Guante", hexcol(GUANTE), 0.32, 0.20)
    m_zapa = mat("Zapa", hexcol(ZAPA), 0.34, 0.25)
    m_suela = mat("Suela", hexcol(SUELA), 0.36, 0.15)

    fruta = [cuerpo(m_piel)]
    fruta += pepitas(m_pepita)
    fruta += corona(m_verde, m_verde_dk)
    fruta += ojo(-1, m_ojo, m_pupila, m_brillo)
    fruta += ojo(+1, m_ojo, m_pupila, m_brillo)
    fruta += cejas(m_ceja)
    fruta += boca(m_boca, m_lengua, m_diente)
    # Todo el cuerpo sube a la vez: las medidas de la cara y de las pepitas
    # estan contadas sobre el perfil, que empieza en cero.
    for ob in fruta:
        ob.location = (ob.location.x, ob.location.y, ob.location.z + SUELO_CUERPO)

    patas = []
    patas += brazo(-1, True, m_piel, m_guante)
    patas += brazo(+1, False, m_piel, m_guante)
    for ob in patas:
        ob.location = (ob.location.x, ob.location.y, ob.location.z + SUELO_CUERPO)
    patas += pierna(-1, m_piel, m_zapa, m_suela)
    patas += pierna(+1, m_piel, m_zapa, m_suela)

    todo = fruta + patas
    terminar(*todo)
    return todo


def render(px=640):
    S = bpy.context.scene
    S.render.engine = 'CYCLES'
    S.cycles.samples = 160
    S.cycles.use_denoising = True
    S.render.image_settings.file_format = 'PNG'
    S.view_settings.view_transform = 'Standard'
    # Fondo gris y NO transparente: esto es una hoja de personaje, no un
    # tile. Sobre transparente, el guante blanco y la suela se pierden y no
    # hay forma de juzgar la silueta.
    S.render.film_transparent = False
    mundo = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    S.world = mundo
    mundo.use_nodes = True
    mundo.node_tree.nodes["Background"].inputs[0].default_value = (0.16, 0.19, 0.21, 1)
    S.render.resolution_x = S.render.resolution_y = px
    if not os.path.isdir(SALIDA): os.makedirs(SALIDA)
    S.render.filepath = os.path.join(SALIDA, "fresita_frente.png")
    bpy.ops.render.render(write_still=True)
    print("[fresita] PNG frente")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    px = int(argv[0]) if argv else 640
    construir()
    render(px)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(SALIDA, "fresita_chibi.blend"))
    print("[fresita] BLEND guardado")

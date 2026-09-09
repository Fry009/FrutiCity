"""El reparto de portada: fresi, pablo y nora.

Los tres comparten cuerpo, esqueleto y cara de calco; lo unico que cambia
es la cabeza, la paleta y el corte de la ropa. Asi la familia se parece
entre si (que es lo que hace que un reparto lea como reparto) y el rig de
fresita_rig.py vale para los tres sin tocar nada.

Nombres: los del reparto que ya existia en reparto_v3.NAMES.
    fresi = fresa    pablo = platano    nora = naranja

Uso:
    blender --background --python frutis.py -- fresi
    blender --background --python frutis.py -- todos
"""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import comun as c
import fresita_sheet as F

OUT = HERE / 'fresita_v5'

# ============ los tres personajes =======================================

FRESI = dict(
    nombre="fresi", etiqueta="Fresita",
    piel="D8392F", piel_dk="A82018",
    perfil=[(0.000, 0.830), (0.075, 0.845), (0.155, 0.885), (0.240, 0.950),
            (0.298, 1.030), (0.330, 1.120), (0.340, 1.210), (0.322, 1.300),
            (0.268, 1.380), (0.190, 1.442), (0.095, 1.482), (0.000, 1.500)],
    semillas=34, curva=0.0, poro=None, lobulos=None,
    corona="fresa",
    cara=dict(yaw=55.0, za=0.95, zb=1.34, plano=0.20),
    ropa="top",
    tela="F5A2C0", tela2="F192B6", vivo="FFFFFF", zapa="F3A8C6",
    iris="8B9A6C", ceja="4A2A1E",
)

PABLO = dict(
    nombre="pablo", etiqueta="Platano",
    piel="F5C63A", piel_dk="C99518",
    # mas estrecho y mas alto que las otras dos: es lo que lo hace platano
    perfil=[(0.000, 0.812), (0.050, 0.840), (0.100, 0.888), (0.145, 0.960),
            (0.176, 1.052), (0.192, 1.156), (0.196, 1.258), (0.188, 1.356),
            (0.164, 1.444), (0.118, 1.518), (0.058, 1.572), (0.000, 1.598)],
    semillas=0, curva=0.135, poro=None, lobulos=(5, 0.055),
    corona="platano",
    cara=dict(yaw=48.0, za=0.98, zb=1.36, plano=0.22),
    ropa="camiseta",
    tela="3FA9D6", tela2="27618F", vivo="FFFFFF", zapa="F2F2F4",
    iris="6B4A2A", ceja="4A3018",
)

NORA = dict(
    nombre="nora", etiqueta="Naranja",
    piel="FF8A0F", piel_dk="C25A00",
    perfil=[(0.000, 0.830), (0.105, 0.860), (0.190, 0.905), (0.262, 0.975),
            (0.305, 1.060), (0.325, 1.155), (0.322, 1.250), (0.292, 1.340),
            (0.230, 1.415), (0.140, 1.465), (0.062, 1.486), (0.000, 1.494)],
    semillas=0, curva=0.0, poro=(150.0, 0.22), lobulos=None,
    corona="naranja",
    cara=dict(yaw=54.0, za=0.95, zb=1.33, plano=0.20),
    ropa="vestido",
    tela="FFFFFF", tela2="4FC2A6", vivo="FFD75E", zapa="4FC2A6",
    iris="7A5230", ceja="4A3018",
)

REPARTO = {p["nombre"]: p for p in (FRESI, PABLO, NORA)}


# ============ coronas ===================================================

def corona(tipo, perfil):
    z_cima = perfil[-1][1]
    if tipo == "fresa":
        return F.corona()
    if tipo == "naranja":
        hojas = []
        for k, (ang, caida, largo) in enumerate(((-70, 46, .30), (110, 52, .26),
                                                 (20, 40, .22))):
            hojas.append(c.hoja_puesta(MATS_LOCAL['leaf'], (0, 0, z_cima - .012),
                                       (caida, -6, ang), largo=largo, ancho=.090,
                                       grosor=.016, nombre="Hoja"))
        hojas.append(c.tallo(MATS_LOCAL['leaf'], (0, 0, z_cima + .030), rot=(6, 0, 0),
                             r_base=.034, r_punta=.024, alto=.10, caras=12,
                             nombre="Rabito"))
        F.log("  corona: 3 hojas y rabito de naranja")
        return hojas
    if tipo == "platano":
        # las dos puntas oscuras: sin ellas es un melon amarillo
        obs = [F.elipsoide("Punta", (0.075, 0, z_cima - .030), (.055, .052, .050),
                           MATS_LOCAL['punta'], 18, 12, 1),
               F.elipsoide("Punta", (0.075, 0, 0.856), (.052, .048, .044),
                           MATS_LOCAL['punta'], 18, 12, 1)]
        obs.append(c.tallo(MATS_LOCAL['punta'], (0.070, 0, z_cima + .036),
                           rot=(-8, 0, 0), r_base=.026, r_punta=.016, alto=.10,
                           caras=10, nombre="Rabito"))
        F.log("  corona: puntas y rabito de platano")
        return obs
    raise ValueError(tipo)


# ============ ropa ======================================================

def ropa(tipo):
    if tipo == "top":
        return F.ropa()

    obs = []
    if tipo == "camiseta":
        # camiseta hasta la cadera, con manga corta
        cam = F._cascara("Camiseta", 0.452, 0.792, .017, MATS_LOCAL['tela'], .015,
                         escote=.052)
        obs.append(cam)
        obs.append(F.ribete_borde(cam, MATS_LOCAL['vivo'], .015, arriba=True))
        obs.append(F.ribete_borde(cam, MATS_LOCAL['tela'], .014, arriba=False))
        for sgn, nom in ((-1, "L"), (1, "R")):
            mg = F.capsula("Manga%s" % nom, (0.150 * sgn, 0, 0.782),
                           (0.214 * sgn, .003, 0.664), .092, .080,
                           MATS_LOCAL['tela'], 24)
            obs.append(mg)
            obs.append(F.capsula("MangaVivo%s" % nom, (0.212 * sgn, .003, 0.676),
                                 (0.216 * sgn, .003, 0.662), .083, .083,
                                 MATS_LOCAL['vivo'], 24))
        # pantalon corto
        pan = F._cascara("Pantalon", 0.352, 0.478, .018, MATS_LOCAL['tela2'], .016)
        obs.append(pan)
        obs.append(F.ribete_borde(pan, MATS_LOCAL['tela2'], .015, arriba=True))
        for sgn, nom in ((-1, "L"), (1, "R")):
            pn = F.capsula("Pernera%s" % nom, (0.104 * sgn, 0, 0.412),
                           (0.114 * sgn, 0, 0.330), .116, .106,
                           MATS_LOCAL['tela2'], 28)
            pn.scale = (1, .92, 1)
            obs.append(pn)
        F.log("  ropa: camiseta con manga, cuello y pantalon corto")
        return obs

    if tipo == "vestido":
        # vestido acampanado: el radio crece hacia abajo
        pts = [(F._radio_torso(0.760) + .018, 0.760),
               (F._radio_torso(0.660) + .020, 0.660),
               (F._radio_torso(0.560) + .024, 0.560),
               (F._radio_torso(0.470) + .040, 0.470),
               (0.246, 0.400), (0.268, 0.350)]
        ve = c.revolucion(pts, seg=48, nombre="Vestido")
        ve.data.materials.append(MATS_LOCAL['tela'])
        zmax = max(v.co.z for v in ve.data.vertices)
        for v in ve.data.vertices:
            v.co.y *= F.APLASTA_Y
            if abs(v.co.z - zmax) < 1e-4:
                v.co.z -= .040 * (math.sin(math.atan2(v.co.y, v.co.x)) ** 2)
        ve.data.update()
        m = ve.modifiers.new("Grosor", 'SOLIDIFY'); m.thickness = .016; m.offset = 1
        c.suave(ve, 2)
        obs.append(ve)
        obs.append(F.ribete_borde(ve, MATS_LOCAL['tela2'], .017, arriba=False))
        obs.append(F.ribete_borde(ve, MATS_LOCAL['tela2'], .015, arriba=True))
        obs.append(F.anillo("VestidoCintura", 0.556, F._radio_torso(0.556) + .030,
                            .017, MATS_LOCAL['tela2'], aplasta=F.APLASTA_Y))
        for sgn, nom in ((-1, "L"), (1, "R")):
            obs.append(F.capsula("Tirante%s" % nom, (0.112 * sgn, -.088, 0.762),
                                 (0.122 * sgn, .070, 0.772), .020, .020,
                                 MATS_LOCAL['tela'], 10))
        # lazo en la cintura
        for sgn in (-1, 1):
            obs.append(F.elipsoide("Lazo%s" % ("L" if sgn < 0 else "R"),
                                   (0.030 * sgn, -.200, 0.556), (.032, .014, .022),
                                   MATS_LOCAL['vivo'], 16, 10, 1))
        F.log("  ropa: vestido acampanado con vivos y lazo")
        return obs
    raise ValueError(tipo)


# ============ montaje ===================================================

MATS_LOCAL = {}


def paleta(p):
    """Recolorea la paleta de fresita_sheet para este personaje y anade
    los materiales que solo usan las frutas nuevas."""
    F.SKIN, F.SKIN_DK = p["piel"], p["piel_dk"]
    F.TOP, F.SHORT = p["tela"], p["tela2"]
    F.TRIM, F.SHOE = p["vivo"], p["zapa"]
    m = F.materiales()
    if p["poro"]:
        escala, fuerza = p["poro"]
        c.poro(m['skin'], escala, fuerza)
        c.poro(m['skin_liso'], escala, fuerza)
    m['tela'] = m['top']
    m['tela2'] = m['short']
    m['vivo'] = m['trim']
    m['punta'] = c.mat("Punta", c.hexcol("6E4A1E"), .52, .06)
    MATS_LOCAL.clear(); MATS_LOCAL.update(m)
    F.MATS.update(m)
    return m


def construir(nombre, expresion="idle"):
    p = REPARTO[nombre]
    c.empezar()
    paleta(p)
    F.PERFIL_CABEZA = p["perfil"]
    F.Z_BARBILLA, F.Z_CIMA = p["perfil"][0][1], p["perfil"][-1][1]
    F.CARA_YAW = p["cara"]["yaw"]
    F.CARA_ZA, F.CARA_ZB = p["cara"]["za"], p["cara"]["zb"]
    F.CARA_PLANO = p["cara"]["plano"]
    F.CARA_Z0, F.CARA_Z1 = p["cara"]["za"] - 0.02, p["cara"]["zb"] + 0.02
    F.CARAS = HERE / 'fresita_v5' / 'caras' / nombre

    lob = p.get("lobulos") or (0, 0.0)
    h = F.cabeza(semillas=p["semillas"], curva=p["curva"],
                 lobulos=lob[0], lobulo_fuerza=lob[1])
    corona(p["corona"], p["perfil"])
    F.cara_sprite(h, expresion)
    F.nariz()
    t = F.torso()
    if p["semillas"]:
        F.pepitas(t, 20, 0.42, 0.78, radio=.013, seed=23)
    F.brazos(); F.piernas(); F.zapatillas()
    ropa(p["ropa"])
    bpy.context.view_layer.update()
    caja, centro = c._extremos(None)
    F.log("[%s] ancho %.3f  fondo %.3f  alto %.3f"
          % (nombre, caja[0], caja[1], caja[2]))
    return h, t


def retrato(nombre, vista, ang, ):
    """Un render por personaje y encuadre, con su propio nombre de fichero."""
    s = bpy.context.scene
    alto, ancho = (1.16, 0.80) if vista == "cara" else (0.85, 2.05)
    cam = bpy.data.objects.get("CamVista")
    if cam is None:
        cd = bpy.data.cameras.new("CamVista"); cd.type = 'ORTHO'
        cam = bpy.data.objects.new("CamVista", cd)
        s.collection.objects.link(cam)
    cam.data.ortho_scale = ancho
    s.camera = cam
    a = math.radians(ang)
    cam.location = (6.0 * math.sin(a), -6.0 * math.cos(a), alto)
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector((0, 0, alto)) - Vector(cam.location)).to_track_quat('-Z', 'Y')
    s.render.filepath = str(OUT / ("%s_%s.png" % (nombre, vista)))
    bpy.ops.render.render(write_still=True)
    F.log("RENDER %s_%s" % (nombre, vista))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["todos"]
    quienes = list(REPARTO) if "todos" in argv else [a for a in argv if a in REPARTO]
    for nombre in quienes:
        construir(nombre)
        destino = str(OUT / ("%s.blend" % nombre))
        bpy.ops.wm.save_as_mainfile(filepath=destino)
        F.log("BLEND %s" % destino)
        F.escena_render()
        for vista, ang in (("frente", 0), ("lado", 90), ("cara", 0)):
            retrato(nombre, vista, ang)
    F.log("REPARTO LISTO")


if __name__ == "__main__":
    main()

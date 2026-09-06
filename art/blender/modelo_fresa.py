"""Ficha de fresa - FrutiCity. Estilo Royal Match.

Cuerpo de revolucion con el maximo de anchura muy arriba (eso es lo que
la separa de un cono).

Dos cosas se copian de la fresa de verdad, y son las que la delatan:

1. Las pepitas van METIDAS en un hoyo, no pegadas encima. Puestas sobre
   la piel parecen granitos de arroz. Por eso se hunde la malla en cada
   sitio ANTES de colocarlas.
2. El caliz va doblado hacia atras y sentado en una cuenca por debajo
   del contorno, no de pie sobre la punta como una helice.

El rojo tampoco es plano: lleva degradado y algo de luz por dentro.
"""
import os, sys, math, importlib
from mathutils import Vector
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_HOMBRO = "C4132C"   # arriba, mas profundo
COLOR_PUNTA  = "F0364A"   # abajo, mas encendido
COLOR_PEPITA = "F2D06B"
COLOR_PEPITA2= "C98A34"   # una de cada dos, mas tostada
COLOR_HOJA   = "3F9B31"
COLOR_TALLO  = "4C7A2B"
BRILLO       = 0.80
RUGOSIDAD    = 0.28
JUGO         = 0.20       # cuanta luz pasa por dentro

ALTO     = 0.86
ANCHO    = 0.80
HOMBRO   = 0.45      # <1 sube el punto mas ancho. Bajo = mas de corazon
LLENO    = 0.86      # bajo = hombros mas cuadrados
HUNDIDO  = 0.15      # la cuenca de arriba, donde se sienta el caliz

FILAS      = 8
POR_FILA   = 12      # se reparten menos donde la fresa es estrecha
PEPITA     = (.040, .028, .015)
HOYO_R     = 0.058   # radio del hoyo. Mas grande y la piel parece acolchada
HOYO_H     = 0.018   # cuanto se hunde
HUNDE      = 0.004   # cuanto se mete la pepita dentro del hoyo

HOJAS_CORONA = 8
CORONA_CAIDA = -34.0 # grados. Positivo = la punta cae. Reflexo pero visible:
                     # del todo caido queda tapado por el hombro y no se lee
CORONA_LARGO = 0.70
CORONA_SUBE  = 0.11  # las hojas nacen en el BORDE de la cuenca, no en el fondo
# ================================

# malla densa: con pocos anillos el hoyito no se resuelve y desaparece
PASOS, SEG = 64, 88


def perfil():
    """Punto mas ancho arriba, punta redondeada abajo."""
    pts = []
    for i in range(PASOS + 1):
        t = i / PASOS
        r = math.sin(math.pi * (t ** HOMBRO)) ** LLENO
        z = ALTO * math.cos(math.pi * t)
        if z > 0:
            z -= HUNDIDO * math.exp(-(r / 0.50) ** 2)
        pts.append((r, z))
    return pts


def _en(pts, t):
    """Punto y normal del perfil en t, en el plano (r, z)."""
    x = t * PASOS
    i0 = max(0, min(PASOS - 1, int(x))); f = x - i0
    r = pts[i0][0] * (1 - f) + pts[i0 + 1][0] * f
    z = pts[i0][1] * (1 - f) + pts[i0 + 1][1] * f
    dr = pts[i0 + 1][0] - pts[i0][0]
    dz = pts[i0 + 1][1] - pts[i0][1]
    n = Vector((dz, -dr))
    if n.length > 1e-9: n.normalize()
    return r, z, n


def sitios(pts):
    """Donde va cada pepita: punto en la piel y normal de la piel ahi.
    Se calcula antes de tocar la malla, para poder hacer el hoyo y luego
    meter la pepita exactamente en el mismo sitio."""
    rmax = max(p[0] for p in pts) * ANCHO
    fuera = []
    for fila in range(FILAS):
        t = 0.11 + (0.83 - 0.11) * fila / (FILAS - 1.0)
        r, z, n = _en(pts, t)
        r *= ANCHO
        cuantas = max(3, int(round(POR_FILA * r / rmax)))
        desfase = (math.pi / cuantas) * (fila % 2)      # al tresbolillo
        for k in range(cuantas):
            th = 2 * math.pi * k / cuantas + desfase
            n3 = Vector((n.x * math.cos(th), n.x * math.sin(th), n.y))
            if n3.length > 1e-9: n3.normalize()
            fuera.append((Vector((r * math.cos(th), r * math.sin(th), z)), n3))
    return fuera


def pepitas(claro, oscuro, sitios_):
    for i, (p, n3) in enumerate(sitios_):
        e = esfera("Pepita", 1.0, p - n3 * (HOYO_H + HUNDE), PEPITA, 12, 8)
        e.rotation_mode = 'QUATERNION'
        e.rotation_quaternion = n3.to_track_quat('Z', 'Y')
        e.data.materials.append(claro if i % 2 else oscuro)
        suave(e, 0)


def corona(hoja_mat, tallo_mat, z):
    """Caliz reflexo: las hojas salen hacia fuera y caen sobre el hombro,
    no se levantan. Largos alternos para que no parezca una tuerca."""
    for k in range(HOJAS_CORONA):
        ang = 360.0 * k / HOJAS_CORONA + 11.0
        largo = CORONA_LARGO * (1.0 if k % 2 else 0.82)
        caida = CORONA_CAIDA + (6.0 if k % 2 else -4.0)
        hoja_puesta(hoja_mat, loc=(0, 0, z + CORONA_SUBE), rot=(90, caida, ang),
                    largo=largo, ancho=.155, grosor=.016, nombre="HojaCorona")
    tallo(tallo_mat, loc=(0, 0, z + CORONA_SUBE + .10), rot=(5, 0, 0),
          r_base=.050, r_punta=.040, alto=.20, caras=12)


def construir():
    empezar()
    pts = perfil()
    sitios_ = sitios(pts)

    ob = revolucion(pts, ANCHO, SEG, "Fresa")
    hoyitos(ob, [p for p, _ in sitios_], HOYO_R, HOYO_H)

    piel = mat("Piel", hexcol(COLOR_PUNTA), RUGOSIDAD, BRILLO)
    degradado(piel, hexcol(COLOR_PUNTA), hexcol(COLOR_HOMBRO),
              eje=2, desde=-ALTO, hasta=ALTO)
    carne(piel, JUGO, (0.42, 0.14, 0.09))
    ob.data.materials.append(piel)
    suave(ob, 2)

    pepitas(mat("Pepita", hexcol(COLOR_PEPITA), .40, .35),
            mat("Pepita2", hexcol(COLOR_PEPITA2), .45, .30),
            sitios_)

    # la cuenca: el caliz se sienta ahi, por debajo del contorno
    corona(mat("Hoja", hexcol(COLOR_HOJA), .50, .25),
           mat("Tallo", hexcol(COLOR_TALLO), .75),
           ALTO - HUNDIDO)

    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return ob


if __name__ == "__main__":
    construir()

"""Ficha de manzana - FrutiCity / Frutinovelas. Estilo Royal Match.
Guardar este archivo hace que Blender lo reconstruya solo si el vigilante corre.
El perfil NO son puntos a mano: se genera con una funcion, para que la
curvatura sea continua y no salgan escalones ni tramos rectos.
El estudio (luces, camara, materiales) vive en comun.py.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_PIEL   = "F0453C"   # rojo caramelo
COLOR_HOJA   = "4FA83A"   # verde hoja, no lima
COLOR_TALLO  = "6B4423"
BRILLO       = 0.85       # barniz: el brillo gordo de Royal Match
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


def construir():
    empezar()
    ob = revolucion(perfil(), ANCHO, SEG, "Manzana",
                    LOBULOS, LOBULO_FUERZA, LOBULO_FASE)
    ob.data.materials.append(mat("Piel", hexcol(COLOR_PIEL), RUGOSIDAD, BRILLO))
    suave(ob, 2)

    suelo = ALTO - HOYUELO      # fondo del hoyuelo: ahi nace el rabito

    tallo(mat("Tallo", hexcol(COLOR_TALLO), .85),
          loc=(0, 0, suelo + .11), rot=(5, 0, -7))

    hoja_puesta(mat("Hoja", hexcol(COLOR_HOJA), .50, .30),
                loc=(.07, -.07, suelo + .07), rot=(90, -40, 12))

    if CARA:
        ojo = mat("Ojo", hexcol("3A2320"), .30, .5)
        for sx in (-.27, .27):
            e = esfera("Ojo", .115, (sx, -.74, .10), (1.0, .55, 1.25), 20, 12)
            e.data.materials.append(ojo)
            suave(e, 0)

    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return ob


if __name__ == "__main__":
    construir()

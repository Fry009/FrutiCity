"""Ficha de moneda - FrutiCity. Pieza especial.

Tres discos apilados, no uno con textura: el canto oscuro, la cara clara
y la estrella en relieve. Asi el brillo del barniz cae distinto en cada
altura y la moneda tiene grosor de verdad.
"""
import os, sys, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_CANTO   = "C97F14"    # el borde, mas oscuro que la cara
COLOR_CARA    = ORO
COLOR_RELIEVE = ORO_CLARO
BRILLO        = 0.70
RUGOSIDAD     = 0.26

RADIO   = 0.92
GRUESO  = 0.26
CARA    = 0.78      # radio de la cara hundida
CARA_Z  = 0.32      # sobresale un pelo por los dos lados

REL_FUERA, REL_DENTRO, REL_Z = 0.46, 0.20, 0.40

ENCARA = (84.0, 0.0, -6.0)
# ================================


def construir():
    empezar()
    canto = cilindro("Moneda", RADIO, GRUESO, caras=40, canto=.05)
    canto.data.materials.append(mat("Canto", hexcol(COLOR_CANTO), RUGOSIDAD + .08, BRILLO))

    cara = cilindro("MonedaCara", CARA, CARA_Z, caras=40, canto=.04)
    cara.data.materials.append(mat("Cara", hexcol(COLOR_CARA), RUGOSIDAD, BRILLO))

    rel = prisma(estrella(5, REL_FUERA, REL_DENTRO), REL_Z, "Relieve", .03, 3)
    rel.data.materials.append(mat("Relieve", hexcol(COLOR_RELIEVE), RUGOSIDAD, BRILLO))

    obs = [canto, cara, rel]
    girar(obs, ENCARA)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

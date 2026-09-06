"""Ficha de estrella - FrutiCity. Pieza especial.

Dos estrellas, no una: la de dentro sobresale por las dos caras y hace de
chaflan brillante. Con una sola, el oro sale plano y la pieza parece una
pegatina en vez de un objeto.
"""
import os, sys, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR      = ORO
COLOR_ALMA = ORO_CLARO
BRILLO     = 0.70
RUGOSIDAD  = 0.24

PUNTAS  = 5
FUERA   = 0.95
DENTRO  = 0.42
GRUESO  = 0.30

ALMA    = 0.76      # que porcion de la estrella ocupa la de dentro
ALMA_Z  = 1.42      # cuanto sobresale por delante y por detras
CANTO   = 0.055     # el bisel: sin el, la estrella corta como un cuchillo

ENCARA  = (84.0, 0.0, -4.0)
# ================================


def construir():
    empezar()
    fuera = prisma(estrella(PUNTAS, FUERA, DENTRO), GRUESO, "Estrella", CANTO, 3)
    fuera.data.materials.append(mat("Oro", hexcol(COLOR), RUGOSIDAD, BRILLO))

    alma = prisma(estrella(PUNTAS, FUERA * ALMA, DENTRO * ALMA * 1.04),
                  GRUESO * ALMA_Z, "EstrellaAlma", CANTO * .8, 3)
    alma.data.materials.append(mat("OroClaro", hexcol(COLOR_ALMA), RUGOSIDAD, BRILLO))

    obs = [fuera, alma]
    girar(obs, ENCARA)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

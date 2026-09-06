"""Ficha de uvas - FrutiCity. Estilo Royal Match.
Un racimo no es un monton de bolas: es un triangulo que se estrecha hacia
abajo. Las filas se declaran a mano (no al azar) para que la silueta sea
siempre la misma; el azar solo mueve cada grano un pelo, con semilla fija.
"""
import os, sys, math, importlib, random
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_UVA   = "7B3FBE"   # morado uva
COLOR_FONDO = "56287F"   # los granos de detras, mas apagados
COLOR_HOJA  = "4FA83A"
COLOR_TALLO = "5C4326"
BRILLO      = 0.92       # uva = casi charol
RUGOSIDAD   = 0.22

GRANO   = 0.29           # radio del grano
APLASTA = 0.94           # los granos son un pelin ovalados
BAILE   = 0.022          # cuanto puede moverse cada grano de su sitio

# filas del racimo, de arriba abajo: (z, [x...])
FILAS = [
    ( 0.40, [-0.55, -0.185, 0.185, 0.55]),
    ( 0.08, [-0.37,  0.00,  0.37]),
    (-0.24, [-0.19,  0.19]),
    (-0.56, [ 0.00]),
]
# granos de relleno al fondo, para que el racimo tenga volumen
FONDO = [(0.26, -0.30, 0.55), (-0.26, -0.30, 0.55), (0.00, -0.30, 0.22)]
# ================================


def racimo(frente, fondo):
    obs = []
    for z, xs in FILAS:
        for x in xs:
            p = (x + random.uniform(-BAILE, BAILE),
                 random.uniform(-BAILE, BAILE) - 0.02,
                 z + random.uniform(-BAILE, BAILE))
            e = esfera("Uva", GRANO, p, (1.0, 1.0, APLASTA), 22, 14)
            e.data.materials.append(frente)
            suave(e, 1)
            obs.append(e)
    for x, y, z in FONDO:
        e = esfera("UvaFondo", GRANO * 0.92, (x, y, z), (1.0, 1.0, APLASTA), 18, 12)
        e.data.materials.append(fondo)
        suave(e, 1)
        obs.append(e)
    return obs


def construir():
    empezar()
    frente = mat("Uva", hexcol(COLOR_UVA), RUGOSIDAD, BRILLO)
    fondo  = mat("UvaFondo", hexcol(COLOR_FONDO), RUGOSIDAD + .06, BRILLO * .7)
    obs = racimo(frente, fondo)

    cima = FILAS[0][0] + GRANO
    tallo(mat("Tallo", hexcol(COLOR_TALLO), .80),
          loc=(0, -.05, cima + .10), rot=(6, 0, -8),
          r_base=.070, r_punta=.055, alto=.28)

    hoja_puesta(mat("Hoja", hexcol(COLOR_HOJA), .50, .30),
                loc=(.06, -.10, cima + .16), rot=(90, -38, 14),
                largo=.52, ancho=.155)

    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

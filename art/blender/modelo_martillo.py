"""Ficha de martillo - FrutiCity. Pieza especial.

Va en diagonal por lo mismo que el cohete: es la pieza mas alargada de
las trece y en vertical no cabe sin encogerla hasta que no se lee.
"""
import os, sys, importlib, math
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_MANGO  = MADERA_OSCURA
COLOR_CABEZA = "94AC9A"    # acero frio. Mas claro y estas luces lo queman
COLOR_BANDA  = "6B8371"
COLOR_POMO   = ORO
BRILLO       = 0.60
RUGOSIDAD    = 0.36

MANGO   = (.135, 1.42)     # radio, largo
CABEZA  = (1.10, .52, .52)
BANDA   = (.22, .60, .60)  # el refuerzo, pegado a la cabeza
POMO    = (.185, .13)

INCLINA = 24.0             # grados: la diagonal del tile
# ================================


def construir():
    empezar()
    obs = []
    r = math.radians(INCLINA)
    arriba = (math.sin(r) * MANGO[1] / 2, 0, math.cos(r) * MANGO[1] / 2)
    abajo = (-arriba[0], 0, -arriba[2])

    ma = cilindro("Mango", MANGO[0], MANGO[1], rot=(0, INCLINA, 0), caras=20, canto=.03)
    ma.data.materials.append(mat("Mango", hexcol(COLOR_MANGO), RUGOSIDAD + .2, .25))
    obs.append(ma)

    cb = caja("Cabeza", CABEZA, loc=arriba, rot=(0, INCLINA, 0), canto=.075, seg=3)
    cb.data.materials.append(mat("Cabeza", hexcol(COLOR_CABEZA), RUGOSIDAD, BRILLO))
    obs.append(cb)

    # la banda va desplazada a lo largo del eje de la cabeza, no en X global
    dx, dz = math.cos(r) * .30, -math.sin(r) * .30
    bn = caja("Banda", BANDA, loc=(arriba[0] + dx, 0, arriba[2] + dz),
              rot=(0, INCLINA, 0), canto=.05, seg=3)
    bn.data.materials.append(mat("Banda", hexcol(COLOR_BANDA), RUGOSIDAD, BRILLO))
    obs.append(bn)

    po = cilindro("Pomo", POMO[0], POMO[1], loc=abajo, rot=(0, INCLINA, 0),
                  caras=18, canto=.03)
    po.data.materials.append(mat("Pomo", hexcol(COLOR_POMO), RUGOSIDAD, BRILLO))
    obs.append(po)

    encajar(obs)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

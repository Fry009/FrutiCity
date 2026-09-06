"""Ficha de bomba - FrutiCity. Pieza especial.

Nota: la version por codigo (FruitModels.Bomb) pega una mancha crema en
el hombro para simular el brillo. Aqui NO se pone: con luces de verdad el
brillo sale solo, y pintarlo encima daria dos brillos peleandose.
"""
import os, sys, importlib, math
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_CUERPO = "5A4874"   # morado apagado, para que el oro de la mecha cante
COLOR_TAPA   = "413352"
COLOR_MECHA  = ORO
COLOR_CHISPA = CORAL
COLOR_NUCLEO = CREMA
BRILLO       = 0.55       # mas alto y la esfera parece bola de cristal
RUGOSIDAD    = 0.30

RADIO   = 0.78
CENTRO  = -0.16          # la baja un poco: la mecha necesita sitio arriba
TAPA    = (.21, .22)     # radio, alto
MECHA_R = 0.055
MECHA_S = 0.34           # cuanto serpentea
MECHA_H = 0.46           # cuanto sube
CHISPA  = 0.155
# ================================


def mecha_puntos(n=7):
    z0 = CENTRO + RADIO + TAPA[1] * .8
    return [(math.sin(i / (n - 1.0) * 2.1) * MECHA_S,
             0.0,
             z0 + (i / (n - 1.0)) * MECHA_H) for i in range(n)]


def construir():
    empezar()
    obs = []

    cuerpo = esfera("Bomba", RADIO, (0, 0, CENTRO), seg=40, anillos=24)
    cuerpo.data.materials.append(mat("Cuerpo", hexcol(COLOR_CUERPO), RUGOSIDAD, BRILLO))
    suave(cuerpo, 1)
    obs.append(cuerpo)

    tp = cilindro("Tapa", TAPA[0], TAPA[1],
                  loc=(0, 0, CENTRO + RADIO + TAPA[1] * .35), caras=20, canto=.03)
    tp.data.materials.append(mat("Tapa", hexcol(COLOR_TAPA), RUGOSIDAD + .2, .5))
    obs.append(tp)

    pts = mecha_puntos()
    me = cuerda("Mecha", pts, MECHA_R)
    me.data.materials.append(mat("Mecha", hexcol(COLOR_MECHA), .55, .3))
    obs.append(me)

    punta = pts[-1]
    ch = esfera("Chispa", CHISPA, (punta[0], punta[1], punta[2] + .07),
                seg=20, anillos=12)
    ch.data.materials.append(mat("Chispa", hexcol(COLOR_CHISPA), .30, .8))
    suave(ch, 1)
    obs.append(ch)

    nu = esfera("Nucleo", CHISPA * .52, (punta[0], punta[1] - .05, punta[2] + .10),
                seg=16, anillos=10)
    nu.data.materials.append(mat("Nucleo", hexcol(COLOR_NUCLEO), .25, .9))
    suave(nu, 1)
    obs.append(nu)

    encajar(obs)          # con la mecha se iba a 2.58 de alto
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

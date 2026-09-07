"""Ficha de humo - FrutiCity. Efecto, no pieza de tablero.

Una bocanada de humo modelada de verdad, no un degradado radial. Lo que
la hace leerse como humo y no como una mancha es que sea un racimo de
bolas de tamanos distintos: el contorno queda con bultos, y la luz de
estudio le talla sombra entre ellos. Una sola esfera sale como una
pelota gris.

Va sin barniz y con rugosidad alta a proposito: el humo es lo unico de
esta familia que NO debe brillar. Con el barniz de las frutas parecia
un globo.
"""
import os, sys, importlib, random
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
CLARO     = "F4F2EC"        # la cresta iluminada
OSCURO    = "A8A6A0"        # la panza en sombra
RUGOSIDAD = 0.92            # humo mate: sin esto parece plastico
BARNIZ    = 0.0

BOLAS = [                   # (x, y, z, radio)
    ( 0.00,  0.00,  0.10, 0.62),
    (-0.42,  0.06, -0.14, 0.44),
    ( 0.44, -0.04, -0.10, 0.46),
    ( 0.10,  0.10,  0.48, 0.40),
    (-0.26, -0.10,  0.36, 0.34),
    ( 0.30,  0.08,  0.34, 0.32),
    ( 0.02, -0.06, -0.34, 0.38),
]
SUAVIZAR = 2
ENCARA   = (78.0, 0.0, 6.0)
# ================================


def construir():
    empezar()
    m = mat("Humo", hexcol(CLARO), RUGOSIDAD, BARNIZ)
    degradado(m, hexcol(OSCURO), hexcol(CLARO), 2, -0.9, 0.9)

    obs = []
    for i, (x, y, z, r) in enumerate(BOLAS):
        ob = esfera("Bocanada%d" % i, r, (x, y, z), seg=22, anillos=12)
        suave(ob, SUAVIZAR)
        ob.data.materials.append(m)
        obs.append(ob)

    # Sin booleanas: las bolas son opacas y comparten material, asi que desde
    # camara ya se ven como una silueta sola. Una union real aqui solo anade
    # un modificador que puede fallar en headless sin decir nada.
    girar(obs, ENCARA)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

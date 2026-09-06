"""Ficha de cohete - FrutiCity. Pieza especial.

Va inclinado: un cohete vertical dentro de un tile cuadrado desperdicia
las dos esquinas y encima no transmite movimiento. Inclinado llena la
diagonal, que es la medida larga del cuadrado.
"""
import os, sys, importlib, math
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_CUERPO  = CORAL
COLOR_MORRO   = "E2604C"
COLOR_VENTANA = CREMA
COLOR_ALETA   = ORO
COLOR_LLAMA   = "FFE27A"   # mas clara que el oro de las aletas, o se funden
COLOR_NUCLEO  = CREMA
BRILLO        = 0.80
RUGOSIDAD     = 0.28

RADIO   = 0.40
LARGO   = 1.10
MORRO   = 0.60          # alto del cono de la punta
VENTANA = (.25, .10, .25)

ALETAS  = 3
ALETA   = [(0, -.52), (.46, -.82), (.08, -.06)]   # contorno, en (x, z)
ALETA_G = 0.09          # grosor
ALETA_X = 0.26          # cuanto sale del cuerpo

LLAMA   = (.30, .07, .92)   # tiene que sobresalir POR DEBAJO de las aletas
NUCLEO  = (.17, .03, .58)

INCLINA = (0.0, -22.0, 0.0)
# ================================


def construir():
    empezar()
    obs = []
    cuerpo_m = mat("Cuerpo", hexcol(COLOR_CUERPO), RUGOSIDAD, BRILLO)

    c = cilindro("Cohete", RADIO, LARGO, caras=32, canto=.04)
    c.data.materials.append(cuerpo_m); obs.append(c)

    m = cono("Morro", RADIO, .02, MORRO, loc=(0, 0, LARGO / 2 + MORRO / 2 - .03),
             caras=32, canto=.02)
    m.data.materials.append(mat("Morro", hexcol(COLOR_MORRO), RUGOSIDAD, BRILLO))
    obs.append(m)

    v = esfera("Ventana", 1.0, (.05, -RADIO * .84, .16), VENTANA, 24, 14)
    v.data.materials.append(mat("Ventana", hexcol(COLOR_VENTANA), .18, .95))
    suave(v, 1); obs.append(v)

    aleta_m = mat("Aleta", hexcol(COLOR_ALETA), RUGOSIDAD + .06, BRILLO)
    for i in range(ALETAS):
        # el prisma nace en XY; girarlo 90 en X pone el contorno en XZ y
        # deja el grosor a lo ancho, que es como se apoya una aleta
        a = prisma(ALETA, ALETA_G, "Aleta", .02, 2)
        a.location = (ALETA_X, 0, 0)
        a.rotation_euler = (math.radians(90), 0, 0)
        a.data.materials.append(aleta_m)
        girar([a], (0, 0, 360.0 * i / ALETAS))
        obs.append(a)

    z = -LARGO / 2 - LLAMA[2] / 2 + .04
    ll = cono("Llama", LLAMA[0], LLAMA[1], LLAMA[2], loc=(0, 0, z),
              rot=(180, 0, 0), caras=20, canto=.02)
    ll.data.materials.append(mat("Llama", hexcol(COLOR_LLAMA), .30, .85))
    obs.append(ll)

    nu = cono("LlamaNucleo", NUCLEO[0], NUCLEO[1], NUCLEO[2],
              loc=(0, 0, z - LLAMA[2] * .30), rot=(180, 0, 0), caras=16, canto=.015)
    nu.data.materials.append(mat("Nucleo", hexcol(COLOR_NUCLEO), .22, .95))
    obs.append(nu)

    girar(obs, INCLINA)
    encajar(obs)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

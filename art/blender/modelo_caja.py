"""Ficha de caja de madera - FrutiCity. Pieza especial (obstaculo).

Va girada en tres cuartos a proposito: de frente, un cubo se lee como un
cuadrado plano y pierde todo el volumen. Girada se ven dos caras y una
arista, que es lo que dice "esto es una caja".
"""
import os, sys, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_CUERPO = MADERA
COLOR_TABLA  = MADERA_OSCURA
COLOR_CLARO  = MADERA_CLARA
BRILLO       = 0.30       # la madera no es de charol
RUGOSIDAD    = 0.62

LADO    = 1.28
TABLA   = (1.26, .075, .21)     # ancho <= LADO, o asoma por las esquinas
TABLA_Z = 0.40                  # a que altura van las dos horizontales
CRUZ    = (.24, .075, 0.98)     # la tabla diagonal, dentro de la cara
CRUZ_A  = 34.0                  # grados de la diagonal
TAPA    = (1.36, 1.36, .14)     # la tapa SI vuela: es lo que la hace tapa

GIRO    = (0.0, 0.0, -26.0)     # tres cuartos
# ================================


def construir():
    empezar()
    cuerpo_m = mat("Madera", hexcol(COLOR_CUERPO), RUGOSIDAD, BRILLO)
    tabla_m  = mat("Tabla", hexcol(COLOR_TABLA), RUGOSIDAD + .08, BRILLO)
    claro_m  = mat("Clara", hexcol(COLOR_CLARO), RUGOSIDAD, BRILLO)

    obs = []
    c = caja("Caja", (LADO, LADO, LADO), canto=.06, seg=3)
    c.data.materials.append(cuerpo_m)
    obs.append(c)

    fuera = LADO / 2 + TABLA[1] / 2 - .01      # pegadas a la cara, sin flotar
    for k in range(4):
        for dz in (TABLA_Z, -TABLA_Z):
            t = caja("Tabla", TABLA, loc=(0, -fuera, dz), canto=.025)
            t.data.materials.append(tabla_m)
            girar([t], (0, 0, 90.0 * k))
            obs.append(t)
        d = caja("Cruz", CRUZ, loc=(0, -fuera, 0), rot=(0, CRUZ_A, 0), canto=.025)
        d.data.materials.append(claro_m)
        girar([d], (0, 0, 90.0 * k))
        obs.append(d)

    tp = caja("Tapa", TAPA, loc=(0, 0, LADO / 2 + TAPA[2] / 2 - .02), canto=.04)
    tp.data.materials.append(claro_m)
    obs.append(tp)

    girar(obs, GIRO)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

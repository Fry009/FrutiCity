"""Ficha de raiz - FrutiCity. Los zarcillos que sujetan una fruta.

Tampoco es una pieza: es una REJA que se dibuja encima de la fruta, asi que
lo que manda son los HUECOS. Un velo verde con una equis encima —que es lo
que habia— tapa la fruta y no explica nada.

DOS intentos descartados, los dos por el mismo motivo: la simetria.

1. Cuatro zarcillos de esquina a esquina cruzandose en el centro. Salia una
   equis verde enorme, o sea exactamente el glifo que se venia a sustituir.
2. Dos correas horizontales arriba y abajo con dos garfios a los lados.
   Salia una CARA SONRIENTE: los garfios de ojos, la correa de abajo de
   boca. Nada en la consola lo delataba; se vio mirando el PNG.

Lo que funciona es no repartir nada alrededor del centro. Los zarcillos
SUBEN desde el borde de abajo, que es de donde salen las raices de verdad,
con alturas todas distintas y rizo en la punta. La fruta se ve por arriba,
que es donde tiene la cara, y la casilla se lee como algo agarrado por el
pie en vez de como un icono.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_LENA  = "6B4A2A"     # la madera del pie
COLOR_BROTE = "6DB03A"     # la punta tierna
COLOR_HOJA  = "7CBF44"
RUGOSIDAD   = 0.62
BARNIZ      = 0.05

DELANTE  = 0.40            # cuanto se adelantan hacia camara

# (x del pie, altura, deriva lateral, rizo). Cinco, TODAS distintas: dos
# iguales enfrentadas y vuelve a salir una cara.
ZARCILLOS = [(-0.86, 1.34, -0.16, 0.26),
             (-0.44, 1.78, 0.20, -0.30),
             (-0.04, 1.12, -0.10, 0.22),
             (0.48, 1.94, 0.14, 0.34),
             (0.90, 1.50, 0.24, -0.24)]
PIE      = -0.98           # el borde de abajo de la casilla
GRUESO   = 0.115           # radio en el pie
PASOS    = 11

# (indice de zarcillo, altura relativa 0-1, lado, rotacion Z)
HOJAS = [(1, 0.60, 1, 38), (3, 0.46, -1, -34), (0, 0.70, -1, 128)]
LARGO_HOJA = 0.52

ENCARA = (0.0, 0.0, 0.0)
# ================================


def _zarcillo(x, alto, deriva, rizo):
    """Sube desde el pie, se va de lado y riza la punta hacia dentro."""
    pts = []
    for i in range(PASOS + 1):
        t = i / PASOS
        # la punta se curva mas que la base: t al cuadrado en la deriva
        px = x + deriva * t * t * 2.4 + rizo * (t ** 3) * 2.0
        pz = PIE + alto * t
        py = -DELANTE * math.sin(math.pi * t * 0.7)
        pts.append((px, py, pz))
    return pts


def construir():
    empezar()

    lena = mat("Lena", hexcol(COLOR_LENA), RUGOSIDAD, BARNIZ)
    # De madera abajo a brote verde arriba: es lo que dice que esto crece.
    degradado(lena, hexcol(COLOR_LENA), hexcol(COLOR_BROTE), 2, PIE, PIE + 1.7)
    poro(lena, escala=190.0, fuerza=0.24)
    verde = mat("HojaRaiz", hexcol(COLOR_HOJA), 0.48, 0.10)

    obs = []
    trazas = []
    for n, (x, alto, deriva, rizo) in enumerate(ZARCILLOS):
        pts = _zarcillo(x, alto, deriva, rizo)
        trazas.append(pts)
        c = cuerda("Zarcillo%d" % n, pts, GRUESO * (0.78 + 0.10 * (n % 3)))
        c.data.materials.append(lena)
        obs.append(c)

    for i, (cual, altura, lado, giro) in enumerate(HOJAS):
        pts = trazas[cual]
        p = pts[int(altura * PASOS)]
        # rot X a 88 deja la hoja de cara a la camara; tumbada salia una
        # elipse plana que parecia un ojo.
        # El giro va en Y, NO en Z. Con Euler XYZ la matriz es Rz*Ry*Rx: la X
        # mete la hoja en el plano de la camara y la Y la gira DENTRO de ese
        # plano, mientras que la Z la saca de canto. Con el giro en Z las tres
        # hojas salian como elipses finas, y dos de ellas parecian ojos.
        lf = hoja_puesta(verde, (p[0], p[1] - 0.12, p[2]),
                         (88, giro, 0), largo=LARGO_HOJA, ancho=0.135,
                         grosor=0.024, nombre="Hojita%d" % i)
        comun._nace(lf)
        obs.append(lf)

    girar(obs, ENCARA)
    encajar(obs)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

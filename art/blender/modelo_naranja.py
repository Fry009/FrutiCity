"""Ficha de naranja - FrutiCity. Estilo Royal Match.
Es la hermana facil de la manzana: mismo cuerpo de revolucion, pero mas
achatada (mas ancha que alta), sin lobulos y con la piel picada.
El poro va por bump, no por geometria: a 128 px el relieve real no se ve.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_PIEL   = "FF8C1A"   # naranja saturado, no amarillo
COLOR_HOJA   = "4FA83A"
COLOR_CALIZ  = "3E8E2E"   # la estrellita verde de arriba
BRILLO       = 0.65       # menos barniz que la manzana: la piel es mate
RUGOSIDAD    = 0.44

REDONDEZ     = 0.94       # casi esfera
ALTO         = 0.76       # achatada: ancho > alto
ANCHO        = 0.88
HOYUELO      = 0.11
HOYUELO_CULO = 0.09
HOYUELO_ANCHO= 0.34

PORO_ESCALA  = 170.0
PORO_FUERZA  = 0.13
# ================================

PASOS, SEG = 40, 64


def perfil():
    pts = []
    for i in range(PASOS + 1):
        phi = math.pi * i / PASOS
        r = math.sin(phi) ** REDONDEZ
        z = math.cos(phi) * ALTO
        caida = math.exp(-(r / HOYUELO_ANCHO) ** 2)
        z -= caida * (HOYUELO if z >= 0 else -HOYUELO_CULO)
        pts.append((r, z))
    return pts


def caliz(material, z):
    """Estrella verde de 5 puntas en el hoyuelo. Un cono muy chato con
    pocas caras lee a caliz sin gastar geometria."""
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=.185, radius2=.055,
                                    depth=.075, location=(0, 0, z))
    ob = bpy.context.object; ob.name = "Caliz"
    ob.rotation_euler = (0, 0, math.radians(18))
    ob.data.materials.append(material)
    suave(ob, 1)
    return comun._nace(ob)      # que cuente para medir y encuadrar


def construir():
    empezar()
    ob = revolucion(perfil(), ANCHO, SEG, "Naranja")
    piel = mat("Piel", hexcol(COLOR_PIEL), RUGOSIDAD, BRILLO)
    poro(piel, PORO_ESCALA, PORO_FUERZA)
    ob.data.materials.append(piel)
    suave(ob, 2)

    suelo = ALTO - HOYUELO
    caliz(mat("Caliz", hexcol(COLOR_CALIZ), .60, .20), suelo + .03)

    hoja_puesta(mat("Hoja", hexcol(COLOR_HOJA), .50, .30),
                loc=(.05, -.06, suelo + .05), rot=(90, -34, 16),
                largo=.50, ancho=.150)

    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return ob


if __name__ == "__main__":
    construir()

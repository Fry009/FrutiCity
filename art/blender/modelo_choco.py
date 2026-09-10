"""Ficha de chocolate - FrutiCity. La costra pegajosa de dos capas.

Este SI tapa la fruta: el motor ni siquiera la recoge cuando la casilla lleva
chocolate, asi que la costra puede ser opaca. Lo que tiene que decir es "esto
esta pringado y hay que picarlo dos veces".

Primer intento, ya descartado: una caja redondeada con esferas pegadas
alrededor a modo de goterones, y una elipse clara encima haciendo de brillo.
Salia un dado marron con pompones y una pegatina de mango en la cara. Los
goterones eran objetos SUELTOS, y se notaba el corte donde tocaban la caja.

Ahora es UNA sola masa: un contorno cerrado cuyo radio ondula con dos senos
de periodos distintos, extruido y biselado a saco. Los goterones son parte
de la silueta, no piezas pegadas, asi que no hay costura que delate el
truco. El brillo se deja al material (rugosidad baja y barniz alto), que es
como brilla algo pringoso de verdad; pintarlo como un objeto claro lo
convertia en un adhesivo.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_OSCURO = "3A1D12"      # el fondo de la costra
COLOR_CLARO  = "8A4C28"      # lo que pilla la luz
RUGOSIDAD    = 0.20          # pringoso = brillante
BARNIZ       = 0.85

RADIO   = 0.86
GRUESO  = 0.44
CANTO   = 0.15               # bisel gordo: la masa no tiene aristas

# Ondulacion del contorno: dos senos de periodos primos entre si para que no
# se repita el patron y no se lea como una flor.
LOBULOS_A, FUERZA_A, FASE_A = 3, 0.150, 0.7
LOBULOS_B, FUERZA_B, FASE_B = 7, 0.075, 2.1
# Tres goterones concretos, mas hondos que la ondulacion de fondo
GOTERONES = [(0.9, 0.20), (2.6, 0.16), (4.4, 0.13)]
ANCHO_GOTA = 0.42            # radianes de ancho de cada goteron

PUNTOS = 96

# Se monta plano mirando a +Z y se gira para encarar la camara, igual que el
# kiwi. Sin encarar sale un canto de 0.44 visto de lado.
ENCARA = (86.0, 0.0, 0.0)
# ================================


def contorno():
    pts = []
    for i in range(PUNTOS):
        a = 2.0 * math.pi * i / PUNTOS
        r = RADIO * (1.0
                     + FUERZA_A * math.sin(LOBULOS_A * a + FASE_A)
                     + FUERZA_B * math.sin(LOBULOS_B * a + FASE_B))
        for centro, hondo in GOTERONES:
            d = abs((a - centro + math.pi) % (2.0 * math.pi) - math.pi)
            if d < ANCHO_GOTA:
                r += RADIO * hondo * math.cos(d / ANCHO_GOTA * math.pi * 0.5) ** 2
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def construir():
    empezar()

    masa = mat("Choco", hexcol(COLOR_OSCURO), RUGOSIDAD, BARNIZ)
    degradado(masa, hexcol(COLOR_OSCURO), hexcol(COLOR_CLARO), 2, -GRUESO, GRUESO)
    poro(masa, escala=110.0, fuerza=0.14)

    costra = prisma(contorno(), GRUESO, "Choco", canto=CANTO, seg=3)
    costra.data.materials.append(masa)
    suave_auto(costra, 44.0)

    obs = [costra]
    girar(obs, ENCARA)
    encajar(obs)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

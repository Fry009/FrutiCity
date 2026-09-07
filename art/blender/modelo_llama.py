"""Ficha de llama - FrutiCity. El fueguito de la dinamita.

Una gota de revolucion con la punta estirada y lamida hacia un lado: una
llama simetrica se lee como una lagrima, y lo que la hace fuego es que la
punta se doble. El degradado va de rojo abajo a amarillo arriba, que es
como se ve una llama de verdad y como la pinta Royal Match.

Emisiva, porque el fuego es lo unico de la familia que da luz propia.
"""
import os, sys, importlib, math
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
BASE      = "E23C12"        # rojo del pie
PUNTA     = "FFDC53"        # amarillo de la punta
CORAZON   = "FFF3C4"
RUGOSIDAD = 0.30
BARNIZ    = 0.40
FUERZA_LUZ = 2.2

# Perfil (radio, altura) de abajo arriba. El ensanche esta al tercio bajo:
# subirlo convierte la llama en una cebolla.
PERFIL = [(0.00, -1.00), (0.30, -0.86), (0.46, -0.58), (0.50, -0.28),
          (0.44, 0.04), (0.32, 0.36), (0.18, 0.66), (0.07, 0.88), (0.00, 1.00)]
LADEO   = 14.0              # grados que se dobla la punta
CORAZON_ESCALA = 0.46

# Sin encarar: la revolucion crece en Z y la camara la mira de lado, que es
# justo el perfil de la llama. Tumbarla la convertia en una bola naranja.
ENCARA = (0.0, 0.0, 0.0)
# ================================


def _emisivo(m, color, fuerza):
    b = m.node_tree.nodes["Principled BSDF"]
    for nombre in ("Emission Color", "Emission"):
        if nombre in b.inputs:
            b.inputs[nombre].default_value = color
            break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = fuerza
    return m


def construir():
    empezar()
    fuera = mat("LlamaFuera", hexcol(PUNTA), RUGOSIDAD, BARNIZ)
    degradado(fuera, hexcol(BASE), hexcol(PUNTA), 2, -1.0, 0.7)
    _emisivo(fuera, hexcol("FF7A18"), FUERZA_LUZ * 0.5)

    dentro = mat("LlamaCorazon", hexcol(CORAZON), 0.16, BARNIZ)
    _emisivo(dentro, hexcol(CORAZON), FUERZA_LUZ)

    cuerpo = revolucion(PERFIL, 1.0, 48, "Llama")
    suave(cuerpo, 2)
    cuerpo.data.materials.append(fuera)

    # El corazon claro asoma por el pie: es lo que da la sensacion de que la
    # llama esta hueca y no es un cono pintado.
    corazon = revolucion([(r * CORAZON_ESCALA, z * 0.72 - 0.16) for r, z in PERFIL],
                         1.0, 40, "Corazon")
    suave(corazon, 2)
    corazon.data.materials.append(dentro)

    obs = [cuerpo, corazon]
    girar([cuerpo], (0.0, LADEO, 0.0))
    girar(obs, ENCARA)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

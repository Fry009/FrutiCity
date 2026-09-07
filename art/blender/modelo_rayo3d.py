"""Ficha de rayo 3D - FrutiCity. Efecto de la bola de luz.

El rayo de la pieza 8 (energia) es un simbolo plano: sirve como icono en
una casilla, pero no como chispa volando por el tablero. Este es un rayo
con cuerpo: un tubo quebrado que se estrecha hacia la punta, con nucleo
blanco emisivo y funda violeta.

Se estrecha de verdad (el radio baja punto a punto) porque un tubo de
grosor constante se lee como un cable doblado, no como electricidad.
"""
import os, sys, importlib, math
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *
import bpy

# ============ MANDOS ============
FUNDA      = "A869E8"       # el violeta de la bola de luz en el juego
NUCLEO     = "FFF4FF"
RUGOSIDAD  = 0.18
BARNIZ     = 0.55
FUERZA_LUZ = 2.6            # emision del nucleo

# Quiebros del rayo en el plano XZ, de arriba abajo. El zigzag es lo unico
# que separa un rayo de una barra.
QUIEBROS = [(-0.18, 1.00), (0.30, 0.42), (-0.10, 0.16),
            (0.22, -0.20), (-0.26, -0.52), (0.14, -1.00)]
RADIO_BASE = 0.155
RADIO_PUNTA = 0.045
FUNDA_EXTRA = 1.55          # cuanto mas gorda es la funda que el nucleo

ENCARA = (84.0, 0.0, -6.0)
# ================================


def _emisivo(m, color, fuerza):
    """Enciende el material. mat() no toca la emision, y sin ella el rayo
    sale gris oscuro sobre el tablero en vez de brillar."""
    b = m.node_tree.nodes["Principled BSDF"]
    for nombre in ("Emission Color", "Emission"):
        if nombre in b.inputs:
            b.inputs[nombre].default_value = color
            break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = fuerza
    return m


def _tubo(nombre, radio_base, radio_punta, material):
    """Tubo quebrado. Se construye punto a punto para poder afinar el radio
    a lo largo del recorrido, que es lo que le da la punta."""
    datos = bpy.data.curves.new(nombre, 'CURVE')
    datos.dimensions = '3D'
    datos.resolution_u = 4
    datos.bevel_depth = radio_base
    datos.bevel_resolution = 5
    datos.use_fill_caps = True
    linea = datos.splines.new('POLY')
    linea.points.add(len(QUIEBROS) - 1)
    for i, (x, z) in enumerate(QUIEBROS):
        avance = i / float(len(QUIEBROS) - 1)
        # Plano XY, como el contorno de la pieza de energia: la camara mira
        # desde -Y, asi que un rayo montado en XZ se ve de punta (era un tubo).
        linea.points[i].co = (x, z, 0.0, 1.0)
        # radius es un factor sobre bevel_depth: 1 en la base, casi nada al final
        linea.points[i].radius = 1.0 - avance * (1.0 - radio_punta / radio_base)
    ob = bpy.data.objects.new(nombre, datos)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(material)
    # En --background bpy.ops no deja los objetos en scene.collection, y este
    # no pasa por bpy.ops: se registra a mano o no lo mide nadie.
    return comun._nace(ob)


def construir():
    empezar()
    funda = mat("RayoFunda", hexcol(FUNDA), RUGOSIDAD, BARNIZ)
    _emisivo(funda, hexcol(FUNDA), FUERZA_LUZ * 0.35)
    nucleo = mat("RayoNucleo", hexcol(NUCLEO), 0.10, BARNIZ)
    _emisivo(nucleo, hexcol(NUCLEO), FUERZA_LUZ)

    obs = [
        _tubo("RayoFunda", RADIO_BASE * FUNDA_EXTRA, RADIO_PUNTA * FUNDA_EXTRA, funda),
        _tubo("RayoNucleo", RADIO_BASE, RADIO_PUNTA, nucleo),
    ]
    girar(obs, ENCARA)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

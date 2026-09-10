"""Ficha de hielo - FrutiCity. El bloque que sujeta una fruta.

No es una pieza del tablero: es una TAPA que se dibuja encima de la fruta,
asi que lo importante no es la silueta sino el alfa. El centro tiene que
dejar ver la fruta apagada de debajo y el canto tiene que ser opaco, que es
lo que hace que se lea como un cristal grueso y no como un filtro azul.

El alfa va por Layer Weight: a contraluz (Facing bajo, o sea el borde del
volumen visto de canto) opaco, y de frente translucido. Es el mismo truco
que usa cualquier cristal de juego casual, y es lo unico que separa "hielo"
de "cuadrado azul".

Trampa: en Cycles el alfa del Principled SI sale al PNG con
film_transparent. Lo que no sirve aqui es Transmission: da refraccion, pero
el pixel queda opaco y el PNG sale como un bloque solido.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_HIELO  = "BFEBFF"      # el cuerpo
COLOR_CANTO  = "6FC4E8"      # el borde, mas saturado
COLOR_ESCARCHA = "F2FCFF"    # las lascas blancas de las esquinas
RUGOSIDAD    = 0.10          # el hielo es lo mas pulido de la familia
BARNIZ       = 0.85

ALFA_CENTRO  = 0.18          # cara delantera Y trasera suman: el centro real sube al ~33%
ALFA_CANTO   = 1.00
MEZCLA       = 0.42          # como de rapido pasa de translucido a opaco

LADO   = 1.78                # el bloque casi llena la casilla
FONDO  = 0.78
CANTO  = 0.26                # redondeo gordo: el hielo de juego no tiene aristas vivas

# Cuatro lascas, una por esquina, de tamanos distintos. Iguales se leen como
# un marco; desiguales, como un bloque roto a martillazos.
LASCAS = [(-0.66, -0.62, 0.30), (0.70, -0.54, 0.22),
          (-0.58, 0.68, 0.24), (0.62, 0.64, 0.33)]

ENCARA = (0.0, 0.0, 0.0)     # el bloque se mira de frente: no hay nada que girar
# ================================


def _alfa_por_canto(m, centro, canto, mezcla):
    """Opaco donde la superficie se ve de canto, translucido de frente."""
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    peso = nt.nodes.new("ShaderNodeLayerWeight")
    peso.inputs["Blend"].default_value = mezcla
    rampa = nt.nodes.new("ShaderNodeValToRGB")
    # Trampa pagada: Facing vale 0 MIRANDO DE FRENTE y 1 en el canto, no al
    # reves. Con los valores cambiados el bloque salio opaco por el medio y
    # translucido por el borde, o sea un cuadrado azul tapando la fruta, y no
    # dio ningun error: solo se ve midiendo el alfa del PNG.
    rampa.color_ramp.elements[0].position = 0.0
    rampa.color_ramp.elements[0].color = (centro, centro, centro, 1.0)
    rampa.color_ramp.elements[1].position = 1.0
    rampa.color_ramp.elements[1].color = (canto, canto, canto, 1.0)
    nt.links.new(peso.outputs["Facing"], rampa.inputs["Fac"])
    nt.links.new(rampa.outputs["Color"], b.inputs["Alpha"])
    return m


def construir():
    empezar()

    cristal = mat("Hielo", hexcol(COLOR_HIELO), RUGOSIDAD, BARNIZ)
    degradado(cristal, hexcol(COLOR_CANTO), hexcol(COLOR_HIELO), 2, -1.0, 1.0)
    _alfa_por_canto(cristal, ALFA_CENTRO, ALFA_CANTO, MEZCLA)

    escarcha = mat("Escarcha", hexcol(COLOR_ESCARCHA), 0.26, 0.40)
    _alfa_por_canto(escarcha, 0.82, 1.0, 0.30)

    bloque = caja("Hielo", (LADO, FONDO, LADO), canto=CANTO, seg=3)
    bloque.data.materials.append(cristal)
    suave_auto(bloque, 34.0)

    obs = [bloque]
    for x, z, r in LASCAS:
        # caja() ya convierte a radianes: aqui van GRADOS.
        lasca = caja("Lasca", (r, FONDO * 0.62, r * 0.86),
                     loc=(x, -FONDO * 0.30, z), rot=(0, (38 * r * 10) % 45, 0),
                     canto=r * 0.24, seg=2)
        lasca.data.materials.append(escarcha)
        suave_auto(lasca, 34.0)
        obs.append(lasca)

    girar(obs, ENCARA)
    encajar(obs)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

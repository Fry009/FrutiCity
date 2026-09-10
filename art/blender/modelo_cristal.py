"""Ficha de cristal - FrutiCity. La llave morada que abre los capitulos.

Es la pieza mas importante de la barra, asi que no puede parecer una gema
generica: tiene que leerse como un CRISTAL, y un cristal se lee por sus
CARAS. Por eso va a seis lados y con sombreado plano, sin suavizar. En
cuanto se suaviza, las facetas desaparecen y queda una zanahoria morada.

Tres piezas apiladas y nada mas: punta de abajo, cuerpo y punta de arriba.
La de arriba es mas larga que la de abajo y el cuerpo va un pelin ladeado,
porque un cristal perfectamente simetrico se lee como un icono y no como un
mineral.

Brilla desde dentro. Es emisivo ademas de barnizado: lo que hace que una
gema parezca cara no es el reflejo, es que parezca que tiene luz propia.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_CRISTAL = "C42BC4"     # el morado del cuerpo
COLOR_CANTO   = "8A1BA0"     # mas oscuro, para el degradado de abajo
COLOR_LUZ     = "E86BF5"     # el brillo de dentro
RUGOSIDAD     = 0.08         # lo mas pulido de toda la familia
BARNIZ        = 1.00
FUERZA_LUZ    = 0.85         # luz propia, sin pasarse: no es una llama

CARAS   = 6                  # seis lados. Mas caras = menos cristal.
RADIO   = 0.46
CUERPO  = 1.15               # alto del tronco
PUNTA   = 0.95               # alto de la punta de arriba
PIE     = 0.62               # alto de la punta de abajo, mas corta a proposito
LADEO   = 5.0                # grados de inclinacion del conjunto

# El alma: una copia encogida por dentro, mas clara y mas emisiva. Es lo que
# da la sensacion de que el cristal tiene FONDO y no es una carcasa pintada.
ALMA    = 0.52
ALFA_CENTRO = 0.72          # cuanto se ve el alma a traves del cuerpo

ENCARA = (0.0, 0.0, 0.0)     # se mira de frente; la revolucion crece en Z
# ================================


def _alfa_por_canto(m, centro, canto, mezcla=0.35):
    """Opaco en el canto y algo translucido de frente, igual que el hielo.

    Sin esto el cuerpo tapa por completo el alma y el alma es GEOMETRIA MUERTA:
    se modela, se renderiza y no se ve un solo pixel de ella. Y lo que hace que
    una gema parezca cara no es el reflejo, es que se le vea el fondo.

    Trampa ya pagada en el hielo: Facing vale 0 MIRANDO DE FRENTE y 1 en el
    canto, no al reves.
    """
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    peso = nt.nodes.new("ShaderNodeLayerWeight")
    peso.inputs["Blend"].default_value = mezcla
    rampa = nt.nodes.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].position = 0.0
    rampa.color_ramp.elements[0].color = (centro, centro, centro, 1.0)
    rampa.color_ramp.elements[1].position = 1.0
    rampa.color_ramp.elements[1].color = (canto, canto, canto, 1.0)
    nt.links.new(peso.outputs["Facing"], rampa.inputs["Fac"])
    nt.links.new(rampa.outputs["Color"], b.inputs["Alpha"])
    return m


def _emisivo(m, color, fuerza):
    b = m.node_tree.nodes["Principled BSDF"]
    for nombre in ("Emission Color", "Emission"):
        if nombre in b.inputs:
            b.inputs[nombre].default_value = color
            break
    if "Emission Strength" in b.inputs:
        b.inputs["Emission Strength"].default_value = fuerza
    return m


def _pieza(nombre, r1, r2, alto, z, material, caras=CARAS):
    """Un tronco de cono de pocas caras, SIN suavizar y SIN biselar: las
    aristas vivas son justo lo que hace que se lea como cristal."""
    ob = cono(nombre, r1, r2, alto, loc=(0, 0, z), caras=caras, canto=0)
    # cono() llama a suave_auto, que redondea el sombreado. Aqui hay que
    # deshacerlo: con las normales suavizadas las seis caras se funden en una
    # superficie continua y el mineral se convierte en un globo.
    for cara in ob.data.polygons: cara.use_smooth = False
    ob.data.materials.append(material)
    return ob


def construir():
    empezar()

    cuerpo_mat = mat("Cristal", hexcol(COLOR_CRISTAL), RUGOSIDAD, BARNIZ)
    degradado(cuerpo_mat, hexcol(COLOR_CANTO), hexcol(COLOR_CRISTAL), 2, -1.2, 1.2)
    _emisivo(cuerpo_mat, hexcol(COLOR_CRISTAL), FUERZA_LUZ * 0.35)
    # El cuerpo deja pasar algo de luz por el centro para que se vea el alma.
    # 0.72 y no menos: por debajo se convierte en un cristal de ventana y pierde
    # el color, que es justo lo que lo hace reconocible en la barra a 64 px.
    _alfa_por_canto(cuerpo_mat, ALFA_CENTRO, 1.0)

    alma_mat = mat("CristalAlma", hexcol(COLOR_LUZ), 0.05, 1.0)
    _emisivo(alma_mat, hexcol(COLOR_LUZ), FUERZA_LUZ)

    medio = CUERPO * 0.5
    obs = [
        _pieza("Pie",    0.0,   RADIO, PIE,    -medio - PIE * 0.5,    cuerpo_mat),
        _pieza("Cuerpo", RADIO, RADIO, CUERPO, 0.0,                   cuerpo_mat),
        _pieza("Punta",  RADIO, 0.0,   PUNTA,  medio + PUNTA * 0.5,   cuerpo_mat),
    ]

    # El alma repite la silueta a menor escala, por dentro del cuerpo.
    alma = [
        _pieza("AlmaPie",    0.0,          RADIO * ALMA, PIE * ALMA,    -medio - PIE * 0.5, alma_mat),
        _pieza("AlmaCuerpo", RADIO * ALMA, RADIO * ALMA, CUERPO,        0.0,                alma_mat),
        _pieza("AlmaPunta",  RADIO * ALMA, 0.0,          PUNTA * ALMA,  medio + PUNTA * 0.4, alma_mat),
    ]
    obs += alma

    girar(obs, (0.0, LADEO, 0.0))
    girar(obs, ENCARA)
    encajar(obs)
    terminar()
    return obs


if __name__ == "__main__":
    construir()

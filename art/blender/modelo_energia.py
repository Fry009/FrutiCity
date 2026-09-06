"""Ficha de energia (rayo) - FrutiCity. Pieza especial.

El contorno del rayo es el mismo que usa FruitModels.cs, para que la
pieza 3D y la pieza por codigo sean reconocibles como la misma cosa.
"""
import os, sys, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR      = ORO
COLOR_ALMA = ORO_CLARO
BRILLO     = 0.70
RUGOSIDAD  = 0.24

ESCALA  = 0.94
ANCHA   = 1.20      # el rayo original es muy estrecho para un tile cuadrado
GRUESO  = 0.30
CANTO   = 0.055     # el bisel hace de borde: cuanto mas gordo, mas marco
UMBRAL  = 0.80      # que parte del canto va en oro oscuro

# el rayo, tal cual esta en FruitModels.Energy()
RAYO = [(.18, 1.0), (-.62, .04), (-.10, .04),
        (-.28, -1.0), (.62, -.02), (.06, -.02)]

ENCARA = (84.0, 0.0, -5.0)
# ================================


def contorno():
    return [(x * ESCALA * ANCHA, y * ESCALA) for x, y in RAYO]


def construir():
    empezar()
    # Una sola pieza con el color por cara, no dos prismas encajados: el
    # contorno del rayo no esta centrado en el origen, asi que escalarlo
    # para hacer un alma mas pequena deja el borde gordo por un lado y
    # nulo por el otro. Por cara, el borde sale igual en todo el perimetro.
    ob = prisma(contorno(), GRUESO, "Rayo", CANTO, 3)
    ob.data.materials.append(mat("OroClaro", hexcol(COLOR_ALMA), RUGOSIDAD, BRILLO))
    ob.data.materials.append(mat("Oro", hexcol(COLOR), RUGOSIDAD + .04, BRILLO))
    for p in ob.data.polygons:
        p.material_index = 0 if abs(p.normal.z) > UMBRAL else 1

    obs = [ob]
    girar(obs, ENCARA)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return obs


if __name__ == "__main__":
    construir()

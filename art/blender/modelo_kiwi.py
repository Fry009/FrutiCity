"""Ficha de kiwi - FrutiCity. Estilo Royal Match.
A proposito NO es un kiwi entero: un ovalo marron no se distingue de una
patata a 128 px. Va en corte, que es lo que hacen los match-3 y lo que
hace la pieza reconocible de un vistazo.

Se monta plano (el corte mirando a +Z, comodo de calcular) y al final se
gira el grupo entero para encarar la camara.
"""
import os, sys, math, importlib
_f = globals().get("__file__")
AQUI = os.path.dirname(os.path.abspath(_f)) if _f else \
    r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun; importlib.reload(comun)
from comun import *

# ============ MANDOS ============
COLOR_CARNE   = "8FC13F"   # verde kiwi
COLOR_CORTEZA = "8A6440"   # marron peludo
COLOR_CORAZON = "F4F1D8"   # el centro cremoso
COLOR_PEPITA  = "241C14"
BRILLO        = 0.55       # la carne brilla, la corteza no
UMBRAL        = 0.80       # que parte del canto va en corteza (mas alto = mas anillo)

RADIO   = 0.86
GRUESO  = 0.19     # SEMIgrosor del disco
CANTO   = 0.20     # redondeo del borde
BOMBA   = 0.045    # cuanto se abomba la cara del corte

CORAZON = 0.23     # radio del centro cremoso
PEPITAS = 16
ANILLO  = 0.36     # a que radio va la corona de pepitas
PEPITA  = (.030, .046, .013)

ENCARA  = (84.0, 0.0, -8.0)   # giro final para mirar a camara
# ================================

N, M, SEG = 12, 10, 64


def perfil():
    """Del centro de la cara delantera, por el canto redondo, hasta la
    trasera. Un solo recorrido continuo: eso lo hace de revolucion."""
    pts = []
    for i in range(N + 1):                      # cara delantera abombada
        u = i / N
        pts.append(((RADIO - CANTO) * u, GRUESO + BOMBA * (1.0 - u * u)))
    for i in range(1, 2 * M):                   # canto
        a = math.pi * i / (2.0 * M)
        pts.append((RADIO - CANTO + CANTO * math.sin(a), GRUESO * math.cos(a)))
    for i in range(N + 1):                      # cara trasera
        u = 1.0 - i / N
        pts.append(((RADIO - CANTO) * u, -GRUESO - BOMBA * (1.0 - u * u)))
    return pts


def cara_z(r):
    """Altura de la cara del corte a una distancia r del eje."""
    u = min(1.0, r / (RADIO - CANTO))
    return GRUESO + BOMBA * (1.0 - u * u)


def construir():
    empezar()
    ob = revolucion(perfil(), 1.0, SEG, "Kiwi")

    carne = mat("Carne", hexcol(COLOR_CARNE), .38, BRILLO)
    corteza = mat("Corteza", hexcol(COLOR_CORTEZA), .88)
    poro(corteza, 260.0, 0.22)
    ob.data.materials.append(carne)      # indice 0
    ob.data.materials.append(corteza)    # indice 1
    # el canto son las caras cuya normal apenas mira al eje Z
    for p in ob.data.polygons:
        p.material_index = 0 if abs(p.normal.z) > UMBRAL else 1
    suave(ob, 2)

    obs = [ob]

    c = esfera("Corazon", 1.0, (0, 0, cara_z(0) - .010),
               (CORAZON, CORAZON, .045), 32, 12)
    c.data.materials.append(mat("Corazon", hexcol(COLOR_CORAZON), .45, .35))
    suave(c, 0)
    obs.append(c)

    pep = mat("Pepita", hexcol(COLOR_PEPITA), .30, .60)
    for k in range(PEPITAS):
        th = 2 * math.pi * k / PEPITAS + math.radians(11)
        x, y = ANILLO * math.cos(th), ANILLO * math.sin(th)
        e = esfera("Pepita", 1.0, (x, y, cara_z(ANILLO) - .004), PEPITA, 12, 8)
        e.rotation_euler = (0, 0, th)     # tumbadas siguiendo la corona
        e.data.materials.append(pep)
        suave(e, 0)
        obs.append(e)

    girar(obs, ENCARA)
    terminar()          # sin argumentos: mide TODA la pieza, accesorios incluidos
    return ob


if __name__ == "__main__":
    construir()

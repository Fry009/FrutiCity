"""Las caras de Fresita, dibujadas como sprites con alfa.

Ojos, cejas y boca dejan de ser geometria y pasan a ser un PNG que se pega
sobre la cara. Se gana lo que en 3D costaba una barbaridad: cambiar de
expresion es cambiar de imagen, y las caras valen igual para el tablero
del juego que para el modelo.

El lienzo cubre la zona facial de la cabeza. Coordenadas en fraccion de
lienzo (0..1), con el origen ABAJO a la izquierda (se voltea al guardar),
para que casen con el mapa UV del calco en fresita_sheet.py:

    u = 0 .. 1   ->  yaw -55 .. +55 grados alrededor de la cabeza
    v = 0 .. 1   ->  z 0.95 .. 1.34

Se dibuja a 4x y se reduce: PIL no tiene antialias en las primitivas, y a
tamano final los bordes salen como una sierra.

Uso:
    python caras_fresita.py            # las saca todas en fresita_v5/caras/
"""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import math

HERE = Path(__file__).resolve().parent
OUT = HERE / 'fresita_v5' / 'caras'
LADO = 512
SS = 4                      # supersampling

# --- paleta (la del muestrario de la hoja) -----------------------------
BLANCO  = (255, 252, 250, 255)
IRIS    = (139, 154, 108, 255)
IRIS_DK = (86, 100, 64, 255)
PUPILA  = (26, 20, 16, 255)
LINEA   = (38, 24, 18, 255)     # pestañas y contorno
CEJA    = (74, 42, 30, 255)
BOCA_IN = (74, 18, 24, 255)
LABIO   = (122, 28, 40, 255)     # oscuro: sobre piel roja el rosa no se ve
DIENTE  = (255, 250, 246, 255)
LENGUA  = (240, 112, 140, 255)

# --- geometria de la cara en el lienzo ---------------------------------
OJO_X, OJO_Y = 0.295, 0.545       # centro del ojo izquierdo (u, v)
OJO_RX, OJO_RY = 0.115, 0.140
BOCA_Y = 0.150


def _px(d, x, y):
    """De fraccion de lienzo a pixeles, con el origen abajo."""
    N = LADO * SS
    return (x * N, (1.0 - y) * N)


def _elipse(d, cx, cy, rx, ry, color, giro=0.0):
    N = LADO * SS
    if abs(giro) < 1e-6:
        x0, y0 = _px(d, cx - rx, cy + ry)
        x1, y1 = _px(d, cx + rx, cy - ry)
        d.ellipse([x0, y0, x1, y1], fill=color)
        return
    pts = []
    for i in range(64):
        a = 2 * math.pi * i / 64
        ex, ey = rx * math.cos(a), ry * math.sin(a)
        g = math.radians(giro)
        rxp = ex * math.cos(g) - ey * math.sin(g)
        ryp = ex * math.sin(g) + ey * math.cos(g)
        pts.append(_px(d, cx + rxp, cy + ryp))
    d.polygon(pts, fill=color)


def _trazo(d, puntos, grosor, color, punta_fina=True):
    """Una linea de grosor variable: circulos a lo largo del recorrido.
    Con d.line() el grosor es constante y todo acaba en topes romos."""
    n = len(puntos)
    N = LADO * SS
    for i, (x, y) in enumerate(puntos):
        t = i / max(1, n - 1)
        k = math.sin(math.pi * t) ** 0.45 if punta_fina else 1.0
        r = grosor * (0.18 + 0.82 * k) * N / 2
        px, py = _px(d, x, y)
        d.ellipse([px - r, py - r, px + r, py + r], fill=color)


def _arco(cx, cy, rx, ry, a0, a1, pasos=80):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / pasos)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / pasos)))
            for i in range(pasos + 1)]


# ============ piezas ====================================================

def ojo(d, sgn, forma, mirada=(0.0, 0.0)):
    """sgn -1 = ojo de la izquierda del lienzo. forma: abierto, feliz,
    cerrado, grande, entornado."""
    cx = OJO_X if sgn < 0 else 1 - OJO_X
    cy = OJO_Y
    rx, ry = OJO_RX, OJO_RY

    if forma in ("feliz", "cerrado"):
        # ojo curvado hacia arriba, el ^_^ de toda la vida. Arco abierto y
        # poco hondo: si se cierra mucho parece un ojo triste del reves.
        alto = 0.062 if forma == "feliz" else 0.034
        pts = _arco(cx, cy - alto * 0.45, rx * 1.00, alto, 8, 172, pasos=60)
        _trazo(d, pts, 0.044, LINEA, punta_fina=True)
        if forma == "feliz":
            fuera = -1 if cx < 0.5 else 1
            base = pts[0] if fuera < 0 else pts[-1]
            for ang, largo in ((28, 0.052), (52, 0.050)):
                a = math.radians(ang)
                _trazo(d, [(base[0] + fuera * largo * math.cos(a) * t / 5,
                            base[1] + largo * math.sin(a) * t / 5)
                           for t in range(6)], 0.022, LINEA)
        return

    if forma == "grande":
        rx, ry = rx * 1.06, ry * 1.16
    elif forma == "entornado":
        ry = ry * 0.74

    # linea de pestañas: un ovalo oscuro un pelin mayor y subido, tapado
    # despues por el blanco. Solo asoma la banda de arriba.
    _elipse(d, cx, cy + 0.020, rx + 0.016, ry + 0.016, LINEA)
    _elipse(d, cx, cy, rx, ry, BLANCO)

    mx, my = mirada
    ix, iy = cx + mx * rx * 0.30, cy - 0.012 + my * ry * 0.30
    irx = rx * 0.60 if forma != "grande" else rx * 0.52
    iry = ry * 0.52 if forma != "grande" else ry * 0.46
    _elipse(d, ix, iy, irx, iry, IRIS_DK)
    _elipse(d, ix, iy + iry * 0.10, irx * 0.90, iry * 0.86, IRIS)
    _elipse(d, ix, iy, irx * 0.52, iry * 0.56, PUPILA)
    _elipse(d, ix - irx * 0.40, iy + iry * 0.44, irx * 0.30, iry * 0.28, BLANCO)
    _elipse(d, ix + irx * 0.42, iy - iry * 0.46, irx * 0.16, iry * 0.15, BLANCO)

    # tres pestañas en el angulo de fuera
    fuera = -1 if cx < 0.5 else 1
    for i, (ang, largo) in enumerate(((18, 0.070), (36, 0.080), (56, 0.066))):
        a = math.radians(ang)
        x0 = cx + fuera * rx * 0.86
        y0 = cy + ry * 0.34 + i * 0.012
        _trazo(d, [(x0 + fuera * largo * math.cos(a) * t / 6,
                    y0 + largo * math.sin(a) * t / 6) for t in range(7)],
               0.026, LINEA)


def ceja(d, sgn, forma):
    cx = OJO_X if sgn < 0 else 1 - OJO_X
    fuera = -1 if sgn < 0 else 1
    alto = {"normal": 0.762, "alta": 0.812, "caida": 0.752, "enfado": 0.736}[forma]
    arqueo = {"normal": 0.030, "alta": 0.040, "caida": 0.020, "enfado": 0.018}[forma]
    # inclinacion: negativa = extremo de fuera hacia abajo (pena)
    incl = {"normal": -0.018, "alta": -0.010, "caida": -0.052, "enfado": 0.046}[forma]
    pts = []
    for i in range(21):
        t = i / 20.0
        x = cx + fuera * (t - 0.5) * 0.200
        y = alto + arqueo * math.sin(math.pi * t) + incl * (t - 0.5) * 2 * (
            1 if fuera > 0 else 1)
        pts.append((x, y))
    _trazo(d, pts, 0.038, CEJA)


def boca(d, forma):
    cx, cy = 0.5, BOCA_Y

    if forma == "sonrisa":
        pts = _arco(cx, cy + 0.062, 0.168, 0.098, 200, 340)
        _trazo(d, pts, 0.064, LABIO)
        return

    if forma == "risa":                      # boca abierta, la de ALEGRE
        ancho, alto = 0.155, 0.105
        cont = _arco(cx, cy + 0.030, ancho, alto, 185, 355)
        tapa = [(x, cy + 0.030 + (0.012 * math.sin(math.pi * i / (len(cont) - 1))))
                for i, (x, _) in enumerate(cont)]
        d.polygon([_px(d, *p) for p in cont] + [_px(d, *p) for p in reversed(tapa)],
                  fill=BOCA_IN)
        # dientes pegados al labio de arriba
        dien = [(x, cy + 0.030 - 0.004) for x, _ in cont]
        dbaj = [(x, cy + 0.030 - 0.030 * math.sin(math.pi * i / (len(cont) - 1)) - 0.004)
                for i, (x, _) in enumerate(cont)]
        d.polygon([_px(d, *p) for p in dien] + [_px(d, *p) for p in reversed(dbaj)],
                  fill=DIENTE)
        _elipse(d, cx, cy - 0.048, 0.058, 0.030, LENGUA)
        _trazo(d, cont, 0.030, LABIO)
        _trazo(d, tapa, 0.022, LABIO)
        return

    if forma == "o":                         # sorpresa
        _elipse(d, cx, cy + 0.010, 0.062, 0.082, LABIO)
        _elipse(d, cx, cy + 0.010, 0.046, 0.066, BOCA_IN)
        _elipse(d, cx, cy - 0.040, 0.030, 0.018, LENGUA)
        return

    if forma == "triste":
        pts = _arco(cx, cy - 0.052, 0.126, 0.074, 20, 160)
        _trazo(d, pts, 0.048, LABIO)
        return

    if forma == "duda":                      # boquita pequeña hacia un lado
        pts = _arco(cx + 0.030, cy + 0.034, 0.080, 0.052, 205, 330)
        _trazo(d, pts, 0.044, LABIO)
        return

    raise ValueError("boca desconocida: " + forma)


# ============ expresiones ===============================================
# (ojo izquierdo, ojo derecho, ceja, boca, mirada)
EXPRESIONES = {
    "idle":       ("abierto", "abierto", "normal", "sonrisa", (0.0, 0.0)),
    "alegre":     ("feliz",   "feliz",   "alta",   "risa",    (0.0, 0.0)),
    "guino":      ("abierto", "cerrado", "alta",   "risa",    (0.0, 0.0)),
    "sorpresa":   ("grande",  "grande",  "alta",   "o",       (0.0, 0.05)),
    "triste":     ("entornado", "entornado", "caida", "triste", (0.0, -0.35)),
    "duda":       ("abierto", "entornado", "enfado", "duda",  (0.35, 0.20)),
}


# cada fruta con su color de ojo y de ceja; el resto de la cara es comun
PERSONAJES = {
    "fresi": dict(iris=(139, 154, 108), ceja=(74, 42, 30)),
    "pablo": dict(iris=(107, 74, 42), ceja=(74, 48, 24)),
    "nora":  dict(iris=(122, 82, 48), ceja=(74, 48, 24)),
}


def dibujar(nombre, quien=None):
    global IRIS, IRIS_DK, CEJA
    if quien:
        r, g, b = PERSONAJES[quien]["iris"]
        IRIS = (r, g, b, 255)
        IRIS_DK = (int(r * .62), int(g * .62), int(b * .62), 255)
        CEJA = PERSONAJES[quien]["ceja"] + (255,)
    ojo_i, ojo_d, cj, bc, mirada = EXPRESIONES[nombre]
    N = LADO * SS
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ceja(d, -1, cj)
    ceja(d, 1, cj)
    ojo(d, -1, ojo_i, mirada)
    ojo(d, 1, ojo_d, mirada)
    boca(d, bc)
    img = img.resize((LADO, LADO), Image.LANCZOS)
    return img


def todas(quien=None):
    carpeta = OUT / quien if quien else OUT
    carpeta.mkdir(parents=True, exist_ok=True)
    rutas = []
    for nombre in EXPRESIONES:
        img = dibujar(nombre, quien)
        r = carpeta / ("cara_%s.png" % nombre)
        img.save(r)
        rutas.append(r)
        print("[cara]", r)
    return rutas


if __name__ == "__main__":
    for quien in PERSONAJES:
        todas(quien)
    todas()
    # hoja de contacto para poder mirarlas juntas
    nombres = list(EXPRESIONES)
    ims = [Image.open(OUT / "fresi" / ("cara_%s.png" % n)) for n in nombres]
    cols, M = 3, 12
    filas = (len(ims) + cols - 1) // cols
    W = LADO * cols + M * (cols + 1)
    H = (LADO + 30) * filas + M * (filas + 1)
    hoja = Image.new('RGBA', (W, H), (232, 232, 236, 255))
    dr = ImageDraw.Draw(hoja)
    for i, (n, im) in enumerate(zip(nombres, ims)):
        cx = M + (i % cols) * (LADO + M)
        cy = M + (i // cols) * (LADO + 30 + M)
        hoja.alpha_composite(im, (cx, cy))
        dr.text((cx + LADO / 2 - dr.textlength(n.upper()) / 2, cy + LADO + 8),
                n.upper(), fill=(70, 70, 78, 255))
    hoja.convert('RGB').save(OUT / "caras_hoja.png", quality=95)
    print("[cara] hoja:", OUT / "caras_hoja.png")

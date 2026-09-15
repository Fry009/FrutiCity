# -*- coding: utf-8 -*-
"""LAS CARAS DE LOS FRUTIFRIENDS, como sprites.

POR QUE SPRITES Y NO GEOMETRIA
------------------------------
Los seis amigos de `Resources/FrutiFriends/` estan renderizados en Blender con
la cara MODELADA: ojos, cejas y boca son geometria. Eso les deja con una sola
expresion para siempre, y cambiarla es volver a Blender y volver a renderizar
los seis. Lo pidio Fran al reves: "ojos y boca sprites, super expresivas, asi
muestran emociones".

Con la cara en PNG, cambiar de emocion es cambiar de imagen. Y ademas se puede
hacer EN MEDIO de una partida: la fruta del nivel del jefe pasa de tranquila a
asustada segun se acerca el bicho, sin tocar ningun modelo.

Es la misma decision que ya se tomo con Fresita -ver art/blender/caras_fresita.py,
"ojos, cejas y boca dejan de ser geometria y pasan a ser un PNG"-, traida a los
munequitos, que son el canon.

DE DONDE SALE EL CUERPO
-----------------------
De `Resources/Fruti3D/`, que son LAS MISMAS FRUTAS SIN CARA: las fichas del
tablero. Estan renderizadas en Blender con las luces buenas, a 512, y no hay que
borrarle la cara a nadie ni volver a modelar. El cuerpo sigue siendo 3D de
verdad; lo unico dibujado es lo que tiene que cambiar.

EL ESTILO DE LOS BRAZOS
-----------------------
Palos negros con tres dedos de linea, como pidio Fran. Es el recurso de los
dibujos clasicos: un brazo sin volumen no compite con el cuerpo, se lee a
cualquier tamano y se puede doblar como se quiera sin que parezca roto. Aqui
ademas resuelve un problema real: un brazo con sombreado tendria que casar con
la luz del render de Blender, y un palo negro no tiene que casar con nada.

USO
---
    python tools/caras_fruti.py            # saca todo y una hoja de contacto

Escribe en `FrutiCity/Assets/FrutiCity/Resources/Fruti/`:
    cara_<expresion>.png   ojos + cejas + boca + colorete
    brazo_<pose>.png       un brazo, el izquierdo; el derecho se voltea
    pie.png                una zapatilla
    marca_<tipo>.png       la gota de sudor, la exclamacion, la interrogacion
"""

import os

from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECURSOS = os.path.join(RAIZ, 'FrutiCity', 'Assets', 'FrutiCity', 'Resources')
SALIDA = os.path.join(RECURSOS, 'Fruti')

# Se dibuja a x4 y se reduce: PIL no suaviza las primitivas y a tamano final los
# bordes salen como una sierra. Es la misma receta de caras_fresita.py.
LADO = 512
SS = 4
N = LADO * SS

NEGRO = (28, 24, 26, 255)
BLANCO = (255, 253, 250, 255)
CEJA = (74, 44, 32, 255)
BOCA_DENTRO = (150, 46, 60, 255)
LENGUA = (232, 116, 132, 255)
DIENTE = (255, 252, 246, 255)
COLORETE = (245, 140, 130, 90)


def _px(v):
    """De fraccion de lienzo (0..1) a pixel del lienzo grande."""
    return int(round(v * N))


def _elipse(d, cx, cy, rx, ry, color):
    d.ellipse([_px(cx - rx), _px(cy - ry), _px(cx + rx), _px(cy + ry)], fill=color)


def _trazo(d, puntos, grosor, color):
    """Una linea gruesa con las puntas redondeadas, que es lo que la hace trazo
    y no un rectangulo girado."""
    p = [(_px(x), _px(y)) for x, y in puntos]
    g = _px(grosor)
    d.line(p, fill=color, width=g, joint='curve')
    for x, y in p:
        d.ellipse([x - g // 2, y - g // 2, x + g // 2, y + g // 2], fill=color)


# ============ ojos ======================================================
# El ojo de estos munecos es una almendra grande y vertical, con la pupila
# enorme y DOS brillos: uno grande arriba a la izquierda y uno chico abajo a la
# derecha. Con un solo brillo el ojo se queda de peluche; con dos, mira.

def ojo(d, lado, forma, mirada=(0.0, 0.0)):
    cx = 0.5 + lado * 0.148
    cy = 0.455
    rx, ry = 0.093, 0.118

    if forma == 'cerrado':                      # una pestana curva hacia abajo
        _trazo(d, [(cx - rx, cy), (cx - rx * .4, cy + ry * .5),
                   (cx + rx * .4, cy + ry * .5), (cx + rx, cy)], 0.022, NEGRO)
        return
    if forma == 'feliz':                        # el arco de ojo contento, hacia arriba
        _trazo(d, [(cx - rx, cy + ry * .35), (cx - rx * .35, cy - ry * .45),
                   (cx + rx * .35, cy - ry * .45), (cx + rx, cy + ry * .35)], 0.026, NEGRO)
        return

    if forma == 'grande':
        rx, ry = rx * 1.16, ry * 1.20
    elif forma == 'entornado':
        ry *= .60

    _elipse(d, cx, cy, rx, ry, NEGRO)                       # el contorno oscuro
    _elipse(d, cx, cy, rx * .86, ry * .86, BLANCO)          # el blanco
    px = cx + mirada[0] * rx * .30
    py = cy + mirada[1] * ry * .30
    pr = ry * (.66 if forma != 'entornado' else .82)
    _elipse(d, px, py, pr * .78, pr, NEGRO)                 # la pupila
    _elipse(d, px - pr * .30, py - pr * .40, pr * .30, pr * .34, BLANCO)   # brillo grande
    _elipse(d, px + pr * .30, py + pr * .34, pr * .15, pr * .17, BLANCO)   # brillo chico


def ceja(d, lado, forma):
    cx = 0.5 + lado * 0.150
    cy = 0.300
    largo, grosor = 0.082, 0.026
    if forma == 'alta':
        cy -= 0.030
        _trazo(d, [(cx - largo, cy + .012), (cx, cy - .014), (cx + largo, cy + .012)], grosor, CEJA)
    elif forma == 'caida':                      # los extremos de fuera, hacia abajo
        _trazo(d, [(cx - lado * largo, cy - .012), (cx + lado * largo, cy + .028)], grosor, CEJA)
    elif forma == 'enfado':                     # los extremos de dentro, hacia abajo
        _trazo(d, [(cx - lado * largo, cy + .030), (cx + lado * largo, cy - .010)], grosor, CEJA)
    else:
        _trazo(d, [(cx - largo, cy + .008), (cx, cy - .006), (cx + largo, cy + .008)], grosor, CEJA)


# ============ bocas =====================================================

def boca(d, forma):
    cx, cy = 0.5, 0.640

    if forma == 'sonrisa':
        _trazo(d, [(cx - .072, cy - .014), (cx, cy + .030), (cx + .072, cy - .014)], 0.026, NEGRO)
        return
    if forma == 'risa':                         # abierta, con lengua: la de ALEGRE
        d.pieslice([_px(cx - .105), _px(cy - .085), _px(cx + .105), _px(cy + .115)],
                   start=0, end=180, fill=NEGRO)
        d.pieslice([_px(cx - .088), _px(cy - .066), _px(cx + .088), _px(cy + .096)],
                   start=0, end=180, fill=BOCA_DENTRO)
        _elipse(d, cx, cy + .052, .052, .034, LENGUA)
        return
    if forma == 'grito':                        # ovalo alto: el "SOCORRO"
        _elipse(d, cx, cy + .022, .070, .098, NEGRO)
        _elipse(d, cx, cy + .026, .054, .080, BOCA_DENTRO)
        _elipse(d, cx, cy + .062, .040, .030, LENGUA)
        # Los dos dientes de arriba, que es lo que lo separa de un agujero.
        d.rectangle([_px(cx - .040), _px(cy - .068), _px(cx + .040), _px(cy - .040)], fill=DIENTE)
        return
    if forma == 'o':                            # sorpresa: redonda y pequena
        _elipse(d, cx, cy + .014, .050, .056, NEGRO)
        _elipse(d, cx, cy + .016, .036, .042, BOCA_DENTRO)
        return
    if forma == 'triste':
        _trazo(d, [(cx - .066, cy + .030), (cx, cy - .012), (cx + .066, cy + .030)], 0.026, NEGRO)
        return
    if forma == 'duda':                         # ondulada, ni si ni no
        _trazo(d, [(cx - .072, cy + .014), (cx - .024, cy - .014),
                   (cx + .024, cy + .018), (cx + .072, cy - .010)], 0.024, NEGRO)
        return
    if forma == 'enfado':                       # apretada, con los dientes marcados
        d.pieslice([_px(cx - .092), _px(cy - .070), _px(cx + .092), _px(cy + .086)],
                   start=0, end=180, fill=NEGRO)
        d.rectangle([_px(cx - .070), _px(cy - .006), _px(cx + .070), _px(cy + .020)], fill=DIENTE)
        return
    raise ValueError('boca desconocida: ' + forma)


def colorete(d):
    _elipse(d, 0.5 - 0.235, 0.565, 0.062, 0.040, COLORETE)
    _elipse(d, 0.5 + 0.235, 0.565, 0.062, 0.040, COLORETE)


# (ojo izquierdo, ojo derecho, ceja, boca, mirada, colorete)
EXPRESIONES = {
    'idle':      ('abierto', 'abierto', 'normal',  'sonrisa', (0.0, 0.0),   True),
    'alegre':    ('feliz',   'feliz',   'alta',    'risa',    (0.0, 0.0),   True),
    'guino':     ('abierto', 'cerrado', 'alta',    'risa',    (0.0, 0.0),   True),
    'sorpresa':  ('grande',  'grande',  'alta',    'o',       (0.0, 0.05),  False),
    'susto':     ('grande',  'grande',  'alta',    'grito',   (0.0, 0.10),  False),
    'duda':      ('abierto', 'entornado', 'enfado', 'duda',   (0.35, 0.18), False),
    'enfado':    ('entornado', 'entornado', 'enfado', 'enfado', (0.0, .05), False),
    'triste':    ('entornado', 'entornado', 'caida', 'triste', (0.0, -0.32), False),
}


def cara(nombre):
    ojo_i, ojo_d, cj, bc, mirada, rubor = EXPRESIONES[nombre]
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rubor:
        colorete(d)
    ceja(d, -1, cj)
    ceja(d, 1, cj)
    ojo(d, -1, ojo_i, mirada)
    ojo(d, 1, ojo_d, mirada)
    boca(d, bc)
    return img.resize((LADO, LADO), Image.LANCZOS)


# ============ brazos, piernas y marcas ==================================

def brazo(pose):
    """El brazo izquierdo. El derecho es este volteado, asi que solo hay uno.

    Palo negro y tres dedos de linea, como pidio Fran. El lienzo es cuadrado y
    el hombro cae en la esquina de ARRIBA A LA DERECHA, que es por donde se pega
    al costado de la fruta: asi la interfaz solo tiene que decir donde esta el
    hombro y el brazo cuelga solo."""
    n = LADO * SS // 2
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    g = int(n * .085)

    def linea(pts, grosor=None):
        gg = grosor or g
        p = [(int(x * n), int(y * n)) for x, y in pts]
        d.line(p, fill=NEGRO, width=gg, joint='curve')
        for x, y in p:
            d.ellipse([x - gg // 2, y - gg // 2, x + gg // 2, y + gg // 2], fill=NEGRO)

    if pose == 'abajo':
        codo, mano = (0.52, 0.52), (0.42, 0.84)
    elif pose == 'arriba':                       # pidiendo socorro
        codo, mano = (0.46, 0.40), (0.30, 0.14)
    elif pose == 'saludo':
        codo, mano = (0.44, 0.44), (0.16, 0.30)
    else:
        raise ValueError('pose desconocida: ' + pose)

    linea([(0.94, 0.14), codo, mano])
    # Tres dedos, abiertos en abanico desde la mano.
    import math
    base = math.atan2(mano[1] - codo[1], mano[0] - codo[0])
    for k in (-0.46, 0.0, 0.46):
        a = base + k
        largo = n and 0.19
        linea([mano, (mano[0] + math.cos(a) * largo, mano[1] + math.sin(a) * largo)],
              grosor=int(g * .62))
    return img.resize((LADO // 2, LADO // 2), Image.LANCZOS)


def pie():
    n = LADO * SS // 3
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([int(n * .06), int(n * .34), int(n * .94), int(n * .86)], fill=(96, 62, 40, 255))
    d.ellipse([int(n * .12), int(n * .30), int(n * .88), int(n * .70)], fill=(132, 88, 56, 255))
    return img.resize((LADO // 3, LADO // 3), Image.LANCZOS)


def marca(tipo):
    """Las marcas de tebeo: gota de sudor, exclamacion e interrogacion. Son lo
    que deja decir 'esta agobiada' sin ninguna palabra."""
    n = LADO * SS // 3
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if tipo == 'sudor':
        azul, claro = (108, 186, 232, 255), (198, 234, 250, 255)
        d.polygon([(n * .50, n * .10), (n * .82, n * .62), (n * .50, n * .90), (n * .18, n * .62)],
                  fill=azul)
        d.ellipse([n * .34, n * .52, n * .66, n * .84], fill=azul)
        d.ellipse([n * .38, n * .52, n * .52, n * .68], fill=claro)
    elif tipo in ('exclamacion', 'interrogacion'):
        color = (246, 200, 62, 255) if tipo == 'exclamacion' else (170, 214, 250, 255)
        borde = (58, 44, 30, 255)
        if tipo == 'exclamacion':
            d.polygon([(n * .38, n * .08), (n * .62, n * .08), (n * .56, n * .60), (n * .44, n * .60)],
                      fill=color, outline=borde, width=int(n * .035))
            d.ellipse([n * .40, n * .70, n * .60, n * .90], fill=color, outline=borde, width=int(n * .035))
        else:
            d.arc([n * .28, n * .08, n * .72, n * .52], start=160, end=20, fill=color, width=int(n * .13))
            d.line([(n * .50, n * .42), (n * .50, n * .62)], fill=color, width=int(n * .13))
            d.ellipse([n * .41, n * .72, n * .59, n * .90], fill=color)
    else:
        raise ValueError('marca desconocida: ' + tipo)
    return img.resize((LADO // 3, LADO // 3), Image.LANCZOS)


# ============ donde va la cara en cada fruta ============================
# La cara es UNA por expresion y cada fruta la lleva a su sitio: repetirla seis
# veces serian cuarenta y ocho PNG que habria que rehacer enteros al tocar un
# ojo. Aqui va como DATO, y el juego usa esta misma tabla (ver FrutiChibi.cs).
#
# Los numeros salen de medir la caja de alfa de cada cuerpo y su franja mas
# ancha -donde de verdad cabe una cara-, no de moverlos hasta que quedaban bien:
#
#   manzana  412x475  franja mas ancha en y=0.557
#   naranja  457x457                      y=0.547
#   fresa    373x458                      y=0.281   <- es un cono: la cara va ALTA
#   kiwi     449x458                      y=0.469
#   uvas     375x445                      y=0.404
#   platano  455x338                      y=0.568   <- media luna: cara pequena y corrida
#
# (desplazamiento x, desplazamiento y, escala), en fraccion del lienzo.
CARA_EN = {
    'manzana': (0.000, -0.015, 0.94),
    'naranja': (0.000, -0.020, 1.00),
    'fresa':   (0.000, -0.130, 0.78),
    'kiwi':    (0.000, -0.045, 0.88),
    'uvas':    (0.005, -0.070, 0.80),
    'platano': (-0.030, 0.045, 0.60),
}


def poner_cara(cuerpo, cara_img, fruta, lado):
    """Compone cuerpo + cara ya colocada. Es lo mismo que hara el juego."""
    dx, dy, esc = CARA_EN[fruta]
    n = max(8, int(lado * esc))
    c = cara_img.resize((n, n), Image.LANCZOS)
    fondo = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    fondo.paste(c, (int((lado - n) / 2 + dx * lado), int((lado - n) / 2 + dy * lado)), c)
    return Image.alpha_composite(cuerpo, fondo)


# ============ hoja de contacto ==========================================

def contacto(destino):
    """Las ocho caras sobre los cuerpos de verdad, para poder JUZGARLAS. Mirar
    una cara sobre fondo transparente no dice nada: lo que hay que ver es si
    encaja en la fruta."""
    cuerpos = ['manzana', 'naranja', 'fresa', 'kiwi', 'uvas', 'platano']
    nombres = list(EXPRESIONES)
    celda = 200
    hoja = Image.new('RGB', (celda * len(nombres), celda * 2 + 26), (38, 42, 50))
    d = ImageDraw.Draw(hoja)
    for i, exp in enumerate(nombres):
        c = Image.open(os.path.join(SALIDA, 'cara_%s.png' % exp)).convert('RGBA')
        for fila in range(2):
            cuerpo = cuerpos[(i + fila * 3) % len(cuerpos)]
            b = Image.open(os.path.join(RECURSOS, 'Fruti3D', cuerpo + '.png')).convert('RGBA')
            b = b.resize((celda, celda), Image.LANCZOS)
            comp = poner_cara(b, c, cuerpo, celda)
            hoja.paste(comp, (i * celda, fila * celda + 26), comp)
        d.text((i * celda + 8, 6), exp, fill=(235, 235, 235))
    hoja.save(destino)


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    for nombre in EXPRESIONES:
        cara(nombre).save(os.path.join(SALIDA, 'cara_%s.png' % nombre))
    for pose in ('abajo', 'arriba', 'saludo'):
        brazo(pose).save(os.path.join(SALIDA, 'brazo_%s.png' % pose))
    pie().save(os.path.join(SALIDA, 'pie.png'))
    for tipo in ('sudor', 'exclamacion', 'interrogacion'):
        marca(tipo).save(os.path.join(SALIDA, 'marca_%s.png' % tipo))
    print('escritas %d caras, 3 brazos, 1 pie y 3 marcas en %s' % (len(EXPRESIONES), SALIDA))
    hoja = os.path.join(os.environ.get('TEMP', '.'), 'caras_contacto.png')
    contacto(hoja)
    print('hoja de contacto: ' + hoja)

# -*- coding: utf-8 -*-
"""El decorado del teatrillo del jefe: una calle de FrutiCity que se desplaza.

QUE ES ESTO
-----------
Una tira ANCHA y REPETIBLE. El dino anda por el escenario y el fondo corre por debajo:
eso es lo que convierte un bicho que se desliza por delante de una foto en un bicho que
RECORRE un sitio. La tira se pinta en un RawImage y lo que se mueve es su `uvRect`, asi
que hay que poder empalmarla consigo misma sin que se vea la juntura.

POR QUE SE ESPEJA
-----------------
La costura se resuelve espejando: la tira es `A + reverso(A)`. El borde derecho de A toca
su propio reverso, y el borde izquierdo de A toca el borde izquierdo del reverso; las dos
junturas empalman POR CONSTRUCCION, sin retocar un solo pixel. Cuadrar a mano una
panoramica de pueblo para que empalme era media tarde y quedaba peor.

EL ANCHO NO SE ELIGE: SE HEREDA
-------------------------------
A la banda se le manda la ALTURA (220) y se le obedece el ancho, que sale de la
proporcion del recorte. El primer intento estiraba la banda hasta un ancho redondo y
salia el pueblo al doble de tamano, con una sola casa comiendose el escenario entero.

LA CALLE VA EN SILUETA
----------------------
Las ilustraciones del pueblo salieron de un `image_gen` que ya no esta disponible: no se
pueden rehacer, solo RECOMPONER —la misma trampa que se pago con el mapa del viaje, y la
misma salida que tomo `merge_journey_art.py`—. Asi que las casas son un recorte, y lo que
hace falta y no existe —la parada de autobus, las farolas, el banco— se dibuja aqui.

Pero se dibuja en SILUETA OSCURA y no con la paleta de la interfaz. Se probo lo otro
—marquesina de teja verde, poste metalico, banco de madera— y quedaba pegado encima: el
fondo es pintura y la interfaz es plano, y los dos estilos no se mezclan a media
distancia. La silueta si, y ademas es lo que hacen los juegos de scroll lateral para
separar el primer plano del decorado.

USO
---
    python tools/escenario_jefe.py

Escribe `FrutiCity/Assets/FrutiCity/Resources/Art/boss_stage.png`. Mirar el PNG despues.
"""

import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTE = os.path.join(RAIZ, 'FrutiCity', 'Assets', 'FrutiCity', 'Resources', 'Art')
FUENTE = os.path.join(ARTE, 'bg_village.png')
SALIDA = os.path.join(ARTE, 'boss_stage.png')

# El escenario mide 500 x 110 pixeles de diseno; la tira se pinta a x2 porque el Canvas
# escala x2,26 en el Redmi.
ESCALA = 2
# EL ESCENARIO CRECE EN LOS MOVILES ALARGADOS. El diseno base le da 110 px de alto, pero un
# movil de 20:9 deja 120 px libres por arriba y el teatro se los queda: puede llegar a 226.
# La tira se pinta para el caso MAS ALTO y el juego ensena de ella la franja de abajo que le
# quepa (uvRect.height). Al reves -pintarla para 110 y estirarla- el pueblo salia aplastado
# al doble de alto en cuanto el teatro crecia.
ALTO_DISENO_MAX = 300
ALTO = ALTO_DISENO_MAX * ESCALA
# EL BORDE DE ABAJO NO SE MUEVE: es donde pisa el dino. Lo que se gana al crecer es CIELO,
# asi que la banda se estira hacia arriba desde el mismo pie de la ilustracion.
PIE_FUENTE = 902
ALTO_BANDA = 551   # lo mas alto que da la ilustracion sin salirse por arriba
BANDA_Y = PIE_FUENTE - ALTO_BANDA
# El ancho de la mitad se CLAVA en 1024, y la tira espejada mide 2048 justos. El limite de
# textura de Unity en movil y en escritorio es 2048: con un pixel mas la reescala ella, y al
# reescalar descuadra el espejo, que es justo lo que hace que la costura empalme.
MEDIA_ANCHO = 1024

# EL MOBILIARIO DE CALLE ESTA APAGADO, y el codigo se queda como acta de lo que se probo.
#
# Fran pidio "un escenario de una parada de autobus". Se dibujo: marquesina, farolas, banco
# y papelera, en dos versiones -vector con la paleta de la interfaz, y silueta oscura con
# filo de luz-. LAS DOS QUEDAN MAL, y por el mismo motivo: el pueblo es una ilustracion
# PINTADA, con volumen, textura y luz propia, y cualquier forma plana puesta encima se lee
# como un recorte pegado o directamente como un fallo de carga -barras negras-.
#
# Lo que si funciona es la calle sola, que ya ES un escenario 2D de pueblo y ya tiene
# mobiliario pintado (mesas, farolillos, un buzon). Una parada de autobus de verdad pide un
# asset del mismo estilo, no formas de PIL: o modelada y renderizada como las fichas, o
# ilustrada. Poner MOBILIARIO = True para volver a ver lo descartado.
MOBILIARIO = False

SILUETA = (28, 25, 38, 236)
# EL FILO DE LUZ es lo que separa "objeto en sombra" de "agujero en la imagen". Dos pixeles
# mas claros en el canto de arriba de cada pieza, en la direccion de la luz del teatrillo.
# Sin el, las siluetas se leian como barras negras y parecian un fallo de carga.
FILO = (150, 156, 178, 210)


def _banda():
    """Una franja del pueblo a su escala, apagada para que el dino gris se despegue."""
    pueblo = Image.open(FUENTE).convert('RGB')
    banda = pueblo.crop((0, BANDA_Y, pueblo.width, BANDA_Y + ALTO_BANDA))
    banda = banda.resize((MEDIA_ANCHO, ALTO), Image.LANCZOS)
    banda = ImageEnhance.Color(banda).enhance(0.72)
    banda = ImageEnhance.Brightness(banda).enhance(0.74)
    # El fondo esta LEJOS. Ademas el desenfoque mata el grano del reescalado y, sobre todo,
    # hace que al correr no compita con el bicho, que es lo unico que hay que mirar.
    return banda.filter(ImageFilter.GaussianBlur(1.1))


def _masa(d, caja, filo=True):
    """Una pieza solida con su canto iluminado arriba."""
    x0, y0, x1, y1 = caja
    d.rectangle([x0, y0, x1, y1], fill=SILUETA)
    if filo and y1 - y0 > 4:
        d.rectangle([x0, y0, x1, y0 + 2], fill=FILO)


def _farola(d, x, suelo):
    alto = 74 * ESCALA
    arriba = suelo - alto
    _masa(d, [x, arriba, x + 6 * ESCALA, suelo], filo=False)
    _masa(d, [x - 2 * ESCALA, arriba + 4 * ESCALA, x + 8 * ESCALA, arriba + 7 * ESCALA])
    # El farol: una campana maciza y, DENTRO, la bombilla encendida. La luz va dentro del
    # farol y no flotando al lado, que es lo que hacia que antes no se leyera.
    _masa(d, [x - 9 * ESCALA, arriba - 13 * ESCALA, x + 15 * ESCALA, arriba + 4 * ESCALA])
    d.ellipse([x - 5 * ESCALA, arriba - 10 * ESCALA, x + 11 * ESCALA, arriba + 1 * ESCALA],
              fill=(255, 226, 150, 220))
    d.ellipse([x - 20 * ESCALA, arriba - 24 * ESCALA, x + 26 * ESCALA, arriba + 15 * ESCALA],
              fill=(255, 222, 140, 30))


def _parada(d, x, suelo):
    """La marquesina: techo volado, panel de fondo macizo, banco y el disco del bus."""
    ancho, alto = 104 * ESCALA, 60 * ESCALA
    arriba = suelo - alto
    # El panel de fondo va SOLIDO. Translucido se leia como una mesa con patas.
    _masa(d, [x + 3 * ESCALA, arriba + 7 * ESCALA, x + ancho - 3 * ESCALA, suelo], filo=False)
    # El techo vuela por los dos lados: es lo que la hace marquesina y no un armario.
    _masa(d, [x - 7 * ESCALA, arriba, x + ancho + 7 * ESCALA, arriba + 7 * ESCALA])
    _masa(d, [x, arriba, x + 6 * ESCALA, suelo], filo=False)
    _masa(d, [x + ancho - 6 * ESCALA, arriba, x + ancho, suelo], filo=False)
    # El banco de dentro, recortado en claro sobre el panel: a contraluz, lo que se ve de
    # una marquesina es el HUECO del banco, no el banco.
    banco = suelo - 20 * ESCALA
    d.rectangle([x + 12 * ESCALA, banco, x + ancho - 12 * ESCALA, banco + 5 * ESCALA],
                fill=(120, 126, 148, 220))
    # El disco de la parada en su palo, con un autobus recortado dentro.
    palo = x + ancho + 16 * ESCALA
    _masa(d, [palo, suelo - 70 * ESCALA, palo + 5 * ESCALA, suelo], filo=False)
    cx, cy, r = palo + 2 * ESCALA, suelo - 70 * ESCALA, 15 * ESCALA
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SILUETA)
    d.ellipse([cx - r, cy - r, cx + r, cy - r + 4], fill=FILO)
    bw, bh = int(r * 1.2), int(r * 0.72)
    bx, by = cx - bw // 2, cy - bh // 2
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=3, fill=(240, 231, 205, 240))
    d.rectangle([bx + 2, by + bh - 4, bx + bw - 2, by + bh], fill=SILUETA)
    d.rectangle([bx + bw // 2 - 1, by + 2, bx + bw // 2 + 1, by + bh - 4], fill=SILUETA)


def _banco(d, x, suelo):
    ancho = 42 * ESCALA
    tabla = suelo - 16 * ESCALA
    _masa(d, [x, tabla, x + ancho, tabla + 5 * ESCALA])
    _masa(d, [x, tabla - 14 * ESCALA, x + ancho, tabla - 9 * ESCALA])
    for pata in (x + 3 * ESCALA, x + ancho - 8 * ESCALA):
        _masa(d, [pata, tabla - 14 * ESCALA, pata + 5 * ESCALA, suelo], filo=False)


def _papelera(d, x, suelo):
    ancho, alto = 15 * ESCALA, 20 * ESCALA
    d.rounded_rectangle([x, suelo - alto, x + ancho, suelo], radius=4, fill=SILUETA)
    d.rectangle([x, suelo - alto, x + ancho, suelo - alto + 3], fill=FILO)


def construir():
    fondo = _banda().convert('RGBA')
    media = fondo.width
    suelo = int(ALTO * 0.942)   # el mismo punto de la ilustracion que antes, en la banda alta

    if MOBILIARIO:
        calle = Image.new('RGBA', (media, ALTO), (0, 0, 0, 0))
        d = ImageDraw.Draw(calle, 'RGBA')
        _farola(d, int(media * 0.05), suelo)
        _parada(d, int(media * 0.16), suelo)
        _papelera(d, int(media * 0.42), suelo)
        _banco(d, int(media * 0.52), suelo)
        _farola(d, int(media * 0.70), suelo)
        _papelera(d, int(media * 0.90), suelo)
        fondo = Image.alpha_composite(fondo, calle)

    # Sombra del telon, de arriba abajo. Es uniforme a lo ancho, asi que empalma sola y no
    # hay que preocuparse de ella al espejar. Un decorado de teatro nunca esta igual de
    # iluminado arriba que a la altura del actor.
    sombra = Image.new('RGBA', (media, ALTO), (0, 0, 0, 0))
    lapiz = ImageDraw.Draw(sombra)
    tope = int(ALTO * 0.46)
    for y in range(tope):
        k = 1.0 - y / float(tope)
        lapiz.line([(0, y), (media, y)], fill=(8, 14, 30, int(165 * k * k)))
    fondo = Image.alpha_composite(fondo, sombra)

    tira = Image.new('RGBA', (media * 2, ALTO), (0, 0, 0, 0))
    tira.paste(fondo, (0, 0))
    tira.paste(fondo.transpose(Image.FLIP_LEFT_RIGHT), (media, 0))
    return tira.convert('RGB')


if __name__ == '__main__':
    imagen = construir()
    imagen.save(SALIDA)
    print('escrito %s  %sx%s  %s KB' % (
        SALIDA, imagen.size[0], imagen.size[1], os.path.getsize(SALIDA) // 1024))

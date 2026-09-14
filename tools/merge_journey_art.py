"""Funde las diez ilustraciones del viaje en las cinco del barrio de diez niveles.

EL PROBLEMA. Cada ilustracion trae un camino pintado con CINCO paradas, y sus
coordenadas estan medidas a mano sobre el dibujo (JourneyStops, en
EpisodeJourney.cs). Al pasar el barrio a diez niveles hacian falta diez paradas, y
las dos salidas obvias eran malas: estirar una sola imagen al doble de alto deja a
los personajes con el doble de altura, y repartir diez paradas sobre un camino
pintado para cinco las amontona a 28 px unas de otras.

LA SALIDA. Fundir las dos imagenes del barrio en UNA del doble de alto, con la
costura difuminada. Entonces:

- El arte crece de verdad -1024x~2000 en vez de 1024x1035- y el marco crece en la
  misma proporcion, asi que NO se deforma nada.
- Las diez paradas son las cinco de arriba y las cinco de abajo, cada una donde ya
  estaba medida. Cero coordenadas nuevas.
- No se tira ninguna ilustracion, ni la del mapa ni sus vinetas.

LA COSTURA. Las dos escenas son distintas, asi que un corte a hueso se ve. Se
funden sobre una banda de solape con una rampa suave (smoothstep, no lineal: una
rampa lineal deja dos aristas visibles justo donde empieza y acaba la mezcla). La
banda ademas se tine hacia el color medio de las dos escenas en su centro, que es
lo que evita que se lea como una imagen encima de otra.

LAS VINETAS. La franja de comic de cada ilustracion vive en la parte de abajo del
PNG, partida en dos por ComicSplit. El barrio tiene ahora CUATRO vinetas -dos de
cada-, y se colocan en una rejilla 2x2 de cuadrantes fijos de 512x512 debajo del
mapa. Fijos a proposito: asi el codigo no necesita una tabla de cortes por barrio,
solo la altura del mapa.

Uso:
    python tools/merge_journey_art.py
"""
from pathlib import Path
import sys
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RAIZ = Path(__file__).resolve().parents[1]
ARTE = RAIZ / 'FrutiCity/Assets/FrutiCity/Resources/Art/Journey'
ANCHO, ALTO = 1024, 1536

# Lo que mide la parte de MAPA de cada ilustracion; el resto de abajo son sus dos
# vinetas. Copiado de MapBottom y ComicSplit en EpisodeJourney.cs: si alli cambian,
# aqui tambien, o el mapa saldria con media vineta pegada.
MAP_BOTTOM = [1024, 1048, 1040, 1018, 1035, 1048, 1055, 1088, 1047, 1063]
COMIC_SPLIT = [512, 480, 512, 512, 500, 510, 417, 501, 491, 512]

# Alto de la banda donde las dos escenas se mezclan. 190 px sobre 1024 es algo mas
# de un sexto de una escena: menos se lee como un corte, mas se come el camino
# pintado de las dos y las paradas de la costura se quedan sobre una nube gris.
SOLAPE = 190
CUADRANTE = 512


def suave(t):
    """Smoothstep. La rampa lineal deja dos aristas -arriba y abajo de la banda-
    porque la mezcla arranca y para de golpe; esta entra y sale con pendiente cero."""
    return t * t * (3 - 2 * t)


def mapa(indice):
    im = Image.open(ARTE / ('episode_%02d.png' % (indice + 1))).convert('RGB')
    if im.size != (ANCHO, ALTO):
        im = im.resize((ANCHO, ALTO), Image.LANCZOS)
    return im.crop((0, 0, ANCHO, MAP_BOTTOM[indice]))


def vinetas(indice):
    """Las dos vinetas de una ilustracion, cada una por su lado del corte."""
    im = Image.open(ARTE / ('episode_%02d.png' % (indice + 1))).convert('RGB')
    if im.size != (ANCHO, ALTO):
        im = im.resize((ANCHO, ALTO), Image.LANCZOS)
    tira = im.crop((0, MAP_BOTTOM[indice], ANCHO, ALTO))
    corte = COMIC_SPLIT[indice]
    return tira.crop((0, 0, corte, tira.height)), tira.crop((corte, 0, ANCHO, tira.height))


def encaja(imagen, lado=CUADRANTE):
    """La vineta dentro de su cuadrado sin deformarla: se escala por el lado que
    mas aprieta y se recorta el sobrante. Rellenar con barras dejaria dos franjas
    de color plano en mitad del comic."""
    escala = max(lado / imagen.width, lado / imagen.height)
    grande = imagen.resize((max(lado, round(imagen.width * escala)),
                            max(lado, round(imagen.height * escala))), Image.LANCZOS)
    x = (grande.width - lado) // 2
    y = (grande.height - lado) // 2
    return grande.crop((x, y, x + lado, y + lado))


def funde(arriba, abajo):
    """Las dos escenas en una, mezcladas sobre la banda de solape."""
    alto = arriba.height + abajo.height - SOLAPE
    lienzo = Image.new('RGB', (ANCHO, alto))
    lienzo.paste(arriba, (0, 0))
    lienzo.paste(abajo, (0, arriba.height - SOLAPE))
    # La banda se rehace pixel a pixel: se toma la tira de cada escena y se cruzan
    # con el peso de la rampa. Pegar y difuminar encima emborronaria tambien el
    # dibujo de los lados, no solo la union.
    banda_a = arriba.crop((0, arriba.height - SOLAPE, ANCHO, arriba.height))
    banda_b = abajo.crop((0, 0, ANCHO, SOLAPE))
    mezcla = Image.new('RGB', (ANCHO, SOLAPE))
    for fila in range(SOLAPE):
        peso = suave(fila / (SOLAPE - 1.0))
        linea = Image.blend(banda_a.crop((0, fila, ANCHO, fila + 1)),
                            banda_b.crop((0, fila, ANCHO, fila + 1)), peso)
        mezcla.paste(linea, (0, fila))
    # Un desenfoque muy corto SOLO sobre la banda: remata las lineas de contorno de
    # las dos escenas, que son gruesas y oscuras y se cruzarian a la vista.
    mezcla = mezcla.filter(ImageFilter.GaussianBlur(1.6))
    lienzo.paste(mezcla, (0, arriba.height - SOLAPE))
    return lienzo, alto


def main():
    alturas = []
    for area in range(5):
        a, b = area * 2, area * 2 + 1
        fundido, alto_mapa = funde(mapa(a), mapa(b))
        # Las cuatro vinetas en rejilla 2x2, en el orden en que se leen.
        cuatro = list(vinetas(a)) + list(vinetas(b))
        lienzo = Image.new('RGB', (ANCHO, alto_mapa + CUADRANTE * 2))
        lienzo.paste(fundido, (0, 0))
        for i, vineta in enumerate(cuatro):
            lienzo.paste(encaja(vineta), ((i % 2) * CUADRANTE, alto_mapa + (i // 2) * CUADRANTE))
        destino = ARTE / ('area_%02d.png' % (area + 1))
        lienzo.save(destino, optimize=True)
        alturas.append(alto_mapa)
        print('area_%02d.png  %dx%d  mapa=%d  (episodios %d+%d)  %d KB'
              % (area + 1, lienzo.width, lienzo.height, alto_mapa, a + 1, b + 1,
                 destino.stat().st_size // 1024))
    print()
    print('MapBottom para EpisodeJourney.cs:')
    print('        static readonly float[] MapBottom = {' + ','.join(str(h) for h in alturas) + '};')
    print('desplazamiento de las cinco paradas de abajo, por barrio:')
    print('       ', [MAP_BOTTOM[a * 2] - SOLAPE for a in range(5)])


if __name__ == '__main__':
    main()

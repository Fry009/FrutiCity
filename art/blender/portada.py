"""La pantalla inicial de FrutiCity.

El fondo se compone aqui, no en Blender: los rayos, las nubes y los
petalos son formas planas, y hacerlas en 3D solo aniade tiempo de render y
ruido. De Blender salen los tres personajes recortados con alfa
(escenas.py) y aqui se montan sobre el fondo con el rotulo.

Formato 1080x1920: la pantalla inicial de un movil en vertical.

Uso:
    python portada.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random

HERE = Path(__file__).resolve().parent
ESCENAS = HERE / 'fresita_v5' / 'escenas'
SALIDA = HERE / 'fresita_v5' / 'portada_fruticity.png'
# la que se lleva Unity va SIN el boton dibujado: alli el boton es de
# verdad (UiKit) y se pinta encima, para que responda al dedo
SALIDA_JUEGO = HERE / 'fresita_v5' / 'portada_fondo.png'

W, H = 1080, 1920
FUENTES = Path("C:/Windows/Fonts")
TITULO = FUENTES / "ariblk.ttf"
JAPO = FUENTES / "YuGothB.ttc"

# paleta: rosa arriba, amarillo en medio, turquesa abajo
CIELO = [(0.00, (255, 150, 190)), (0.34, (255, 196, 150)),
         (0.62, (255, 224, 130)), (1.00, (122, 226, 214))]
ROSA = (243, 90, 140)
AMARILLO = (255, 208, 62)
TURQUESA = (60, 200, 190)
CREMA = (255, 250, 240)
TINTA = (58, 34, 48)


def _mezcla(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def cielo():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(CIELO) - 1):
            t0, c0 = CIELO[i]
            t1, c1 = CIELO[i + 1]
            if t0 <= t <= t1:
                d.line([(0, y), (W, y)], fill=_mezcla(c0, c1, (t - t0) / (t1 - t0)))
                break
    return img.convert('RGBA')


def rayos(cx, cy, n=26, largo=2400, alfa=48):
    """El sunburst de detras. Es LA forma que dice 'japones alegre'."""
    capa = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + math.pi / n * 0.92
        d.polygon([(cx * 2, cy * 2),
                   (cx * 2 + largo * 2 * math.cos(a0), cy * 2 + largo * 2 * math.sin(a0)),
                   (cx * 2 + largo * 2 * math.cos(a1), cy * 2 + largo * 2 * math.sin(a1))],
                  fill=(255, 255, 255, alfa))
    return capa.resize((W, H), Image.LANCZOS)


def burbujas(n=26, seed=5):
    rnd = random.Random(seed)
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for _ in range(n):
        r = rnd.randint(14, 66)
        x, y = rnd.randint(-20, W + 20), rnd.randint(60, H - 300)
        col = rnd.choice([(255, 255, 255, 70), (255, 226, 120, 74),
                          (255, 150, 190, 66), (120, 226, 214, 70)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    return capa


def petalo(capa, x, y, r, giro, color=(255, 190, 214, 210)):
    """Petalo de sakura: cinco lobulos con una muesca en la punta."""
    d = ImageDraw.Draw(capa)
    for k in range(5):
        a = giro + 2 * math.pi * k / 5
        pts = []
        for i in range(19):
            t = i / 18
            ang = a - 0.42 + 0.84 * t
            rad = r * (0.42 + 0.58 * math.sin(math.pi * t) ** 0.7)
            rad *= 1.0 - 0.22 * (math.sin(math.pi * t * 2) ** 2 if t > 0.82 else 0)
            pts.append((x + rad * math.cos(ang), y + rad * math.sin(ang)))
        d.polygon([(x, y)] + pts, fill=color)


def sakura(n=17, seed=11):
    rnd = random.Random(seed)
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for _ in range(n):
        petalo(capa, rnd.randint(0, W), rnd.randint(40, H - 260),
               rnd.randint(13, 27), rnd.uniform(0, 6.28),
               (255, rnd.randint(180, 210), rnd.randint(210, 232), rnd.randint(150, 225)))
    return capa


def nubes():
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    rnd = random.Random(3)
    for base, esc, alfa in ((H - 150, 1.00, 255), (H - 292, 0.74, 175)):
        x = -80
        while x < W + 120:
            r = rnd.randint(60, 118) * esc
            d.ellipse([x - r, base - r, x + r, base + r], fill=(255, 255, 255, alfa))
            x += r * 1.25
    d.rectangle([0, H - 150, W, H], fill=(255, 255, 255, 255))
    return capa


def texto_contorno(d, xy, texto, font, relleno, contorno=CREMA, grosor=9,
                   sombra=None, ancla="mm"):
    x, y = xy
    if sombra:
        d.text((x + sombra[0], y + sombra[1]), texto, font=font, fill=sombra[2],
               anchor=ancla, stroke_width=grosor, stroke_fill=sombra[2])
    d.text((x, y), texto, font=font, fill=relleno, anchor=ancla,
           stroke_width=grosor, stroke_fill=contorno)


def rotulo(img):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(TITULO), 156)
    palabra = "FrutiCity"
    colores = [ROSA, ROSA, ROSA, ROSA, ROSA, AMARILLO, AMARILLO,
               TURQUESA, TURQUESA]
    anchos = [d.textlength(ch, font=f) for ch in palabra]
    total = sum(anchos)
    x = (W - total) / 2
    y = 258
    # primero el contorno de toda la palabra, para que no se corte entre letras
    for paso in (("borde", 26, TINTA), ("blanco", 15, CREMA)):
        xx = x
        for ch, an in zip(palabra, anchos):
            d.text((xx, y), ch, font=f, fill=paso[2], anchor="ls",
                   stroke_width=paso[1], stroke_fill=paso[2])
            xx += an
    xx = x
    for ch, an, col in zip(palabra, anchos, colores):
        d.text((xx, y), ch, font=f, fill=col, anchor="ls")
        xx += an
    # katakana: "furuutishiti"
    try:
        fj = ImageFont.truetype(str(JAPO), 62)
        texto_contorno(d, (W / 2, y + 84), "フルーティシティ", fj, ROSA,
                       CREMA, 11, ancla="mm")
    except Exception as e:
        print("[portada] sin fuente japonesa:", e)


def boton(img, texto="JUGAR"):
    """Tecla 3D: la cara de arriba y un canto oscuro debajo. Es lo que
    hace que un boton parezca pulsable y no una pegatina."""
    d = ImageDraw.Draw(img)
    w, h = 560, 152
    x0, y0 = (W - w) / 2, H - 262
    canto = 26
    d.rounded_rectangle([x0, y0 + canto, x0 + w, y0 + h + canto], 46,
                        fill=(196, 120, 20))
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 46, fill=(255, 190, 46),
                        outline=CREMA, width=9)
    d.rounded_rectangle([x0 + 34, y0 + 20, x0 + w - 34, y0 + 56], 22,
                        fill=(255, 226, 140))
    f = ImageFont.truetype(str(TITULO), 74)
    texto_contorno(d, (W / 2, y0 + h / 2 + 8), texto, f, (255, 255, 255),
                   (176, 96, 12), 10)


def pega(fondo, ruta, alto, cx, base):
    im = Image.open(ruta).convert('RGBA')
    caja = im.getbbox()
    if caja:
        im = im.crop(caja)
    k = alto / im.height
    im = im.resize((max(1, int(im.width * k)), alto), Image.LANCZOS)
    # sombra blanda en el suelo
    sombra = Image.new('RGBA', fondo.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    rw = im.width * 0.40
    ds.ellipse([cx - rw, base - 26, cx + rw, base + 26], fill=(120, 60, 90, 90))
    fondo.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(16)))
    fondo.alpha_composite(im, (int(cx - im.width / 2), int(base - alto)))
    return fondo


def main():
    img = cielo()
    img.alpha_composite(rayos(W / 2, 900))
    img.alpha_composite(burbujas())
    img.alpha_composite(sakura())
    img.alpha_composite(nubes())
    # los de los lados primero, para que la fresa quede delante
    pega(img, ESCENAS / "portada_pablo.png", 706, 224, 1556)
    pega(img, ESCENAS / "portada_nora.png", 684, 862, 1562)
    pega(img, ESCENAS / "portada_fresi.png", 880, 544, 1530)
    rotulo(img)
    img.convert('RGB').save(SALIDA_JUEGO, quality=96)
    print("[portada]", SALIDA_JUEGO)
    boton(img)
    img.convert('RGB').save(SALIDA, quality=96)
    print("[portada]", SALIDA)


if __name__ == "__main__":
    main()

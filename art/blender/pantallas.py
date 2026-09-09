"""Las pantallas de nivel superado y de reintentar.

Mismo reparto y mismo esqueleto que la portada: cambia el tramo de la
animacion y la cara del calco. Ganar usa el salto con cara alegre y perder
usa el desinflado con cara triste; de ahi salen las dos pantallas sin
modelar ni animar nada nuevo.

Entra: los PNG con alfa que deja escenas.py en fresita_v5/escenas/
Sale:  un GIF por personaje y resultado, listo para mirar.

Uso:
    python pantallas.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import glob, math, re

HERE = Path(__file__).resolve().parent
ESCENAS = HERE / 'fresita_v5' / 'escenas'
SALIDA = HERE / 'fresita_v5'

W, H = 620, 900
FUENTE = Path("C:/Windows/Fonts/ariblk.ttf")
JAPO = Path("C:/Windows/Fonts/YuGothB.ttc")
CREMA = (255, 250, 240)
TINTA = (58, 34, 48)

ESTILOS = {
    "victoria": dict(
        titulo="¡NIVEL SUPERADO!", japo="クリア！",
        color=(255, 196, 40), color2=(255, 126, 60),
        fondo=(38, 22, 54), rayos=(255, 226, 140, 62),
        boton=("SIGUIENTE", (86, 204, 108), (46, 148, 68)),
        estrellas=3),
    "derrota": dict(
        titulo="¡CASI LO TIENES!", japo="もう一回！",
        color=(126, 196, 255), color2=(96, 140, 236),
        fondo=(24, 26, 58), rayos=(150, 190, 255, 44),
        boton=("REINTENTAR", (255, 158, 62), (206, 108, 26)),
        estrellas=0),
}


def rayos(cx, cy, color, n=22, largo=1600):
    capa = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + math.pi / n * 0.9
        d.polygon([(cx * 2, cy * 2),
                   (cx * 2 + largo * 2 * math.cos(a0), cy * 2 + largo * 2 * math.sin(a0)),
                   (cx * 2 + largo * 2 * math.cos(a1), cy * 2 + largo * 2 * math.sin(a1))],
                  fill=color)
    return capa.resize((W, H), Image.LANCZOS)


def estrella(d, cx, cy, r, relleno, borde=CREMA, puntas=5):
    pts = []
    for i in range(puntas * 2):
        a = -math.pi / 2 + math.pi * i / puntas
        rad = r if i % 2 == 0 else r * 0.46
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=relleno, outline=borde, width=5)


def texto(d, xy, txt, font, relleno, contorno=CREMA, grosor=10):
    d.text(xy, txt, font=font, fill=relleno, anchor="mm",
           stroke_width=grosor, stroke_fill=contorno)


def boton(d, etiqueta, cara, canto, y):
    w, h = 400, 108
    x0 = (W - w) / 2
    d.rounded_rectangle([x0, y + 20, x0 + w, y + h + 20], 34, fill=canto)
    d.rounded_rectangle([x0, y, x0 + w, y + h], 34, fill=cara,
                        outline=CREMA, width=7)
    f = ImageFont.truetype(str(FUENTE), 46)
    texto(d, (W / 2, y + h / 2 + 4), etiqueta, f, (255, 255, 255), canto, 7)


def marco(clase):
    """El panel de fondo, igual en todos los fotogramas del GIF."""
    e = ESTILOS[clase]
    img = Image.new('RGBA', (W, H), e["fondo"] + (255,))
    img.alpha_composite(rayos(W / 2, H * 0.52, e["rayos"]))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(FUENTE), 54)
    texto(d, (W / 2, 110), e["titulo"], f, e["color"], CREMA, 11)
    try:
        fj = ImageFont.truetype(str(JAPO), 40)
        texto(d, (W / 2, 176), e["japo"], fj, e["color2"], CREMA, 9)
    except Exception:
        pass
    boton(d, *e["boton"], y=H - 178)
    return img


def frames(nombre, clase):
    rutas = sorted(glob.glob(str(ESCENAS / ("%s_%s_*.png" % (nombre, clase)))),
                   key=lambda p: int(re.findall(r"_(\d+)\.png$", p)[0]))
    if not rutas:
        return []
    fondo = marco(clase)
    alto = 470
    salida = []
    for r in rutas:
        im = Image.open(r).convert('RGBA')
        caja = im.getbbox()
        if caja:
            im = im.crop(caja)
        k = alto / im.height
        im = im.resize((max(1, int(im.width * k)), alto), Image.LANCZOS)
        cuadro = fondo.copy()
        sombra = Image.new('RGBA', cuadro.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sombra)
        ds.ellipse([W / 2 - im.width * .36, H - 234, W / 2 + im.width * .36, H - 204],
                   fill=(0, 0, 0, 78))
        cuadro.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(12)))
        cuadro.alpha_composite(im, (int(W / 2 - im.width / 2), int(H - 216 - alto)))
        dc = ImageDraw.Draw(cuadro)
        for i in range(ESTILOS[clase]["estrellas"]):
            estrella(dc, W / 2 + (i - 1) * 150, 268 - (30 if i == 1 else 0),
                     68 if i == 1 else 56, (255, 210, 60))
        salida.append(cuadro.convert('RGB'))
    return salida


def main():
    hechos = []
    for nombre in ("fresi", "pablo"):
        for clase in ("victoria", "derrota"):
            ims = frames(nombre, clase)
            if not ims:
                print("[pantallas] faltan fotogramas de %s %s" % (nombre, clase))
                continue
            ruta = SALIDA / ("pantalla_%s_%s.gif" % (clase, nombre))
            ims[0].save(ruta, save_all=True, append_images=ims[1:],
                        duration=110, loop=0, optimize=True)
            ims[len(ims) // 2].save(SALIDA / ("pantalla_%s_%s.png" % (clase, nombre)),
                                    quality=95)
            print("[pantallas]", ruta, len(ims), "fotogramas")
            hechos.append(ruta)
    return hechos


if __name__ == "__main__":
    main()

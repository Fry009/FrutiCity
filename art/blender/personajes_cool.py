"""FrutiCity: reparto adulto para el arte de fuera del juego.

Mismas piezas que personajes_v2 (cuerpo, brazos, pies, plataforma de squash) pero
con cara de mayor: gafas de sol, media sonrisa torcida y ceja levantada en vez de
la boca abierta y los mofletes rosas de las frutitas del tablero.

    blender --background --python art/blender/personajes_cool.py -- pina sandia coco limon

Sale un .blend y un PNG de 768 con fondo transparente en personajes_cool/.
Control de calidad: MIRAR el PNG. La camara mira desde -Y, asi que todo lo que
sea cara va con Y negativa; una gafa montada en el plano equivocado no da error
en consola, solo sale de canto.
"""
import bpy, sys, math, importlib
from pathlib import Path
from mathutils import Vector

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comun as c
SALIDA = AQUI / 'personajes_cool'
SALIDA.mkdir(exist_ok=True)

PIEL = {'pina': 'F2B22C', 'sandia': 'E8465A', 'coco': '8A5A32', 'limon': 'F7DE3A'}


def bola(nombre, loc, escala, material, seg=40, anillos=26):
    ob = c.esfera(nombre, 1, loc, escala, seg, anillos)
    ob.data.materials.append(material)
    c.suave(ob, 1)
    return ob


def gafas(oscuro, cristal, y, z, ancho=.30, alto=.19, inclina=8):
    """Dos cristales y el puente. El brillo diagonal es lo que las hace gafas y
    no dos manchas negras: sin el, a tamano pequeno parecen ojos cerrados."""
    for lado in (-1, 1):
        x = ancho * lado
        lente = bola('Cristal', (x, y, z), (ancho * .84, .07, alto), cristal)
        lente.rotation_euler[1] = math.radians(-inclina * lado)
        brillo = bola('Reflejo', (x - .07 * lado, y - .055, z + .05), (.075, .015, .028), oscuro)
        brillo.rotation_euler[1] = math.radians(38)
    bola('Puente', (0, y + .01, z + .02), (ancho * .34, .05, .035), oscuro)
    for lado in (-1, 1):
        patilla = bola('Patilla', (ancho * 1.72 * lado, y + .30, z + .05), (.055, .28, .035), oscuro)
        patilla.rotation_euler[2] = math.radians(-14 * lado)


def sonrisa_torcida(oscuro, superficie, z, ancho=.20, alza=.085):
    """Media sonrisa: una cuerda que sube por un lado. La boca abierta con lengua
    es la cara de las frutitas del tablero, y es justo lo que aqui no queremos."""
    puntos = []
    for i in range(19):
        u = i / 18
        x = (u * 2 - 1) * ancho
        zz = z + alza * (u ** 1.7) - .022 * math.sin(u * math.pi)
        puntos.append((x, superficie(x, zz) - .028, zz))
    ob = c.cuerda('Media sonrisa', puntos, .026)
    ob.data.materials.append(oscuro)
    return ob


def construir(tipo):
    importlib.reload(c)
    c.empezar()
    piel = c.mat('Piel fruta', c.hexcol(PIEL[tipo]), .40, .26)
    hoja = c.mat('Hoja fresca', c.hexcol('3F8F2A'), .43, .12)
    oscuro = c.mat('Chocolate', c.hexcol('2A1A14'), .30, .25)
    luz = c.mat('Brillo ojo', c.hexcol('FFF8E7'), .20, .20)
    zapato = c.mat('Zapato', c.hexcol('7A4A24'), .55)
    cristal = c.mat('Cristal gafa', c.hexcol('16121C'), .12, .85)

    if tipo == 'pina':
        # Cuerpo alargado: la pina es la unica que no es una bola, y esa silueta
        # es la mitad del personaje.
        perfil = [(math.sin(math.pi * i / 64) ** .70 * (.80 + .10 * math.cos(math.pi * i / 64)),
                   1.04 * math.cos(math.pi * i / 64)) for i in range(65)]
        cuerpo = c.revolucion(perfil, .80, 72, 'Cuerpo pina')
        cuerpo.data.materials.append(piel)
        c.suave(cuerpo, 2)
        for i in range(9):
            c.hoja_puesta(hoja, (0, 0, .92), (58 - (i % 3) * 16, -26, i * 40), largo=.86, ancho=.20)
    elif tipo == 'sandia':
        corteza = c.mat('Corteza', c.hexcol('2F7D2A'), .5)
        blanco = c.mat('Blanco corteza', c.hexcol('F2F3E4'), .45)
        # La corteza es un anillo alrededor de la pulpa, no una tapa detras: puesta
        # atras solo asomaba un hilo verde por el borde de arriba.
        bola('Corteza', (0, .05, 0), (1.00, .74, .92), corteza)
        bola('Blanco', (0, .02, 0), (.955, .74, .875), blanco)
        cuerpo = bola('Cuerpo sandia', (0, 0, 0), (.90, .74, .82), piel)
        pepita = c.mat('Pepita', c.hexcol('241812'), .4)
        for x, z in [(-.42, .22), (.40, .18), (-.18, -.30), (.24, -.36), (.0, .42), (-.50, -.14)]:
            bola('Pepita', (x, -.62, z), (.055, .022, .085), pepita, 16, 10)
    elif tipo == 'coco':
        cuerpo = bola('Cuerpo coco', (0, 0, 0), (.84, .78, .80), piel)
        material_pajita = c.mat('Pajita', c.hexcol('E5484F'), .35)
        pajita = bola('Pajita', (.30, -.26, 1.02), (.032, .032, .34), material_pajita, 16, 10)
        pajita.rotation_euler[1] = math.radians(26)
        codo = bola('Codo pajita', (.46, -.30, 1.26), (.032, .032, .12), material_pajita, 16, 10)
        codo.rotation_euler[1] = math.radians(64)
    else:
        perfil = [(math.sin(math.pi * i / 64) ** .86 * (.92 + .16 * math.cos(math.pi * i / 64)),
                   .92 * math.cos(math.pi * i / 64)) for i in range(65)]
        cuerpo = c.revolucion(perfil, .82, 72, 'Cuerpo limon')
        cuerpo.data.materials.append(piel)
        c.suave(cuerpo, 2)
        c.tallo(zapato, (0, 0, .86), alto=.16, r_base=.05, r_punta=.04)
        c.hoja_puesta(hoja, (0, 0, .82), (66, -28, 20), largo=.62, ancho=.21)

    bpy.context.view_layer.update()
    evaluado = cuerpo.evaluated_get(bpy.context.evaluated_depsgraph_get())

    def toca(x, z):
        """Y de la superficie, o None si el rayo no da en el cuerpo. Devolver un
        valor por defecto en el fallo es lo que dejaba escamas flotando fuera de
        la silueta: parecian moscas alrededor de la pina."""
        inv = cuerpo.matrix_world.inverted()
        hit, punto, _, _ = evaluado.ray_cast(inv @ Vector((x, -4, z)),
                                             (inv.to_3x3() @ Vector((0, 1, 0))).normalized())
        return (cuerpo.matrix_world @ punto).y if hit else None

    def superficie(x, z):
        y = toca(x, z)
        return -.60 if y is None else y

    if tipo == 'pina':
        # Rombos apoyados en la superficie por trazado de rayo. Colocarlos por radio
        # a ojo los metia dentro del cuerpo y la pina parecia un mango.
        escama = c.mat('Escama', c.hexcol('C07E14'), .55)
        for fila, z in enumerate([.74, .55, .36, .17, -.02, -.21, -.40, -.59]):
            for col in range(7):
                x = (col - 3) * .20 + (.10 if fila % 2 else 0)
                y = toca(x, z)
                # Solo donde hay cuerpo, y con margen para no pegarlas al filo del
                # contorno, donde asomarian por fuera.
                if y is None or abs(x) > .62 or toca(x + math.copysign(.09, x), z) is None:
                    continue
                rombo = bola('Escama', (x, y + .030, z), (.105, .048, .062), escama, 14, 10)
                rombo.rotation_euler[1] = math.radians(45)
    cara_z = .10 if tipo == 'pina' else .06
    y_gafas = superficie(0, cara_z + .12) - .055
    gafas(oscuro, cristal, y_gafas, cara_z + .12, ancho=.31, alto=.185)
    # Una ceja asomando por encima de la montura: es lo que da el gesto de listillo.
    ceja = []
    for i in range(14):
        dx = (i / 13 - .5) * .24
        zz = cara_z + .335 + .055 * (i / 13)
        ceja.append((-.31 + dx, superficie(-.31 + dx, zz) - .034, zz))
    ob = c.cuerda('Ceja levantada', ceja, .020)
    ob.data.materials.append(zapato)
    sonrisa_torcida(oscuro, superficie, cara_z - .30)
    bola('Brillo mejilla', (.34, superficie(.34, cara_z - .12) - .04, cara_z - .12),
         (.055, .020, .030), luz)

    # Medidos del cuerpo ya evaluado. Con coordenadas fijas, los cuerpos bajos
    # dejaban los pies colgando en el aire y los brazos despegados.
    esquinas = [cuerpo.matrix_world @ Vector(v) for v in evaluado.bound_box]
    ancho = max(p.x for p in esquinas)
    suelo = min(p.z for p in esquinas)
    for lado in (-1, 1):
        brazo = bola('Brazo', (ancho * .90 * lado, .02, suelo * .34), (.14, .17, .27), piel)
        brazo.rotation_euler[1] = lado * math.radians(26)
        bola('Zapato', (.30 * lado, -.14, suelo + .04), (.21, .30, .12), zapato)

    plataforma = bpy.data.objects.new('Fruit_Squash_Rig', None)
    bpy.context.scene.collection.objects.link(plataforma)
    for ob in list(c._vivos()):
        ob.parent = plataforma
    for f, s, z in [(1, (1, 1, 1), 0), (15, (.97, .97, 1.055), .03), (30, (1.055, 1.055, .94), 0),
                    (45, (.985, .985, 1.02), .012), (60, (1, 1, 1), 0)]:
        plataforma.scale = s
        plataforma.location.z = z
        plataforma.keyframe_insert('scale', frame=f)
        plataforma.keyframe_insert('location', frame=f)
    escena = bpy.context.scene
    escena.frame_end = 60
    escena.render.fps = 30
    escena.frame_set(1)
    c.CAM_LOC = (0, -9, 1.65)
    c.MARGEN = .13
    c.LUZ_CLAVE = 280
    c.LUZ_PUNTO = 110
    c.LUZ_RELLENO = 130
    c.LUZ_CONTRA = 180
    c.terminar()
    escena.render.engine = 'CYCLES'
    escena.cycles.samples = 64
    escena.cycles.use_denoising = True
    escena.render.film_transparent = True
    escena.render.image_settings.file_format = 'PNG'
    escena.render.image_settings.color_mode = 'RGBA'
    escena.render.resolution_x = escena.render.resolution_y = 768
    escena.render.resolution_percentage = 100
    escena.view_settings.view_transform = 'Standard'
    escena.render.filepath = str(SALIDA / (tipo + '.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(SALIDA / (tipo + '.blend')))
    bpy.ops.render.render(write_still=True)
    print('FRUTI_COOL_DONE', tipo, flush=True)


if __name__ == '__main__':
    nombres = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['pina', 'sandia', 'coco', 'limon']
    for nombre in nombres:
        construir(nombre)

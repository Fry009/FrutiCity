"""Esqueleto y movimiento de Fresita.

Pocos huesos a proposito: 16. Fresita esta hecha de piezas sueltas (cada
brazo, cada zapatilla, cada ojo es un objeto), asi que NO hace falta
skinning con pesos: cada pieza se cuelga de un hueso y ya. Eso es lo que
permite tener rig sin repartir pesos a mano ni que se estire nada.

    Root
      Hips ─ Spine ─ Head
      │        └ UpperArm.L/R ─ LowerArm.L/R ─ Hand.L/R
      └ Thigh.L/R ─ Shin.L/R ─ Foot.L/R

Uso:
    blender --background fresita_v5/fresita.blend --python fresita_rig.py
    (o importarlo desde una sesion viva y llamar a montar())
"""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

OUT = HERE / 'fresita_v5'
RIG = "Fresita_Rig"

# --- huesos: (nombre, cabeza, cola, padre) ------------------------------
# Las coordenadas salen de las mismas alturas que fresita_sheet.py.
HUESOS = [
    ("Root",  (0, 0, 0.00), (0, 0, 0.12), None),
    ("Hips",  (0, 0, 0.44), (0, 0, 0.53), "Root"),
    ("Spine", (0, 0, 0.53), (0, 0, 0.79), "Hips"),
    ("Head",  (0, 0, 0.82), (0, 0, 1.50), "Spine"),
]
for s, sgn in (("L", -1), ("R", 1)):
    HUESOS += [
        ("UpperArm." + s, (0.158 * sgn, 0, 0.770), (0.228 * sgn, 0, 0.608), "Spine"),
        ("LowerArm." + s, (0.228 * sgn, 0, 0.612), (0.258 * sgn, 0, 0.472), "UpperArm." + s),
        ("Hand." + s,     (0.258 * sgn, 0, 0.472), (0.264 * sgn, 0, 0.350), "LowerArm." + s),
        ("Thigh." + s,    (0.105 * sgn, 0, 0.440), (0.118 * sgn, 0, 0.240), "Hips"),
        ("Shin." + s,     (0.118 * sgn, 0, 0.240), (0.122 * sgn, 0, 0.115), "Thigh." + s),
        ("Foot." + s,     (0.122 * sgn, 0, 0.115), (0.124 * sgn, -0.16, 0.055), "Shin." + s),
    ]

# --- que pieza va con que hueso ----------------------------------------
# Se prueba el prefijo mas largo primero, para que "PerneraRibeteL" no
# caiga en la regla de "PerneraL".
SIN_LADO = {
    "Cabeza": "Head", "HojaAlta": "Head", "Hoja": "Head", "Rabito": "Head",
    "Cara": "Head",
    "Nariz": "Head", "Boca": "Head", "Labio": "Head", "Dientes": "Head",
    "Lengua": "Head",
    "Torso": "Spine", "TopBorde": "Spine", "TopRibete": "Spine", "Top": "Spine",
    "CamisetaRibete": "Spine", "Camiseta": "Spine",
    "VestidoCintura": "Spine", "VestidoRibete": "Spine", "Vestido": "Spine",
    "Cuello": "Spine", "Punta": "Head",
    "ShortCinturilla": "Hips", "Short": "Hips",
    "PantalonRibete": "Hips", "Pantalon": "Hips",
}
CON_LADO = {
    "Pestana": "Head", "Ojo": "Head", "Iris": "Head", "Pupila": "Head",
    "Brillo": "Head", "Rabillo": "Head", "Ceja": "Head",
    "Hombro": "Spine", "Tirante": "Spine", "Busto": "Spine",
    "MangaVivo": "UpperArm.%s", "Manga": "UpperArm.%s",
    "Gluteo": "Hips", "Lazo": "Hips", "Cabo": "Hips",
    "BrazoAlto": "UpperArm.%s", "BrazoBajo": "LowerArm.%s",
    "Mano": "Hand.%s", "Dedo": "Hand.%s", "Pulgar": "Hand.%s",
    "PerneraRibete": "Thigh.%s", "Pernera": "Thigh.%s", "Muslo": "Thigh.%s",
    "Gemelo": "Shin.%s",
    "Zapa": "Foot.%s", "Suela": "Foot.%s", "Puntera": "Foot.%s",
    "Talon": "Foot.%s", "Cordon": "Foot.%s",
}


def _base(nombre):
    """Quita el .001 que Blender pega a los duplicados."""
    if len(nombre) > 4 and nombre[-4] == '.' and nombre[-3:].isdigit():
        return nombre[:-4]
    return nombre


def hueso_de(ob):
    n = _base(ob.name)
    # las pepitas no llevan lado ni numero util: van por altura
    if n == "Pepita":
        return "Head" if ob.matrix_world.translation.z > 0.86 else "Spine"
    for pre in sorted(CON_LADO, key=len, reverse=True):
        if n.startswith(pre):
            resto = n[len(pre):]
            for s in ("L", "R"):
                if resto.startswith(s):
                    destino = CON_LADO[pre]
                    return destino % s if "%s" in destino else destino
    for pre in sorted(SIN_LADO, key=len, reverse=True):
        if n.startswith(pre):
            return SIN_LADO[pre]
    return None


def crear_armadura():
    viejo = bpy.data.objects.get(RIG)
    if viejo:
        bpy.data.objects.remove(viejo, do_unlink=True)
    arm = bpy.data.armatures.new(RIG)
    rig = bpy.data.objects.new(RIG, arm)
    bpy.context.scene.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    for nombre, cab, col, padre in HUESOS:
        b = arm.edit_bones.new(nombre)
        b.head, b.tail = Vector(cab), Vector(col)
        if padre:
            b.parent = arm.edit_bones[padre]
    bpy.ops.object.mode_set(mode='OBJECT')
    rig.select_set(False)
    rig.show_in_front = True
    arm.display_type = 'OCTAHEDRAL'
    return rig


def colgar_piezas(rig):
    """Cada pieza al hueso que le toca, sin mover nada de sitio."""
    puestas, huerfanas = {}, []
    for ob in list(bpy.context.scene.objects):
        if ob.type not in ('MESH', 'CURVE') or ob is rig:
            continue
        h = hueso_de(ob)
        if h is None or h not in rig.data.bones:
            huerfanas.append(ob.name)
            continue
        mw = ob.matrix_world.copy()
        ob.parent = rig
        ob.parent_type = 'BONE'
        ob.parent_bone = h
        bpy.context.view_layer.update()
        ob.matrix_world = mw          # el parent a hueso cuelga de la COLA
        puestas[h] = puestas.get(h, 0) + 1
    return puestas, huerfanas


# ============ movimiento ================================================

def _k(pb, frame, rot=None, loc=None):
    if rot is not None:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = [math.radians(a) for a in rot]
        pb.keyframe_insert('rotation_euler', frame=frame)
    if loc is not None:
        pb.location = loc
        pb.keyframe_insert('location', frame=frame)


def _fcurves(act):
    """Las curvas de una accion. En Blender 5 ya no cuelgan de
    action.fcurves: van por capas y slots, y el atributo viejo no existe."""
    if hasattr(act, "fcurves"):
        return list(act.fcurves)
    out = []
    for capa in getattr(act, "layers", []):
        for strip in capa.strips:
            bolsas = getattr(strip, "channelbags", None)
            if bolsas is None:
                for slot in act.slots:
                    cb = strip.channelbag(slot)
                    if cb:
                        out.extend(cb.fcurves)
            else:
                for cb in bolsas:
                    out.extend(cb.fcurves)
    return out


def animar(rig, fin=230):
    """Una sola accion con los tramos seguidos, para darle al play y verlo
    todo: respirar (1-60), saludar (61-110), saltar (111-170) y
    derrota (171-230), que es la del retry."""
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')
    act = bpy.data.actions.new("Fresita_Demo")
    rig.animation_data_create()
    rig.animation_data.action = act
    P = rig.pose.bones

    def reposo(f):
        for n in ("Root", "Hips", "Spine", "Head",
                  "UpperArm.L", "UpperArm.R", "LowerArm.L", "LowerArm.R",
                  "Thigh.L", "Thigh.R", "Shin.L", "Shin.R"):
            _k(P[n], f, rot=(0, 0, 0))
        _k(P["Root"], f, loc=(0, 0, 0))

    # --- 1..60 respirar: el pecho se abre y la cabeza acompaña tarde ---
    reposo(1)
    for f, (sp, hd, rz) in ((15, (-3.0, 2.0, 0.0)), (30, (0.0, 0.0, 0.0)),
                            (45, (2.5, -1.6, 0.0)), (60, (0.0, 0.0, 0.0))):
        _k(P["Spine"], f, rot=(sp, 0, 0))
        _k(P["Head"], f + 4 if f < 60 else f, rot=(hd, 0, rz))
        _k(P["Root"], f, loc=(0, 0, -0.012 if f in (15, 45) else 0.0))
    for f in (1, 15, 30, 45, 60):
        _k(P["UpperArm.L"], f, rot=(0, 0, 3 if f in (15, 45) else 0))
        _k(P["UpperArm.R"], f, rot=(0, 0, -3 if f in (15, 45) else 0))

    # --- 61..110 saludar con la derecha --------------------------------
    _k(P["UpperArm.R"], 62, rot=(0, 0, 0))
    _k(P["LowerArm.R"], 62, rot=(0, 0, 0))
    _k(P["UpperArm.R"], 78, rot=(0, 0, -128))
    _k(P["LowerArm.R"], 78, rot=(0, 0, -22))
    for i, f in enumerate((86, 94, 102)):
        _k(P["UpperArm.R"], f, rot=(0, 0, -128))
        _k(P["LowerArm.R"], f, rot=(0, 0, -50 if i % 2 == 0 else 6))
    _k(P["UpperArm.R"], 110, rot=(0, 0, 0))
    _k(P["LowerArm.R"], 110, rot=(0, 0, 0))
    for f in (70, 90, 110):
        _k(P["Head"], f, rot=(0, 0, -7 if f == 90 else 0))
        _k(P["Spine"], f, rot=(0, 0, -4 if f == 90 else 0))

    # --- 111..170 salto: agacharse, subir, caer y amortiguar -----------
    def agacha(f, k, aire=0.0):
        _k(P["Root"], f, loc=(0, 0, aire))
        _k(P["Thigh.L"], f, rot=(k, 0, 0)); _k(P["Thigh.R"], f, rot=(k, 0, 0))
        _k(P["Shin.L"], f, rot=(-k * 1.7, 0, 0)); _k(P["Shin.R"], f, rot=(-k * 1.7, 0, 0))
        _k(P["Spine"], f, rot=(-k * 0.35, 0, 0))
    agacha(112, 0)
    agacha(124, 26)                       # se agacha
    agacha(132, -6, aire=0.26)            # despega y estira
    for n in ("UpperArm.L", "UpperArm.R"):
        _k(P[n], 124, rot=(0, 0, 0))
        _k(P[n], 132, rot=(0, 0, 118 if n.endswith("L") else -118))
        _k(P[n], 150, rot=(0, 0, 0))
    _k(P["Head"], 132, rot=(-10, 0, 0))
    agacha(142, 4, aire=0.02)             # toma de contacto
    agacha(150, 20)                       # amortigua
    agacha(162, 0)
    _k(P["Head"], 150, rot=(6, 0, 0))
    _k(P["Head"], 162, rot=(0, 0, 0))
    # --- 171..230 derrota: se desinfla y baja la cabeza ----------------
    # lo que la lee como pena no es la cara (esa la pone el sprite) sino
    # que el pecho se cierre y los brazos cuelguen por delante
    _k(P["Spine"], 172, rot=(0, 0, 0)); _k(P["Head"], 172, rot=(0, 0, 0))
    _k(P["Spine"], 190, rot=(11, 0, 0))
    _k(P["Head"], 196, rot=(19, 0, 0))
    _k(P["Root"], 190, loc=(0, 0, -0.055))
    for n, sgn in (("UpperArm.L", 1), ("UpperArm.R", -1)):
        _k(P[n], 172, rot=(0, 0, 0))
        _k(P[n], 192, rot=(16, 0, 9 * sgn))
        _k(P[n], 214, rot=(12, 0, 7 * sgn))
        _k(P[n], 230, rot=(16, 0, 9 * sgn))
    _k(P["Spine"], 214, rot=(8, 0, 0)); _k(P["Head"], 214, rot=(15, 0, 0))
    _k(P["Root"], 214, loc=(0, 0, -0.045))
    _k(P["Spine"], 230, rot=(11, 0, 0)); _k(P["Head"], 230, rot=(19, 0, 0))
    _k(P["Root"], 230, loc=(0, 0, -0.055))

    for fc in _fcurves(act):
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = fin
    return act


def montar(con_animacion=True):
    rig = crear_armadura()
    puestas, huerfanas = colgar_piezas(rig)
    total = sum(puestas.values())
    print("[rig] %d huesos, %d piezas colgadas" % (len(HUESOS), total), flush=True)
    for h in sorted(puestas):
        print("   %-12s %d" % (h, puestas[h]), flush=True)
    if huerfanas:
        print("[rig] SIN HUESO (%d): %s" % (len(huerfanas), ", ".join(huerfanas[:12])),
              flush=True)
    if con_animacion:
        animar(rig)
        print("[rig] accion Fresita_Demo: respirar 1-60, saludar 61-110, "
              "saltar 111-170, derrota 171-230", flush=True)
    return rig


if __name__ == "__main__":
    montar()
    # el nombre sale del .blend abierto: asi vale para los tres del reparto
    base = Path(bpy.data.filepath).stem or "fresita"
    destino = str(OUT / ("%s_rig.blend" % base))
    bpy.ops.wm.save_as_mainfile(filepath=destino)
    print("BLEND", destino, flush=True)

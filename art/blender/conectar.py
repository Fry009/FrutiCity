"""Abre Blender listo para trabajar con Claude:
   - comprueba que la telemetria del addon sigue apagada
   - construye la fruta que toque
   - arranca el servidor MCP (lo mismo que el boton "Connect to Claude")
   - deja el visor en modo material y encuadrado
   - vigila los archivos: si Claude (o tu) guardais un modelo, se rehace solo

Para abrir otra fruta sin tocar nada: en la consola de Python de Blender,
    cargar("cohete")       # cualquiera de las trece, ver PIEZAS
    galeria()              # las trece a la vez, para comparar la familia
"""
import bpy, os, sys, runpy, builtins, traceback

AQUI = r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path: sys.path.insert(0, AQUI)

FRUTAS = ["manzana", "platano", "fresa", "naranja", "uvas", "kiwi"]
ESPECIALES = ["estrella", "moneda", "energia", "caja", "bomba", "cohete", "martillo"]
PIEZAS = FRUTAS + ESPECIALES
FRUTA = os.environ.get("FRUTICITY_FRUTA", "manzana")   # con la que arranca
COMUN = os.path.join(AQUI, "comun.py")


def ruta(nombre):
    return os.path.join(AQUI, "modelo_%s.py" % nombre)


# 1. telemetria: comprobar, no dar por hecho
try:
    p = bpy.context.preferences.addons["blender_mcp_addon"].preferences
    if p.telemetry_consent:
        p.telemetry_consent = False
        bpy.ops.wm.save_userpref()
    print("[claude] telemetria del addon:", p.telemetry_consent)
except Exception as e:
    print("[claude] no pude leer las preferencias del addon:", e)


def encuadrar():
    """Visor en color y centrado en lo que haya."""
    for area in bpy.context.screen.areas:
        if area.type != 'VIEW_3D': continue
        area.spaces[0].shading.type = 'MATERIAL'
        for region in area.regions:
            if region.type != 'WINDOW': continue
            with bpy.context.temp_override(area=area, region=region):
                bpy.ops.object.select_all(action='DESELECT')
                mallas = [o for o in bpy.context.scene.objects if o.type == 'MESH']
                for o in mallas: o.select_set(True)
                if mallas:
                    bpy.context.view_layer.objects.active = mallas[0]
                    bpy.ops.view3d.view_selected()


# 2. el modelo. _estado guarda que fruta esta puesta y con que fechas
_estado = {"fruta": None, "fechas": {}}


def _fecha(p):
    try: return os.path.getmtime(p)
    except OSError: return 0.0


def cargar(nombre):
    """Construye una fruta y pasa a vigilar sus archivos."""
    r = ruta(nombre)
    if not os.path.exists(r):
        print("[claude] no existe:", r, "| tengo:", ", ".join(PIEZAS))
        return
    try:
        runpy.run_path(r, run_name="__main__")
    except Exception:
        traceback.print_exc()
        return
    _estado["fruta"] = nombre
    _estado["fechas"] = {p: _fecha(p) for p in (r, COMUN)}
    encuadrar()
    print("[claude] puesta:", nombre)


def galeria():
    """Las seis a la vez. Sirve para ver si la familia casa, que es lo
    unico que no se puede juzgar mirando una fruta sola."""
    runpy.run_path(os.path.join(AQUI, "galeria.py"), run_name="__main__")


cargar(FRUTA)

# 3. el servidor MCP
try:
    bpy.ops.blendermcp.start_server()
    print("[claude] servidor MCP arrancado en el puerto",
          bpy.context.scene.blendermcp_port,
          "| corriendo:", bpy.context.scene.blendermcp_server_running)
except Exception as e:
    print("[claude] no arranco el servidor:", e)


# 4. vigilante: si se guarda el modelo activo O comun.py, se rehace la escena
def _tic():
    if _estado["fruta"]:
        for p, vieja in list(_estado["fechas"].items()):
            if _fecha(p) != vieja:
                cargar(_estado["fruta"])
                print("[claude] actualizado solo por", os.path.basename(p))
                break
    return 0.5


if not bpy.app.timers.is_registered(_tic):
    bpy.app.timers.register(_tic, persistent=True)

builtins.cargar = cargar
builtins.galeria = galeria
builtins.FRUTAS = FRUTAS
builtins.ESPECIALES = ESPECIALES
builtins.PIEZAS = PIEZAS
print("[claude] vigilante activo sobre el modelo y comun.py")
print("[claude] en la consola: cargar('cohete') | galeria() | PIEZAS =", PIEZAS)
print("[claude] LISTO")

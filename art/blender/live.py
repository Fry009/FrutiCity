"""Vigilante. Ejecutalo UNA vez en Blender (Scripting -> Run Script).
A partir de ahi, cada vez que Claude guarde modelo_manzana.py, la escena
se reconstruye sola en menos de un segundo. Para pararlo, cierra Blender.
"""
import bpy, os, runpy, traceback

RUTA = os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath or __file__)),
                    "modelo_manzana.py")
if not os.path.exists(RUTA):
    RUTA = r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender\modelo_manzana.py"

_estado = {"mtime": 0.0}

def _tic():
    try:
        m = os.path.getmtime(RUTA)
        if m != _estado["mtime"]:
            _estado["mtime"] = m
            try:
                runpy.run_path(RUTA, run_name="__main__")
                print("[live] reconstruido")
            except Exception:
                traceback.print_exc()       # un error no mata al vigilante
    except FileNotFoundError:
        pass
    return 0.5                              # vuelve a mirar en medio segundo

if bpy.app.timers.is_registered(_tic):
    bpy.app.timers.unregister(_tic)
bpy.app.timers.register(_tic, persistent=True)
print("[live] vigilando", RUTA)

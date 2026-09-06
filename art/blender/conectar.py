"""Abre Blender listo para trabajar con Claude:
   - comprueba que la telemetria del addon sigue apagada
   - construye la manzana
   - arranca el servidor MCP (lo mismo que el boton "Connect to Claude")
   - deja el visor en modo material y encuadrado
"""
import bpy, os, runpy

AQUI = r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"

# 1. telemetria: comprobar, no dar por hecho
try:
    p = bpy.context.preferences.addons["blender_mcp_addon"].preferences
    if p.telemetry_consent:
        p.telemetry_consent = False
        bpy.ops.wm.save_userpref()
    print("[claude] telemetria del addon:", p.telemetry_consent)
except Exception as e:
    print("[claude] no pude leer las preferencias del addon:", e)

# 2. el modelo
try:
    runpy.run_path(os.path.join(AQUI, "modelo_manzana.py"), run_name="__main__")
    print("[claude] manzana construida")
except Exception as e:
    print("[claude] fallo construyendo:", e)

# 3. el servidor MCP
try:
    bpy.ops.blendermcp.start_server()
    print("[claude] servidor MCP arrancado en el puerto",
          bpy.context.scene.blendermcp_port,
          "| corriendo:", bpy.context.scene.blendermcp_server_running)
except Exception as e:
    print("[claude] no arranco el servidor:", e)

# 4. visor en color y encuadrado
body = bpy.data.objects.get("Manzana")
for area in bpy.context.screen.areas:
    if area.type != 'VIEW_3D': continue
    area.spaces[0].shading.type = 'MATERIAL'
    for region in area.regions:
        if region.type != 'WINDOW': continue
        with bpy.context.temp_override(area=area, region=region):
            bpy.ops.object.select_all(action='DESELECT')
            if body:
                body.select_set(True)
                bpy.context.view_layer.objects.active = body
            bpy.ops.view3d.view_selected()
# 5. vigilante: si Claude guarda el modelo, la escena se rehace sola
import os as _os, runpy as _runpy, traceback as _tb
_RUTA = _os.path.join(AQUI, "modelo_manzana.py")
_st = {"m": _os.path.getmtime(_RUTA) if _os.path.exists(_RUTA) else 0.0}

def _tic():
    try:
        m = _os.path.getmtime(_RUTA)
        if m != _st["m"]:
            _st["m"] = m
            try:
                _runpy.run_path(_RUTA, run_name="__main__")
                print("[claude] modelo actualizado solo")
            except Exception:
                _tb.print_exc()
    except FileNotFoundError:
        pass
    return 0.5

bpy.app.timers.register(_tic, persistent=True)
print("[claude] vigilante activo: los cambios apareceran solos")
print("[claude] LISTO")

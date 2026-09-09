"""Abre Blender con Fresita ya montada y el servidor MCP escuchando.

Se lanza asi (el .blend va ANTES del --python, si no se carga despues del
script y se lleva por delante lo que el script haya hecho):

    blender art/blender/fresita_v5/fresita_rig.blend ^
            --python art/blender/abrir_fresita.py

Puerto 9876, que es el que busca blender-mcp.exe (el cliente que tiene
configurado Claude). El 9191 de arrancar_fresita.py era para opencode.
"""
import bpy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

PUERTO = 9876

# 1. telemetria del addon: comprobar y apagar
try:
    p = bpy.context.preferences.addons["blender_mcp_addon"].preferences
    if getattr(p, "telemetry_consent", False):
        p.telemetry_consent = False
        bpy.ops.wm.save_userpref()
except Exception as e:
    print("[abrir] prefs del addon:", e)

# 2. escena lista para animar
s = bpy.context.scene
s.name = "FrutiCity - Fresita"
s.render.fps = 30
s.frame_start, s.frame_end = 1, 170
s.frame_set(1)

# 3. visor en color y encuadrado sobre el personaje
for area in bpy.context.screen.areas:
    if area.type != 'VIEW_3D':
        continue
    area.spaces[0].shading.type = 'MATERIAL'
    for region in area.regions:
        if region.type != 'WINDOW':
            continue
        with bpy.context.temp_override(area=area, region=region):
            bpy.ops.object.select_all(action='DESELECT')
            mallas = [o for o in s.objects if o.type == 'MESH']
            for o in mallas:
                o.select_set(True)
            if mallas:
                bpy.context.view_layer.objects.active = mallas[0]
                bpy.ops.view3d.view_selected()
            bpy.ops.object.select_all(action='DESELECT')

# 4. el servidor MCP (equivale al boton "Connect to Claude" del panel)
try:
    s.blendermcp_port = PUERTO
    bpy.ops.blendermcp.start_server()
    print("[abrir] MCP escuchando en %d: %s"
          % (PUERTO, s.blendermcp_server_running), flush=True)
except Exception as e:
    print("[abrir] no pude arrancar el MCP:", e, flush=True)

print("[abrir] LISTO - dale al play para ver la accion Fresita_Demo", flush=True)

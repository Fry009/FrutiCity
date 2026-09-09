"""Arranque de Blender para trabajar con la Fresita por MCP:
   - limpia la escena a un estado neutro
   - puerto MCP 9191 (asi lo tiene opencode.json)
   - arranca el servidor del addon (equivalente a "Connect to Claude")
   - viewport en color MATERIAL y maximizado
"""
import bpy, os, sys

AQUI = r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# 1. telemetria del addon: comprobar y apagar
try:
    p = bpy.context.preferences.addons["blender_mcp_addon"].preferences
    if getattr(p, "telemetry_consent", False):
        p.telemetry_consent = False
        bpy.ops.wm.save_userpref()
except Exception as e:
    print("[arranque] addon prefs:", e)

# 2. escena limpia con nombre descriptivo
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
s = bpy.context.scene
s.name = "FrutiCity - Fresita"
s.frame_end = 120
s.render.fps = 30
s.render.engine = 'CYCLES'
s.cycles.samples = 48
s.cycles.use_denoising = True

# 3. MCP en 9191
try:
    s.blendermcp_port = 9191
    bpy.ops.blendermcp.start_server()
    print("[arranque] MCP server:", s.blendermcp_server_running)
except Exception as e:
    print("[arranque] fallo al arrancar MCP:", e)

# 4. viewport en material shading
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].shading.type = 'MATERIAL'
        area.spaces[0].shading.show_xray = False
        for region in area.regions:
            if region.type == 'WINDOW':
                region.show_mask_overlay = False

print("[arranque] LISTO")
"""Construye el modelo y saca master 512 + prueba real 128."""
import bpy, os, sys, runpy
AQUI = r"C:\Users\Fran\Desktop\Fran\FrutiCity\art\blender"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
TAG = argv[0] if argv else "rm"
runpy.run_path(os.path.join(AQUI, "modelo_manzana.py"), run_name="__main__")
S = bpy.context.scene
S.render.engine = 'CYCLES'; S.cycles.samples = 180; S.cycles.use_denoising = True
S.render.film_transparent = True
S.render.image_settings.file_format = 'PNG'
S.render.image_settings.color_mode = 'RGBA'
S.view_settings.view_transform = 'Standard'
for px in (512, 128):
    S.render.resolution_x = S.render.resolution_y = px
    S.render.filepath = os.path.join(AQUI, "tile_%s_%d.png" % (TAG, px))
    bpy.ops.render.render(write_still=True)
    print("RENDER", px)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(AQUI, "tile_%s.blend" % TAG))
print("OK")

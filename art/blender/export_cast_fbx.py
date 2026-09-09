import bpy
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'FrutiCity/Assets/FrutiCity/Resources/FrutiCast/Models'
for path in sorted((HERE/'reparto_v3').glob('*.blend')):
    bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.scene.frame_set(1)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.context.scene.objects:
        if ob.type in {'MESH','EMPTY'}:ob.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(OUT/(path.stem+'.fbx')),use_selection=True,object_types={'MESH','EMPTY'},
        axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_ALL',bake_space_transform=False,bake_anim=False,add_leaf_bones=False)

"""Small sculpted navigation props, rendered with the same fruit studio."""
import bpy,sys,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import comun as c
OUT=HERE/'personajes_v2';OUT.mkdir(exist_ok=True)
def box(name,dims,loc,mat):
    ob=c.caja(name,dims,loc,canto=.045,seg=4);ob.data.materials.append(mat);return ob
def build(kind):
    c.empezar()
    cream=c.mat('Cream',c.hexcol('FFF0CA'),.45)
    roof=c.mat('Coral',c.hexcol('ED654B'),.4,.2)
    blue=c.mat('Blue',c.hexcol('427EAC'),.4,.2)
    dark=c.mat('Brown',c.hexcol('805235'),.5)
    gold=c.mat('Gold',c.hexcol('FFC753'),.3,.25)
    box('Building',(1.05,.60,.86),(0,0,-.12),cream)
    box('Plinth',(1.20,.75,.13),(0,0,-.61),dark)
    box('Door',(.25,.08,.49),(.02,-.34,-.27),blue)
    for side in [-1,1]:box('Window',(.23,.08,.25),(.34*side,-.34,.05),gold)
    if kind=='nav_home':
        v=[(-.69,-.42,.29),(.69,-.42,.29),(0,-.42,.97),(-.69,.42,.29),(.69,.42,.29),(0,.42,.97)]
        mesh=bpy.data.meshes.new('Roof');mesh.from_pydata(v,[],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)]);mesh.update()
        ob=bpy.data.objects.new('Roof',mesh);bpy.context.scene.collection.objects.link(ob);ob.data.materials.append(roof);c._nace(ob);c.bisel(ob,.035,4)
        box('Chimney',(.19,.20,.43),(.35,.1,.70),dark)
        for x in [-.72,.71]:
            ob=c.esfera('Bush',.19,(x,-.05,-.46),seg=32,anillos=20);ob.data.materials.append(c.mat('Leaf',c.hexcol('70AC43'),.6))
    else:
        box('Roof',(1.16,.73,.14),(0,0,.39),roof)
        for i in range(6):
            ob=box('Awning stripe',(.19,.66,.12),(-.48+i*.19,-.30,.32),roof if i%2==0 else cream);ob.rotation_euler[0]=math.radians(12)
            ob=c.esfera('Scallop',1,(-.48+i*.19,-.63,.25),(.095,.10,.11),32,20);ob.data.materials.append(roof if i%2==0 else cream)
    c.CAM_LOC=(1.6,-8.6,2.4);c.terminar()
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True
    s.render.film_transparent=True;s.render.resolution_x=s.render.resolution_y=512;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard'
    s.render.filepath=str(OUT/(kind+'.png'));bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(kind+'.blend')));bpy.ops.render.render(write_still=True)
for kind in ['nav_home','nav_shop']:build(kind)

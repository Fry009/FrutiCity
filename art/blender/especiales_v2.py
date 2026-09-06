"""Original fruit-puzzle power-ups: citrus TNT, leaf propeller and prismatic orb."""
import bpy,sys,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import comun as c
OUT=HERE/'especiales_v2';OUT.mkdir(exist_ok=True)
for kind in ['tnt','propeller','orb']:
    c.empezar()
    mats=[c.mat(h,c.hexcol(h),.26,.3) for h in ['FA7452','FFD65B','68BC5C','61D6F2','A869E8','FFF3CB']]
    def ball(n,p,s,m):
        ob=c.esfera(n,1,p,s,48,32);ob.data.materials.append(m);return ob
    if kind=='tnt':
        for x in [-.45,0,.45]:
            ball('Citrus charge',(x,0,0),(.25,.29,.67),mats[0])
        for z in [-.30,.30]:
            ob=c.caja('Golden band',(1.5,.65,.16),(0,0,z),canto=.05,seg=4);ob.data.materials.append(mats[1])
        ball('Spark',(0,0,.98),(.17,.12,.17),mats[1])
        ob=c.caja('Fuse',(.07,.07,.3),(0,0,.75),canto=.03,seg=4);ob.data.materials.append(mats[5])
    elif kind=='propeller':
        for i in range(4):
            a=i*math.pi/2+.4
            ob=ball('Juice fan',(math.sin(a)*.48,0,math.cos(a)*.48),(.26,.12,.49),mats[2 if i%2==0 else 3]);ob.rotation_euler[1]=a
        ball('Hub',(0,-.16,0),(.28,.21,.28),mats[1]);ball('Hub shine',(-.06,-.35,.07),(.08,.03,.08),mats[5])
    else:
        ob=ball('Prismatic juice',(0,0,0),(.75,.75,.75),mats[4])
        for m in mats:ob.data.materials.append(m)
        for p in ob.data.polygons:p.material_index=1+int((math.atan2(p.center.x,p.center.z)+math.pi)/math.tau*5)%5
        for i in range(8):
            a=i*math.tau/8
            ball('Gold orbit',(math.cos(a)*.77,-.13,math.sin(a)*.77),(.095,.095,.095),mats[1])
    c.terminar();s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=40;s.cycles.use_denoising=True
    s.render.film_transparent=True;s.render.resolution_x=s.render.resolution_y=512;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard'
    s.render.filepath=str(OUT/('power_'+kind+'.png'));bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(kind+'.blend')));bpy.ops.render.render(write_still=True)

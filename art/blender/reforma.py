"""Original dollhouse sets. Identical camera across four renovation stages."""
import bpy, sys, math
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import comun as c
OUT=HERE/'reforma';OUT.mkdir(exist_ok=True)
def build(room):
    c.empezar(); groups=[[],[],[],[]]; stage=0
    def mat(n,h):return c.mat(n,c.hexcol(h),.48)
    cream=mat('Vanilla','FFE8BD');wood=mat('Honey oak','B98048');white=mat('Porcelain','FFF9E6');green=mat('Sage','57B7A0');pink=mat('Coral','F18379');blue=mat('Sky','9EDCE9');leaf=mat('Leaves','65A83C');gold=mat('Brass','E9B54B')
    def box(n,d,p,m,b=.07):
        ob=c.caja(n,d,p,canto=b,seg=4);ob.data.materials.append(m);groups[stage].append(ob);return ob
    def ball(n,p,s,m):
        ob=c.esfera(n,1,p,s,32,20);ob.data.materials.append(m);groups[stage].append(ob);return ob
    box('Foundation',(5.4,4.8,.3),(0,0,-.2),wood)
    for i in range(12):box('Floor plank',(5.15,.38,.07),(0,-2.1+i*.39,0),cream,.025)
    box('Back wall',(5.4,.18,2.9),(0,2.3,1.35),green if room==0 else blue if room==1 else pink)
    box('Left wall',(.18,4.65,2.9),(-2.6,0,1.35),cream)
    box('Window frame',(1.6,.17,1.6),(.7,2.15,1.8),white)
    box('Window glass',(1.4,.19,1.4),(.7,2.05,1.8),blue)
    box('Window cross',(.065,.24,1.45),(.7,1.95,1.8),white)
    box('Window cross',(1.45,.24,.065),(.7,1.95,1.8),white)
    box('Window sill',(1.85,.4,.12),(.7,1.94,.97),white)
    stage=1
    if room==0:
        for x in [-1.8,-.65,.5]:
            box('Kitchen cabinet',(1.1,.85,.94),(x,1.6,.5),green)
            box('Cabinet inset',(.91,.04,.70),(x,1.15,.48),cream)
            box('Handle',(.32,.1,.065),(x,1.08,.73),gold)
        box('Countertop',(3.5,1,.13),(-.65,1.6,1.02),white)
    elif room==1:
        box('Sofa base',(3,1.2,.45),(-.35,1.1,.4),green)
        box('Sofa back',(3,.33,1.05),(-.35,1.6,.83),green)
        for x in [-1.7,1]:box('Sofa arms',(.35,1.2,.75),(x,1.1,.65),green)
        for x in [-1.03,.30]:box('Cushions',(1.19,.92,.24),(x,1,.7),cream,.12)
    else:
        box('Bed frame',(2.3,3,.4),(-.7,.2,.4),wood)
        box('Headboard',(2.4,.25,1.5),(-.7,1.65,.85),green,.15)
        box('Mattress',(2.2,2.9,.3),(-.7,.15,.72),white,.16)
        box('Duvet',(2.23,1.85,.27),(-.7,-.4,.94),green,.16)
        for x in [-1.25,-.15]:box('Pillow',(.94,.65,.23),(x,1.05,.98),cream,.14)
    stage=2
    if room==0:
        box('Fridge',(1,1,1.95),(1.85,1.55,1),pink,.13)
        box('Freezer seam',(.92,.04,.035),(1.85,1.025,1.45),white)
        box('Fridge handle',(.07,.12,.5),(1.55,.98,.96),gold)
        box('Kitchen island',(2,1.1,.95),(-.4,-.75,.5),wood)
        box('Island top',(2.2,1.3,.14),(-.4,-.75,1.04),white)
    elif room==1:
        box('Rug',(3.4,2.1,.05),(.15,-.9,.1),pink,.2)
        box('Coffee table',(1.65,.95,.15),(.15,-.8,.62),wood,.15)
        for x in [-.45,.75]:box('Table legs',(.12,.65,.5),(x,-.8,.3),wood)
        box('Book',(.5,.4,.08),(.1,-.8,.75),blue)
    else:
        box('Desk',(1.35,.95,.12),(1.55,.95,.9),wood)
        for x in [1.05,2.05]:box('Desk legs',(.1,.7,.85),(x,.95,.44),wood)
        box('Notebook',(.5,.45,.06),(1.5,.9,1),pink)
    stage=3
    for x,y in [(-2,-1.6),(2,-1.3)]:
        ball('Plant pot',(x,y,.34),(.27,.27,.32),pink)
        for i in range(5):
            a=i*math.tau/5
            ob=ball('Plant foliage',(x+.17*math.cos(a),y+.17*math.sin(a),.8),(.17,.16,.4),leaf)
            ob.rotation_euler[1]=.45*math.cos(a)
    box('Wall picture',(.14,1,1.1),(-2.45,.4,1.85),wood)
    box('Picture art',(.16,.83,.9),(-2.35,.4,1.85),pink)
    ball('Picture sun',(-2.25,.4,2),(.07,.21,.21),gold)
    c.luces();cam=c.camara((0,0,1));cam.data.type='ORTHO';cam.data.ortho_scale=8.2
    cam.location=(8,-11,9);cam.rotation_mode='QUATERNION';cam.rotation_quaternion=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y')
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
    s.render.film_transparent=True;s.render.resolution_x=s.render.resolution_y=1024;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard'
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/('room_'+str(room)+'.blend')))
    for unlocked in range(4):
        for j,obs in enumerate(groups):
            for ob in obs:ob.hide_render=j>unlocked
        s.render.filepath=str(OUT/('room_'+str(room)+'_'+str(unlocked)+'.png'));bpy.ops.render.render(write_still=True)
for room in range(3):build(room)

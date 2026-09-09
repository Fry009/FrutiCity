"""Articulated FrutiCity cast: native Blender masters, FBX rigs and portraits.
blender --background --python art/blender/reparto_v3.py -- mona pablo fresi nora pina sandi
No external models, textures, soundfonts or image generation required.
"""
import bpy, math, sys, json
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'FrutiCity/Assets/FrutiCity/Resources/FrutiCast'
MASTER=HERE/'reparto_v3'
for folder in [OUT/'Models', OUT/'Portraits', MASTER]: folder.mkdir(parents=True,exist_ok=True)
NAMES=['mona','pablo','fresi','nora','pina','sandi']
COLORS=['D94338','F2CB45','CF365C','F49B30','DCAD43','57914A']

def material(name,color,rough=.45):
    mat=bpy.data.materials.new(name+'_'+color);mat.diffuse_color=tuple(int(color[i:i+2],16)/255 for i in (0,2,4))+(1,)
    mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=tuple(v**2.2 for v in mat.diffuse_color[:3])+(1,)
    p.inputs['Roughness'].default_value=rough
    return mat

def parent(ob,par):
    if par:
        bpy.context.view_layer.update();m=ob.matrix_world.copy();ob.parent=par;ob.matrix_world=m
    return ob

def pivot(name,loc,par=None):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob.location=loc
    return parent(ob,par)

def ball(name,loc,scale,mat,par=None,seg=24,rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1,location=loc)
    ob=bpy.context.object;ob.name=name;ob.scale=scale;ob.data.materials.append(mat)
    for f in ob.data.polygons:f.use_smooth=True
    return parent(ob,par)

def tube(name,points,radius,mat,par=None):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=12
    curve.bevel_depth=radius;curve.bevel_resolution=2
    spline=curve.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
    for point,co in zip(spline.bezier_points,points):point.co=co;point.handle_left_type=point.handle_right_type='AUTO'
    ob=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(ob);curve.materials.append(mat)
    return parent(ob,par)

def box(name,loc,size,mat,par=None,bevel=.055):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);ob=bpy.context.object;ob.name=name;ob.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mod=ob.modifiers.new('Soft tailored edges','BEVEL');mod.width=bevel;mod.segments=3
    ob.modifiers.new('Weighted normals','WEIGHTED_NORMAL');ob.data.materials.append(mat)
    return parent(ob,par)

def leaf(name,origin,length,width,angle,mat,par):
    verts=[];faces=[]
    for i in range(13):
        t=i/12;spread=width*math.sin(math.pi*t)**.7
        for side in [-1,0,1]:
            x=side*spread;z=length*t;y=.14*math.sin(math.pi*t)+(abs(side)*.04)
            verts.append((origin[0]+x*math.cos(angle)+z*math.sin(angle),origin[1]+y,origin[2]-x*math.sin(angle)+z*math.cos(angle)))
    for i in range(12):
        for j in range(2):a=i*3+j;faces.append((a,a+1,a+4,a+3))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob);mesh.materials.append(mat)
    sol=ob.modifiers.new('Leaf thickness','SOLIDIFY');sol.thickness=.015
    for f in mesh.polygons:f.use_smooth=True
    return parent(ob,par)

def bodymesh(kind,skin,stripe,par):
    verts=[];faces=[];rows=36;cols=48
    for i in range(rows+1):
        t=i/rows;phi=math.pi*t
        for j in range(cols):
            theta=2*math.pi*j/cols
            if kind=='pablo':
                r=.035+.29*math.sin(phi)**.5
                verts.append((.48*math.sin(phi)-.2+r*math.cos(theta)*(1+.10*math.cos(theta*3)),r*.8*math.sin(theta),.66+1.94*t))
                continue
            r=math.sin(phi)
            z=.83*math.cos(phi)
            if kind=='mona':
                r=r**.77*.84*(1+.024*math.cos(theta*5)*math.sin(phi));z-=.17*math.exp(-(r/.36)**2)*(1 if z>0 else -.65)
            elif kind=='fresi':r=r**.83*(.75+.20*math.cos(phi));z=.87*math.cos(phi)
            elif kind=='pina':r=r**.63*.68;z=.97*math.cos(phi)
            elif kind=='sandi':r*=.87;z=.92*math.cos(phi)
            else:r*=.77;z*=.96
            verts.append((r*math.cos(theta),r*.83*math.sin(theta),1.57+z))
    for i in range(rows):
        for j in range(cols):faces.append((i*cols+j,i*cols+(j+1)%cols,(i+1)*cols+(j+1)%cols,(i+1)*cols+j))
    mesh=bpy.data.meshes.new('Sculpted fruit silhouette');mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new('FruitSkin',mesh);bpy.context.collection.objects.link(ob);mesh.materials.append(skin);mesh.materials.append(stripe)
    for polygon in mesh.polygons:
        polygon.use_smooth=True
        if kind=='sandi' and polygon.index%cols%8<3:polygon.material_index=1
        if kind=='pablo' and (polygon.index//cols<2 or polygon.index//cols>33):polygon.material_index=1
    return parent(ob,par)

def build(kind):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    idx=NAMES.index(kind)
    skin=material('Skin',COLORS[idx],.37);green=material('Leaf','3C7150');dark=material('Ink','282D3A');cream=material('Linen','F0E4CF',.65)
    leather=material('Leather','805748',.6);navy=material('Denim','34495C',.64);gold=material('Brass','DDBD6E',.28)
    white=material('Eye','F7F2E7',.28);iris=material('Iris','526754',.32);pink=material('Mouth','8E3845');stripe=material('Stripe','2E6344' if kind=='sandi' else '835331')
    outfit=material('Outfit',['E8D6B6','386E79','705371','E9E6D9','455365','3D5668'][idx],.65)
    rig=pivot('Rig',(0,0,0));body=pivot('BodyPivot',(0,0,1.57),rig)
    fruit=bodymesh(kind,skin,stripe,body)
    bpy.context.view_layer.update()
    def surface(x,z):
        inv=fruit.matrix_world.inverted();hit,p,_,_=fruit.ray_cast(inv@Vector((x,-4,z)),Vector((0,1,0)))
        return (fruit.matrix_world@p).y if hit else (-.26 if kind=='pablo' else -.58)
    fx=.22 if kind=='pablo' else 0;fz=1.77;spacing=.135 if kind=='pablo' else .235
    for side,suffix in [(-1,'L'),(1,'R')]:
        x=fx+spacing*side;y=surface(x,fz)-.022
        eye=pivot('Eye'+suffix,(x,y,fz),body)
        ball('Sclera',(x,y,fz),(.125 if kind=='pablo' else .155,.055,.122),white,eye)
        ball('Iris',(x+.015,y-.050,fz),(.066,.025,.085),iris,eye)
        ball('Pupil',(x+.017,y-.072,fz),(.036,.013,.062),dark,eye)
        ball('Catchlight',(x-.005,y-.084,fz+.033),(.018,.01,.023),white,eye,12,8)
        brow=pivot('Brow'+suffix,(x,y-.01,fz+.21),body)
        tube('Expressive brow',[(x-.13,y+.01,fz+.21),(x,y-.024,fz+.245+(side*.015)),(x+.13,y+.01,fz+.225)],.026,dark,brow)
        # Deliberately smaller eyes, sculpted upper lids, asymmetrical brows and a closed smirk.
        tube('Upper lid',[(x-.13,y-.012,fz+.045),(x,y-.04,fz+.11),(x+.13,y-.012,fz+.058)],.018,skin,body)
    mz=1.48;my=surface(fx,mz)-.045
    smile=pivot('Smile',(fx,my,mz),body)
    tube('Half smile',[(fx-.14,my+.018,mz+.015),(fx,my-.007,mz-.047),(fx+.17,my+.012,mz+.055)],.021,dark,smile)
    sad=pivot('SadMouth',(fx,my-.001,mz),body)
    tube('Rueful smile',[(fx-.13,my+.012,mz-.035),(fx,my-.006,mz+.018),(fx+.13,my+.012,mz-.018)],.019,dark,sad)
    sad.scale=(.001,.001,.001)
    mouth=pivot('OpenMouth',(fx,my-.01,mz),body)
    ball('Smile inside',(fx,my,mz),(.14,.022,.086),dark,mouth)
    ball('Teeth',(fx,my-.022,mz+.04),(.102,.009,.024),cream,mouth,16,8)
    mouth.scale=(.001,.001,.001)
    # Real limb pivots: upper arm, elbow, wrist, hip and foot, with distinct hands/shoes.
    shoulder=.47 if kind=='pablo' else .76
    for side,suffix in [(-1,'L'),(1,'R')]:
        sx=side*shoulder;sz=1.58
        arm=pivot('Arm'+suffix,(sx,0,sz),body)
        ball('Tailored sleeve',(sx+side*.045,.01,sz-.07),(.15,.16,.22),outfit,arm)
        tube('Upper arm',[(sx,0,sz-.06),(sx+side*.15,-.01,sz-.24),(sx+side*.18,-.05,sz-.38)],.078,skin,arm)
        elbow=pivot('Elbow'+suffix,(sx+side*.18,-.05,sz-.38),arm)
        tube('Forearm',[(sx+side*.18,-.05,sz-.38),(sx+side*.20,-.15,sz-.48),(sx+side*.17,-.23,sz-.54)],.073,skin,elbow)
        wrist=pivot('Hand'+suffix,(sx+side*.17,-.23,sz-.54),elbow)
        ball('Palm',(sx+side*.17,-.23,sz-.56),(.11,.085,.13),skin,wrist)
        for finger in range(3):ball('Finger',(sx+side*.17+(finger-1)*.052,-.255,sz-.65),(.033,.055,.071),skin,wrist,12,8)
        ball('Thumb',(sx+side*.075,-.27,sz-.56),(.052,.059,.075),skin,wrist,12,8)
        hx=side*(.24 if kind=='pablo' else .31)
        leg=pivot('Leg'+suffix,(hx,.025,.81),rig)
        tube('Trouser leg',[(hx,.025,.81),(hx+side*.014,0,.50),(hx+side*.025,-.04,.31)],.095,navy,leg)
        foot=pivot('Foot'+suffix,(hx+side*.025,-.08,.22),leg)
        ball('Shoe upper',(hx+side*.025,-.15,.22),(.185,.29,.15),leather,foot)
        ball('Rubber sole',(hx+side*.025,-.16,.12),(.19,.29,.055),cream,foot)
        tube('Shoe seam',[(hx-.12,-.28,.28),(hx,-.36,.29),(hx+.12,-.28,.28)],.012,cream,foot)
    # Profession-specific tailoring/accessories, not six reskins of the same cylinder.
    if kind=='mona':
        ball('Apron bib',(0,-.57,1.12),(.45,.07,.28),cream,body)
        for side in [-1,1]:tube('Apron strap',[(side*.31,surface(side*.31,1.40)-.012,1.40),(side*.33,surface(side*.33,1.25)-.012,1.25),(side*.25,-.60,1.10)],.021,cream,body)
        for z in [1.07,1.2]:ball('Apron button',(.10,-.65,z),(.026,.016,.026),gold,body,12,8)
        ball('Chef hat band',(-.07,.015,2.32),(.50,.44,.10),cream,body)
        for x,z in [(-.28,2.54),(.02,2.64),(.27,2.51)]:ball('Chef toque',(x,0,z),(.27,.31,.22),cream,body)
    elif kind=='pablo':
        box('Messenger bag',(-.32,.25,1.54),(.51,.43,.70),navy,body,.11)
        tube('Shoulder strap',[(-.36,-.08,2.06),(-.39,-.24,1.72),(-.36,-.20,1.38)],.035,leather,body)
        ball('Courier cap',(-.09,0,2.52),(.34,.29,.15),outfit,body)
        ball('Cap brim',(-.07,-.30,2.46),(.36,.25,.038),outfit,body)
        box('Brass badge',(-.07,-.276,2.54),(.12,.018,.07),gold,body,.014)
    elif kind=='fresi':
        for i in range(6):leaf('Calyx',(0,0,2.30),.49,.17,(i-2.5)*.65,green,body)
        for row,z in enumerate([1.0,1.22,1.55,1.96,2.16]):
            for x in [-.58,-.39,.39,.58]:
                yy=surface(x,z)
                if yy<-.30:ball('Embedded seed',(x,yy+.004,z),(.018,.018,.044),gold,body,12,8)
        for side in [-1,1]:ball('Jacket panel',(side*.49,-.36,1.12),(.20,.08,.29),outfit,body)
        ball('Ear stud',(.72,-.2,1.69),(.04,.03,.04),gold,body,16,10)
        phone=box('Phone',(.94,-.34,1.03),(.15,.04,.26),dark,bpy.data.objects.get('HandR'),.028)
        box('Phone screen',(.94,-.368,1.03),(.115,.015,.20),outfit,phone,.012)
    elif kind=='nora':
        for side in [-1,1]:
            ball('Coat panel',(side*.43,-.44,1.12),(.23,.10,.35),cream,body)
            lapel=box('Coat lapel',(side*.29,-.58,1.34),(.12,.055,.34),white,body,.018);lapel.rotation_euler[1]=side*.28
        tube('Stethoscope',[(-.31,-.60,1.49),(-.28,-.69,1.15),(0,-.72,1.01),(.28,-.69,1.15),(.31,-.60,1.49)],.023,navy,body)
        ball('Stethoscope bell',(0,-.74,1.0),(.07,.02,.07),gold,body)
        leaf('Orange leaf',(.06,0,2.33),.58,.17,.85,green,body)
    elif kind=='pina':
        for i in range(9):leaf('Pineapple crown',(0,.06+(i%2)*.05,2.45),.63+(i%3)*.09,.13,(i-4)*.22,green,body)
        for z in [.92,1.12,1.36,1.98,2.18]:
            for x in [-.5,-.3,-.1,.1,.3,.5]:
                if 1.3<z<2 and abs(x)<.4:continue
                yy=surface(x,z)
                if yy<-.25:
                    s=ball('Pineapple diamond',(x,yy+.013,z),(.058,.026,.087),gold,body,12,8);s.rotation_euler[1]=.65
        tube('Headphone band',[(-.73,0,1.94),(-.65,.04,2.41),(0,.06,2.62),(.65,.04,2.41),(.73,0,1.94)],.053,navy,body)
        for side in [-1,1]:
            ball('Headphone cup',(side*.73,-.01,1.95),(.14,.22,.25),navy,body)
            ball('Cup accent',(side*.82,-.055,1.95),(.035,.16,.16),gold,body)
            ball('Bomber jacket',(side*.45,-.37,1.10),(.22,.08,.28),outfit,body)
    else:
        ball('Overall bib',(0,-.64,1.04),(.43,.055,.30),navy,body)
        for side in [-1,1]:
            tube('Overall strap',[(side*.39,-.45,1.46),(side*.35,-.68,1.21),(side*.28,-.69,1.04)],.044,navy,body)
            ball('Buckle',(side*.29,-.72,1.14),(.035,.018,.045),gold,body,12,8)
        tube('Tool belt',[(-.59,-.28,.98),(-.40,-.58,.92),(0,-.68,.9),(.40,-.58,.92),(.59,-.28,.98)],.055,leather,body)
        box('Tool pouch',(.49,-.50,.87),(.23,.10,.25),leather,body)
        tube('Hammer handle',[(.52,-.57,1.12),(.52,-.57,.83)],.022,gold,body)
        box('Hammer head',(.52,-.57,1.15),(.16,.07,.07),navy,body,.012)
        ball('Hard hat dome',(0,.02,2.43),(.63,.53,.19),gold,body)
        ball('Hard hat brim',(0,-.08,2.34),(.70,.64,.038),gold,body)
    # Convert curves and modifiers, then merge static geometry per rigid group/material.
    for ob in list(bpy.context.scene.objects):
        if ob.type not in {'MESH','CURVE'}:continue
        bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
        bpy.ops.object.convert(target='MESH')
    groups={}
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH':groups.setdefault(ob.parent,[]).append(ob)
    for par,objects in groups.items():
        if len(objects)<2:continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in objects:ob.select_set(True)
        bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();objects[0].name=par.name+'_Geometry'
    # Export the neutral articulated model. Unity owns real-time gesture timing.
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.fbx(filepath=str(OUT/'Models'/f'{kind}.fbx'),use_selection=True,object_types={'MESH','EMPTY'},
        axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_ALL',bake_space_transform=False,bake_anim=False,add_leaf_bones=False)
    # Native editable performance blocking, with named timeline markers.
    scene=bpy.context.scene;scene.render.fps=30;scene.frame_end=240
    for name,frame in [('IDLE',1),('VICTORY',70),('DEFEAT',160),('READY_AGAIN',220)]:scene.timeline_markers.new(name,frame=frame)
    for name in ['BodyPivot','ArmL','ArmR']:
        ob=bpy.data.objects[name];base=ob.location.copy()
        for frame,lift,lean in [(1,0,0),(30,.026,0),(60,0,0),(70,-.08,.06),(82,.33,-.06),(96,0,.03),(120,.05,0),(150,0,0),(160,0,0),(178,-.10,.13),(200,-.07,.07),(220,0,-.03),(240,0,0)]:
            ob.location=base+Vector((0,0,lift if name=='BodyPivot' else 0));ob.rotation_euler=(lean,0,0)
            if name.startswith('Arm') and 78<=frame<=120:ob.rotation_euler[1]=(1 if name=='ArmL' else -1)*1.7
            ob.keyframe_insert('location',frame=frame);ob.keyframe_insert('rotation_euler',frame=frame)
    scene.frame_set(1)
    world=bpy.data.worlds.new('Warm studio');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.36,.42,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
    for name,loc,power,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-2,3),230,3),('Rim',(1,3,5),550,3)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
        light=bpy.data.objects.new(name,data);scene.collection.objects.link(light);light.location=loc;light.rotation_euler=(Vector((0,0,1.5))-light.location).to_track_quat('-Z','Y').to_euler()
    data=bpy.data.cameras.new('PortraitCamera');camera=bpy.data.objects.new('PortraitCamera',data);scene.collection.objects.link(camera)
    camera.location=(.35,-8,3.0);camera.rotation_euler=(Vector((0,0,1.57))-camera.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=3.6;scene.camera=camera
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
    scene.render.resolution_x=scene.render.resolution_y=512;scene.render.resolution_percentage=100
    scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.view_transform='AgX';scene.render.filepath=str(OUT/'Portraits'/f'{kind}.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(MASTER/f'{kind}.blend'))
    bpy.ops.render.render(write_still=True)
    stats={'character':kind,'vertices':sum(len(o.data.vertices) for o in scene.objects if o.type=='MESH'),'mesh_groups':sum(o.type=='MESH' for o in scene.objects)}
    print('FRUTI_CAST '+json.dumps(stats),flush=True)

if __name__=='__main__':
    names=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else NAMES
    for name in names:build(name)

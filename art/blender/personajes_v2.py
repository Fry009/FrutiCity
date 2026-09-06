"""FrutiCity: expressive 3D cast, authored geometry + reusable squash rig.
blender --background --python art/blender/personajes_v2.py -- naranja manzana ...
Native .blend masters and transparent 768 px renders; existing fruit masters stay intact.
"""
import bpy, sys, math, os, importlib
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import comun as c
OUT=HERE/'personajes_v2'
OUT.mkdir(exist_ok=True)

def ball(name,loc,scale,material):
    ob=c.esfera(name,1,loc,scale,48,32)
    ob.data.materials.append(material)
    c.suave(ob,1)
    return ob

def build(kind):
    importlib.reload(c)
    c.empezar()
    skin=c.mat('Fruit candy',c.hexcol({'naranja':'FF9D25','manzana':'EF4948','fresa':'EF4257','platano':'FFD344','uvas':'6762C8','kiwi':'93C83F'}[kind]),.40,.24)
    leaf=c.mat('Fresh leaves',c.hexcol('438D24'),.43,.12)
    dark=c.mat('Warm chocolate',c.hexcol('382019'),.3,.25)
    light=c.mat('Eye catchlights',c.hexcol('FFF8E7'),.2,.2)
    blush=c.mat('Soft cheeks',c.hexcol('FA8265'),.6)
    pink=c.mat('Happy tongue',c.hexcol('FF7191'),.4)
    shoes=c.mat('Tiny shoes',c.hexcol('96582B'),.55)
    if kind=='fresa':
        profile=[(math.sin(math.pi*i/64)**.82*(.94+.22*math.cos(math.pi*i/64)),.83*math.cos(math.pi*i/64)) for i in range(65)]
        body=c.revolucion(profile,.82,80,'Strawberry body')
        body.data.materials.append(skin); c.suave(body,2)
        for i in range(6):
            angle=i*60
            c.hoja_puesta(leaf,(0,0,.76),(65,-32,angle),largo=.67,ancho=.19)
        seed=c.mat('Seeds',c.hexcol('FFC574'),.5)
        for x,z in [(-.58,.24),(.58,.24),(-.43,-.25),(.43,-.25),(-.24,.53),(.24,.53),(-.21,-.60),(.21,-.60)]:
            ball('Seed',(x,-.52,z),(.024,.021,.048),seed)
    elif kind=='platano':
        mod=importlib.import_module('modelo_platano')
        mod.GORDO=.42;mod.ABRE=100
        body=mod.cuerpo();body.data.materials.append(skin);body.data.materials.append(shoes)
        body.rotation_euler[1]=math.radians(-78);c.suave(body,2)
    else:
        body=ball('Fruit body',(0,0,0),(.83,.69,.80 if kind!='uvas' else .70),skin)
        if kind=='manzana':
            mod=importlib.import_module('modelo_manzana')
            bpy.data.objects.remove(body,do_unlink=True)
            body=c.revolucion(mod.perfil(),.84,80,'Apple body');body.data.materials.append(skin);c.suave(body,2)
        c.tallo(shoes,(0,0,.82),alto=.25,r_base=.057,r_punta=.045)
        c.hoja_puesta(leaf,(0,0,.78),(65,-28,10),largo=.77,ancho=.24)
        c.hoja_puesta(leaf,(-.03,.01,.79),(75,-35,160),largo=.51,ancho=.19)
        if kind=='uvas':
            for x,z in [(-.59,-.22),(.59,-.22),(-.36,-.61),(.36,-.61)]:
                ball('Grape',(x,.10,z),(.33,.34,.34),skin)
    bpy.context.view_layer.update()
    # Raycast against the evaluated body: eyes follow the real surface, never float.
    evaluated=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    def surface(x,z):
        inv=body.matrix_world.inverted()
        hit,point,normal,_=evaluated.ray_cast(inv@Vector((x,-4,z)),(inv.to_3x3()@Vector((0,1,0))).normalized())
        return (body.matrix_world@point).y if hit else -.60
    face_z=-.04 if kind=='platano' else .05
    spacing=.19 if kind=='platano' else .265
    eye=.11 if kind=='platano' else .13
    for side in [-1,1]:
        x=spacing*side; z=face_z+.14; y=surface(x,z)-.028
        if kind=='naranja' and side==1:
            points=[(x+(i/24-.5)*.25,y-.025,z+.07*math.sin(i/24*math.pi)) for i in range(25)]
            wink=c.cuerda('Playful wink',points,.028);wink.data.materials.append(dark)
        else:
            ball('Eye',(x,y,z),(eye,.085,eye*1.28),dark)
            ball('Catchlight',(x-.032,y-.081,z+.045),(.035,.022,.043),light)
            ball('Small catchlight',(x+.035,y-.080,z-.034),(.014,.012,.016),light)
        bx=x+side*.11; bz=face_z-.07
        ball('Blush',(bx,surface(bx,bz)-.05,bz),(.105,.035,.062),blush)
        pts=[]
        for i in range(16):
            dx=(i/15-.5)*.20; zz=z+.245+.033*math.sin(i/15*math.pi)
            pts.append((x+dx,surface(x+dx,zz)-.033,zz))
        ob=c.cuerda('Eyebrow',pts,.018);ob.data.materials.append(shoes)
    mouthz=face_z-.22; mouthy=surface(0,mouthz)-.024
    outline=[]
    for i in range(25):
        u=i/24;x=(u*2-1)*.205;z=mouthz+.065-.025*math.sin(u*math.pi)
        outline.append((x,surface(x,z)-.024,z))
    for i in range(25):
        u=1-i/24;x=(u*2-1)*.205;z=mouthz+.065-.225*math.sin(u*math.pi)
        outline.append((x,surface(x,z)-.026,z))
    centerz=mouthz-.035
    outline=[(x,y-.035,z) for x,y,z in outline]
    vertices=[(0,surface(0,centerz)-.065,centerz)]+outline
    faces=[(0,i+1,(i+1)%len(outline)+1) for i in range(len(outline))]
    mesh=bpy.data.meshes.new('Happy smile');mesh.from_pydata(vertices,[],faces);mesh.update()
    smile=bpy.data.objects.new('Happy smile',mesh);bpy.context.scene.collection.objects.link(smile);smile.data.materials.append(dark);c._nace(smile)
    tonguez=mouthz-.105
    ball('Tongue',(.012,surface(0,tonguez)-.082,tonguez),(.095,.018,.037),pink)
    # Rounded arms and feet communicate character even at tile size.
    for side in [-1,1]:
        x=(.59 if kind=='fresa' else .43 if kind=='platano' else .78)*side
        hand=ball('Little arm',(x,-.02,-.25),(.13,.17,.26),skin)
        hand.rotation_euler[1]=side*math.radians(30)
        ball('Shoe',(.30*side,-.12,-.87),(.20,.29,.12),shoes)
    if kind=='naranja':
        bag=c.mat('Adventure backpack',c.hexcol('385779'),.6)
        for side in [-1,1]:
            ball('Backpack pocket',(.70*side,.20,-.31),(.20,.32,.36),bag)
            ball('Shoulder strap',(.62*side,-.45,-.29),(.066,.045,.24),shoes)
    # A real animation root saved in the Blender master.
    rig=bpy.data.objects.new('Fruit_Squash_Rig',None);bpy.context.scene.collection.objects.link(rig)
    for ob in list(c._vivos()): ob.parent=rig
    for frame,scale,z in [(1,(1,1,1),0),(15,(.96,.96,1.065),.035),(30,(1.065,1.065,.93),0),(45,(.98,.98,1.025),.015),(60,(1,1,1),0)]:
        rig.scale=scale;rig.location.z=z;rig.keyframe_insert('scale',frame=frame);rig.keyframe_insert('location',frame=frame)
    scene=bpy.context.scene;scene.frame_end=60;scene.render.fps=30;scene.frame_set(1)
    c.CAM_LOC=(0,-9,1.65);c.MARGEN=.13
    c.LUZ_CLAVE=280;c.LUZ_PUNTO=110;c.LUZ_RELLENO=130;c.LUZ_CONTRA=180
    c.terminar()
    scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
    scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.resolution_x=scene.render.resolution_y=768;scene.render.resolution_percentage=100
    scene.view_settings.view_transform='Standard';scene.render.filepath=str(OUT/(kind+'.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(kind+'.blend')))
    bpy.ops.render.render(write_still=True)
    print('FRUTI_DONE',kind,flush=True)

if __name__=='__main__':
    names=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['naranja','manzana','fresa','platano','uvas','kiwi']
    for name in names: build(name)

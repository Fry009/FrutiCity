"""Fruit soap-opera cast: integrated almond eyes, tailored silhouettes, articulated faces.
Run Blender -b --python art/blender/reparto_v4.py -- mona nora ...
"""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import reparto_v3 as r
import bpy
from mathutils import Vector

def patch_surface(name, outline, surface, mat, par, offset=.025):
    cx=sum(p[0] for p in outline)/len(outline);cz=sum(p[1] for p in outline)/len(outline)
    verts=[(cx,surface(cx,cz)-offset,cz)]+[(x,surface(x,z)-offset,z) for x,z in outline]
    faces=[(0,i+1,(i+1)%len(outline)+1) for i in range(len(outline))]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob);mesh.materials.append(mat)
    for f in mesh.polygons:f.use_smooth=True
    return r.parent(ob,par)

def build(kind):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    idx=r.NAMES.index(kind);female=idx in [0,2,3]
    skin=r.material('Skin',['EC4339','FFD046','EF4059','FFA025','EFBE39','65AE45'][idx],.31)
    ink=r.material('Ink','38231F',.30);white=r.material('Eye','FFF4DA',.25)
    iris=r.material('Iris','80482C',.25);green=r.material('Leaf','38812D',.42)
    gold=r.material('Gold','EABD56',.22);pink=r.material('Lip','B73744',.40)
    cloth=r.material('Outfit',['F3E5D4','246A73','B63167','F4E8CC','267B73','3B755A'][idx],.62)
    pants=r.material('Trousers',['443544','D5B98F','B63167','E9DCC1','465C3E','3B755A'][idx],.62)
    sole=r.material('Shoe','664132',.43);stripe=r.material('Stripe','387235' if kind=='sandi' else '91632C')
    rig=r.pivot('Rig',(0,0,0));body=r.pivot('BodyPivot',(0,0,1.50),rig)
    head=r.pivot('HeadPivot',(0,0,1.57),body)
    fruit=r.bodymesh(kind,skin,stripe,head);bpy.context.view_layer.update()
    def surface(x,z):
        hit,p,_,_=fruit.ray_cast(fruit.matrix_world.inverted()@Vector((x,-4,z)),Vector((0,1,0)))
        return (fruit.matrix_world@p).y if hit else -.25
    fx=.23 if kind=='pablo' else 0;fz=1.70;space=.135 if kind=='pablo' else .28
    width=.13 if kind=='pablo' else .205
    for side,suffix in [(-1,'L'),(1,'R')]:
        x=fx+space*side;eye=r.pivot('Eye'+suffix,(x,surface(x,fz),fz),head)
        outline=[]
        for i in range(25):
            u=i/24;outline.append((x+(u*2-1)*width,fz+.11*math.sin(u*math.pi)+side*(u-.5)*.035))
        for i in range(25):
            u=1-i/24;outline.append((x+(u*2-1)*width,fz-.105*math.sin(u*math.pi)+side*(u-.5)*.035))
        patch_surface('Almond eye',outline,surface,white,eye,.032)
        ix=x+.027;iy=surface(ix,fz)
        r.ball('Iris',(ix,iy-.043,fz),(.079,.023,.094),iris,eye,32,20)
        r.ball('Pupil',(ix,iy-.063,fz),(.044,.012,.067),ink,eye,24,16)
        r.ball('Eye light',(ix-.025,iy-.077,fz+.038),(.020,.007,.025),white,eye,16,10)
        upper=outline[:25]
        r.tube('Sculpted eyelid',[(xx,surface(xx,zz)-.052,zz) for xx,zz in upper],.022,skin,eye)
        if female:
            r.tube('Lash line',[(xx,surface(xx,zz)-.056,zz+.007) for xx,zz in upper],.012,ink,eye)
            for j in range(3):
                xx=x+side*(width-.018-j*.031);zz=fz+.04+j*.02
                r.tube('Eyelash',[(xx,surface(xx,zz)-.052,zz),(xx+side*.045,surface(xx,zz)-.07,zz+.048)],.009,ink,eye)
        brow=r.pivot('Brow'+suffix,(x,surface(x,fz+.23),fz+.23),head)
        points=[]
        for i in range(15):
            u=i/14;xx=x+(u*2-1)*width;zz=fz+.24+.06*math.sin(u*math.pi)+(.035*u if side==1 else -.02*u)
            points.append((xx,surface(xx,zz)-.022,zz))
        r.tube('Expressive brow',points,.022 if female else .032,ink,brow)
    mz=1.36;mw=.13 if kind=='pablo' else .245
    smile=r.pivot('Smile',(fx,surface(fx,mz),mz),head)
    outline=[]
    for i in range(25):
        u=i/24;outline.append((fx+(u*2-1)*mw,mz+.045+.045*u-.03*math.sin(u*math.pi)))
    for i in range(25):
        u=1-i/24;outline.append((fx+(u*2-1)*mw,mz+.045+.045*u-.155*math.sin(u*math.pi)))
    patch_surface('Warm smile',outline,surface,ink,smile,.037)
    teeth=[]
    for i in range(19):
        u=.08+i/18*.84;teeth.append((fx+(u*2-1)*mw,mz+.045+.045*u-.035*math.sin(u*math.pi)))
    for i in range(19):
        u=.92-i/18*.84;teeth.append((fx+(u*2-1)*mw,mz+.045+.045*u-.075*math.sin(u*math.pi)))
    patch_surface('Smile teeth',teeth,surface,white,smile,.043)
    sad=r.pivot('SadMouth',(fx,surface(fx,mz),mz),head)
    r.tube('Rueful mouth',[(fx-mw,surface(fx-mw,mz)-.025,mz),(fx,surface(fx,mz)-.035,mz+.035),(fx+mw,surface(fx+mw,mz)-.025,mz+.025)],.016,pink if female else ink,sad)
    sad.scale=(.001,)*3
    laugh=r.pivot('OpenMouth',(fx,surface(fx,mz),mz),head)
    patch_surface('Laugh',[(x,z-.085*math.sin(i/len(outline)*math.pi)) for i,(x,z) in enumerate(outline)],surface,ink,laugh,.041)
    patch_surface('Laugh teeth',teeth,surface,white,laugh,.047);laugh.scale=(.001,)*3
    # A head with a clear fruit silhouette, above a compact tailored body.
    if kind in ['mona','nora','sandi']:
        r.tube('Stem',[(0,0,2.28),(.035,0,2.48)],.045,sole,head)
        r.leaf('Fresh leaf',(.02,0,2.30),.58,.18,.85,green,head)
    if kind=='fresi':
        for i in range(6):r.leaf('Calyx',(0,0,2.30),.50,.16,(i-2.5)*.63,green,head)
        for z in [1.0,1.20,1.97,2.13]:
            for x in [-.55,-.37,.37,.55]:
                if surface(x,z)<-.28:r.ball('Seed',(x,surface(x,z)-.004,z),(.019,.012,.033),gold,head,12,8)
    if kind=='pina':
        for i in range(9):r.leaf('Crown',(0,.05,2.43),.6+(i%3)*.08,.14,(i-4)*.24,green,head)
        for z in [1.0,1.19,2.0,2.17]:
            for x in [-.50,-.30,-.10,.10,.30,.50]:
                if surface(x,z)<-.28:r.ball('Diamond',(x,surface(x,z)+.008,z),(.058,.022,.073),gold,head,12,8)
    head.location.z+=1.25
    r.ball('Neck',(0,0,1.98),(.14,.14,.20),skin,body)
    # Torso, lapels and clothing are sculpted volumes rather than sleeves on a fruit ball.
    r.ball('Tailored torso',(0,0,1.40),(.43,.28,.52),cloth,body,40,24)
    for side in [-1,1]:
        lapel=r.box('Jacket lapel',(side*.16,-.255,1.69),(.16,.055,.34),white,body,.018);lapel.rotation_euler[1]=side*.30
    r.tube('Waist seam',[(-.36,-.11,1.15),(0,-.28,1.11),(.36,-.11,1.15)],.027,pink if female else sole,body)
    for z in [1.31,1.46,1.59]:r.ball('Button',(.07,-.284,z),(.022,.012,.022),gold,body,12,8)
    for side,suffix in [(-1,'L'),(1,'R')]:
        sx=side*.43;arm=r.pivot('Arm'+suffix,(sx,0,1.78),body)
        r.tube('Sleeve',[(sx,0,1.77),(sx+side*.11,-.02,1.53),(sx+side*.13,-.06,1.35)],.105,cloth,arm)
        elbow=r.pivot('Elbow'+suffix,(sx+side*.13,-.06,1.35),arm)
        r.tube('Forearm',[(sx+side*.13,-.06,1.35),(sx+side*.16,-.16,1.19)],.075,skin,elbow)
        hand=r.pivot('Hand'+suffix,(sx+side*.16,-.16,1.16),elbow)
        r.ball('Hand',(sx+side*.16,-.16,1.13),(.095,.075,.13),skin,hand)
        hx=side*.22;leg=r.pivot('Leg'+suffix,(hx,0,1.05),rig)
        r.tube('Tailored trouser',[(hx,0,1.03),(hx+side*.04,0,.68),(hx+side*.065,-.015,.29)],.137,pants,leg)
        foot=r.pivot('Foot'+suffix,(hx+side*.065,-.05,.20),leg)
        r.ball('Shoe',(hx+side*.065,-.14,.19),(.17,.27,.13),sole,foot)
        r.ball('Sole',(hx+side*.065,-.15,.10),(.174,.275,.04),white,foot)
    # Reuse the proven native rig export/render stage, with a taller portrait camera.
    source=Path(r.__file__).read_text(encoding='utf-8')
    tail=source[source.index('    # Convert curves'):source.index("\nif __name__")]
    tail=tail.replace("camera.location=(.35,-8,3.0)","camera.location=(.35,-8,3.15)").replace("Vector((0,0,1.57))","Vector((0,0,2.0))").replace("data.ortho_scale=3.6","data.ortho_scale=4.7")
    tail=tail.replace("scene.render.resolution_x=scene.render.resolution_y=512","scene.render.resolution_x=scene.render.resolution_y=768")
    tail=tail.replace("scene.view_settings.view_transform='AgX'","scene.view_settings.view_transform='Standard';scene.view_settings.exposure=-.45")
    r.MASTER=r.HERE/'reparto_v4';r.MASTER.mkdir(exist_ok=True)
    namespace=dict(vars(r));namespace.update(locals());namespace['MASTER']=r.MASTER
    exec('def finish():\n'+tail+'\nfinish()',namespace)

if __name__=='__main__':
    for name in (sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else r.NAMES):build(name)

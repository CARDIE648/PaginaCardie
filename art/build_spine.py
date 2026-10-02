"""CARDIE original illustrative spine. Run with Blender --background --python art/build_spine.py.
Centimetre-like artistic units; not a diagnostic/anatomical reference mesh.
"""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'static' / 'models'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, color, roughness=.42, metal=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Metallic'].default_value=metal
    return m

bone=material('Porcelain · warm ivory',(.72,.66,.54),.38)
disc=material('Intervertebral discs · muted teal',(.22,.43,.43),.52)
root=bpy.data.objects.new('CARDIE_Spine',None); bpy.context.collection.objects.link(root)

def mesh(name, verts, faces, mat):
    m=bpy.data.meshes.new(name); m.from_pydata(verts,[],faces); m.update()
    o=bpy.data.objects.new(name,m); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in m.polygons: p.use_smooth=True
    return o

def body(name,rx,ry,h,mat):
    verts=[]; faces=[]; n=40
    # Raised endplate lips and slightly concave cortical walls.
    rings=[(-.5,.88),(-.46,1.02),(-.34,1),(-.12,.94),(.12,.94),(.34,1),(.46,1.02),(.5,.88)]
    for z,r in rings:
        for i in range(n):
            a=2*math.pi*i/n
            kidney=1-.16*max(0,math.sin(a))**4
            verts.append((rx*math.cos(a)*r,ry*math.sin(a)*r*kidney,z*h))
    for j in range(len(rings)-1):
        for i in range(n):
            k=j*n+i; q=j*n+(i+1)%n
            faces.append((k,q,q+n,k+n))
    faces += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
    return mesh(name,verts,faces,mat)

def tube(name,points,radii,mat):
    vs=[]; fs=[]; sides=12
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize(); axis=tangent.cross(Vector((0,0,1)))
        if axis.length<.01: axis=tangent.cross(Vector((0,1,0)))
        axis.normalize(); other=tangent.cross(axis).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides; v=Vector(p)+radii[i]*(axis*math.cos(a)+other*math.sin(a)); vs.append(v)
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides; fs.append((a,b,b+sides,a+sides))
    fs.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
    return mesh(name,vs,fs,mat)

def join(parts,name,remesh=False):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); o=parts[0]; o.name=name
    bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces)); bm.to_mesh(o.data); bm.free()
    if remesh:
        mod=o.modifiers.new('Continuous sculpted bone','REMESH'); mod.mode='VOXEL'; mod.voxel_size=.055
        bpy.ops.object.modifier_apply(modifier=mod.name)
        sm=o.modifiers.new('Polish','SMOOTH'); sm.factor=1.1; sm.iterations=4; bpy.ops.object.modifier_apply(modifier=sm.name)
        dec=o.modifiers.new('Web mesh','DECIMATE'); dec.ratio=.48; bpy.ops.object.modifier_apply(modifier=dec.name)
    for p in o.data.polygons:p.use_smooth=True
    return o

def vertebra_template(region):
    parts=[body('body',.67,.48,.49,bone)]
    # Pedicles + lamina enclose a true open vertebral foramen.
    for s in [-1,1]:
        parts.append(tube('arch',[(s*.42,.2,0),(s*.49,.57,.03),(s*.34,.85,.04),(0,.98,0)],[.15,.145,.14,.14],bone))
        parts.append(tube('transverse',[(s*.44,.53,0),(s*.77,.64,.03),(s*1.01,.69,.08)],[.17,.13,.07],bone))
        for d in [-1,1]:
            parts.append(tube('facet',[(s*.4,.64,0),(s*.42,.67,d*.23),(s*.39,.71,d*.32)],[.15,.13,.10],bone))
    down=-.40 if region=='Thoracic' else -.07
    length=1.57 if region=='Thoracic' else 1.28
    tip=.13 if region=='Lumbar' else .065
    parts.append(tube('spinous',[(0,.87,.02),(0,1.13,down*.4),(0,length,down)],[.16,.15,tip],bone))
    return join(parts,'template_'+region,True)

templates={r:vertebra_template(r) for r in ['Cervical','Thoracic','Lumbar']}
records=[]
def curvature(z): return .72*math.sin((z-1.2)*.68)-.12*math.sin(z*1.4)
z=0
for i in range(24):
    # Construct bottom to top: L5..L1, T12..T1, C7..C1.
    if i<5: region='Lumbar'; num=5-i; scale=1.16-.035*i; h=.63
    elif i<17: region='Thoracic'; num=17-i; scale=.96-.020*(i-5); h=.50
    else: region='Cervical'; num=24-i; scale=.69-.018*(i-17); h=.39
    name=region+'_'+str(num)
    obj=bpy.data.objects.new(name,templates[region].data); bpy.context.collection.objects.link(obj)
    obj.scale=(scale,scale,h/.49*.78); obj.location=(0,curvature(z),z); obj.rotation_euler.x=math.atan(.23*math.cos((z-1.2)*.68))*.4
    obj.parent=root; obj['region']=region; obj['level']=name
    if not (region=='Cervical' and num==1):
        d=body('Disc_'+name,.64*scale,.455*scale,h*.19,disc)
        d.location=(0,curvature(z-h*.5),z-h*.5); d.parent=root; d['region']=region
    if region=='Cervical' and num==1:
        bpy.data.objects.remove(obj,do_unlink=True)
        points=[(.44*math.cos(a*2*math.pi/32),.46*math.sin(a*2*math.pi/32)+.17,0) for a in range(33)]
        obj=tube(name,points,[.11]*33,bone); obj.location=(0,curvature(z),z); obj.parent=root; obj['region']=region
    if region=='Cervical' and num==2:
        dens=tube('Axis_dens',[(0,0,0),(0,0,.36),(0,0,.53)],[.13,.11,.06],bone)
        dens.location=(0,curvature(z),z); dens.parent=root; dens['region']=region
    records.append({'name':name,'region':region,'height':round(z,3)})
    z+=h
for o in templates.values():bpy.data.objects.remove(o,do_unlink=True)

# Sculpted pelvic ring and perforated sacrum, shared by both web views.
import sys
sys.path.insert(0, str(ROOT / 'art'))
from pelvis_anatomy import build_pelvis
pelvis_report = build_pelvis(root, bone, disc, mesh, tube, join)

# Center model about its vertical midpoint; Blender Z maps to glTF Y.
for child in root.children: child.location.z-=4.6
root.rotation_euler.z=math.radians(-24)
for frame,angle in [(1,-24),(121,-7),(241,-24)]:
    root.rotation_euler.z=math.radians(angle); root.keyframe_insert(data_path='rotation_euler',frame=frame)
if root.animation_data:root.animation_data.action.name='CARDIE · slow inspection'
bpy.context.scene.frame_end=240; bpy.context.scene.render.fps=30; bpy.context.scene.frame_set(1)
bpy.ops.object.select_all(action='DESELECT'); root.select_set(True)
for o in root.children:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=str(OUT/'cardie-spine.glb'),export_format='GLB',use_selection=True,export_animations=True,export_extras=True)

# Editable studio scene and locally rendered fallback.
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=24
scene.world.color=(.22,.28,.3)
def aim(o,point):o.rotation_euler=(Vector(point)-o.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('Key',(6,-8,10),1900,8),('Fill',(-6,-4,2),1300,7),('Rim',(4,5,8),2100,6)]:
    bpy.ops.object.light_add(type='AREA',location=loc); l=bpy.context.object; l.name=name; l.data.energy=power; l.data.shape='DISK'; l.data.size=size; aim(l,(0,0,0))
bpy.ops.object.camera_add(location=(11,-20,5)); cam=bpy.context.object; aim(cam,(0,0,-.05)); cam.data.type='ORTHO'; cam.data.ortho_scale=15.2; scene.camera=cam
scene.render.resolution_x=720; scene.render.resolution_y=1000; scene.render.resolution_percentage=100
scene.render.film_transparent=True; scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(OUT/'spine-poster.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art'/'cardie-spine.blend'))
bpy.ops.render.render(write_still=True)
(OUT/'model-report.json').write_text(json.dumps({'vertebrae':records,'count':24,'source':'Original procedural Blender model','purpose':'Stylized web illustration; not a clinical reference','pelvis':pelvis_report,'glb_bytes':(OUT/'cardie-spine.glb').stat().st_size},indent=2))
# Orthographic pelvic review views, separate from the website assets.
review=ROOT/'art'/'review'; review.mkdir(exist_ok=True)
scene.render.resolution_x=1000; scene.render.resolution_y=1000
scene.cycles.samples=48
root.rotation_euler.z=0
root.animation_data_clear()
cam.data.ortho_scale=6.7
for label,position in [('anterior',(0,-18,-5.3)),('posterior',(0,18,-5.3)),('oblique',(11,-18,-3.7))]:
    cam.location=position; aim(cam,(0,-.4,-5.65))
    scene.render.filepath=str(review/('pelvis-'+label+'.png'))
    bpy.ops.render.render(write_still=True)
print('CARDIE_MODEL_COMPLETE')

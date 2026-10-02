"""CARDIE · video en loop para la portada (mitad derecha del hero).

Uso:
  blender --background art/cardie-spine.blend --python art/build_hero_video.py -- [preview|frames|encode|all]

  preview  → 4 fotogramas de prueba a media resolución en art/render/preview/
  frames   → todos los fotogramas PNG en art/render/frames/
  encode   → static/video/hero-spine.mp4 + .webm + poster .webp/.jpg a partir de los PNG
  all      → frames + encode

No modifica art/cardie-spine.blend: guarda la escena del video en art/cardie-hero-video.blend.
Loop perfecto: todo el movimiento es periódico con LOOP fotogramas (el fotograma LOOP+1 == 1).
"""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art'
RENDER = ART / 'render'
MODE = (sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'preview')

FPS = 24
LOOP = 240                     # 10 s
RES = (960, 1080)
TEAL = (0.36, 0.92, 0.84)
random.seed(7)

sc = bpy.context.scene
root = bpy.data.objects['CARDIE_Spine']

# ── Modelo fijo de frente (el movimiento lo hace la cámara) ──────────────────
root.animation_data_clear()
root.rotation_euler = (0, 0, math.radians(-10))
bpy.context.view_layer.update()


def curvature(z_world):
    """Desplazamiento Y de la columna (misma curva que build_spine.py)."""
    zb = z_world + 4.6
    return .72 * math.sin((zb - 1.2) * .68) - .12 * math.sin(zb * 1.4)


def spine_point(z):
    v = Vector((0, curvature(z), z))
    return root.matrix_world @ v


# ── Escáner: empty que recorre la columna de abajo hacia arriba ──────────────
scanner = bpy.data.objects.new('Scanner', None)
sc.collection.objects.link(scanner)
Z0, Z1 = -7.5, 9.5           # fuera de cuadro en ambos extremos → salto invisible


def scan_z(f):
    return Z0 + (Z1 - Z0) * ((f - 1) % LOOP) / LOOP


for f in range(1, LOOP + 2, 4):
    z = Z0 + (Z1 - Z0) * (f - 1) / LOOP
    p = spine_point(max(-4.6, min(6.9, z)))
    scanner.location = (p.x, p.y, z)
    scanner.keyframe_insert('location', frame=f)


def set_linear_cyclic(obj):
    ad = obj.animation_data
    if not ad or not ad.action: return
    act = ad.action
    curves = []
    if hasattr(act, 'fcurves'):
        curves = list(act.fcurves)
    else:  # Blender 4.4+/5.x: acciones por capas
        for layer in act.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curves += list(bag.fcurves)
    for fc in curves:
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'
        if not any(m.type == 'CYCLES' for m in fc.modifiers):
            fc.modifiers.new('CYCLES')


set_linear_cyclic(scanner)


def scan_mask(nt, width, sharp=2.0):
    """Nodo que vale 1 cerca del plano del escáner y 0 lejos (en Z del mundo)."""
    n = nt.nodes
    tc = n.new('ShaderNodeTexCoord'); tc.object = scanner
    sep = n.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs[0])
    ab = n.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; nt.links.new(sep.outputs['Z'], ab.inputs[0])
    mr = n.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0
    mr.inputs['From Max'].default_value = width; mr.inputs['To Min'].default_value = 1; mr.inputs['To Max'].default_value = 0
    nt.links.new(ab.outputs[0], mr.inputs['Value'])
    pw = n.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = sharp
    nt.links.new(mr.outputs['Result'], pw.inputs[0])
    return pw.outputs[0]


def add(nt, a, b, op='ADD', clamp=False):
    m = nt.nodes.new('ShaderNodeMath'); m.operation = op; m.use_clamp = clamp
    nt.links.new(a, m.inputs[0]) if not isinstance(a, (int, float)) else None
    if isinstance(a, (int, float)): m.inputs[0].default_value = a
    if isinstance(b, (int, float)): m.inputs[1].default_value = b
    else: nt.links.new(b, m.inputs[1])
    return m.outputs[0]


# ── Materiales de render (más detalle que el GLB web) ────────────────────────
def upgrade_bone(mat, emissive_scale):
    nt = mat.node_tree; n = nt.nodes
    bs = n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value = .5
    if 'Subsurface Weight' in bs.inputs:
        bs.inputs['Subsurface Weight'].default_value = .12
        bs.inputs['Subsurface Radius'].default_value = (.12, .08, .06)
        bs.inputs['Subsurface Scale'].default_value = .05
    # Textura de hueso: poro fino + vetas suaves
    tc = n.new('ShaderNodeTexCoord')
    noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 38; noise.inputs['Detail'].default_value = 8
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    vor = n.new('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 140
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    mix = add(nt, noise.outputs['Fac'], vor.outputs['Distance'], 'MULTIPLY')
    bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .22; bump.inputs['Distance'].default_value = .02
    nt.links.new(mix, bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
    # Variación de color cálida
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (.66, .60, .49, 1); ramp.color_ramp.elements[1].color = (.80, .76, .66, 1)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    # Brillo del escáner: banda ancha suave + línea fina intensa
    wide = scan_mask(nt, .9, 2.2); line = scan_mask(nt, .07, 1.0)
    strength = add(nt, add(nt, wide, 1.6 * emissive_scale, 'MULTIPLY'), add(nt, line, 7 * emissive_scale, 'MULTIPLY'))
    bs.inputs['Emission Color'].default_value = (*TEAL, 1)
    nt.links.new(strength, bs.inputs['Emission Strength'])


upgrade_bone(bpy.data.materials['Porcelain · warm ivory'], 1.0)
disc = bpy.data.materials['Intervertebral discs · muted teal']
db = disc.node_tree.nodes.get('Principled BSDF')
db.inputs['Base Color'].default_value = (.16, .42, .42, 1); db.inputs['Roughness'].default_value = .35
if 'Coat Weight' in db.inputs: db.inputs['Coat Weight'].default_value = .4
dm = scan_mask(disc.node_tree, 1.1, 1.6)
db.inputs['Emission Color'].default_value = (*TEAL, 1)
disc.node_tree.links.new(add(disc.node_tree, add(disc.node_tree, dm, 3.0, 'MULTIPLY'), .25), db.inputs['Emission Strength'])

# Suavizado solo para el render
for o in root.children_recursive if hasattr(root, 'children_recursive') else root.children:
    if o.type == 'MESH':
        m = o.modifiers.new('Render smooth', 'SUBSURF'); m.levels = 0; m.render_levels = 1


def glow_material(name, color, base, scan_gain, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; n.clear()
    out = n.new('ShaderNodeOutputMaterial'); em = n.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1)
    tr = n.new('ShaderNodeBsdfTransparent'); mx = n.new('ShaderNodeMixShader')
    mask = scan_mask(nt, 1.4, 1.5)
    nt.links.new(add(nt, add(nt, mask, scan_gain, 'MULTIPLY'), base), em.inputs['Strength'])
    mx.inputs['Fac'].default_value = alpha
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    return m


# ── Nervios: raíces que salen entre vértebras y se ramifican ─────────────────
nerve_mat = glow_material('CARDIE · nervio', TEAL, .3, 10, .75)


def nerve(points, radius):
    cu = bpy.data.curves.new('Nerve', 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = radius; cu.bevel_resolution = 2; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(points) - 1)
    for bp, p in zip(sp.bezier_points, points):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    # Se adelgaza hacia la punta
    for i, bp in enumerate(sp.bezier_points): bp.radius = 1 - .8 * i / max(1, len(points) - 1)
    o = bpy.data.objects.new('Nerve', cu); sc.collection.objects.link(o); o.data.materials.append(nerve_mat)
    return o


for o in [o for o in root.children if o.name.startswith(('Lumbar_', 'Thoracic_', 'Cervical_'))]:
    if o.name in ('Cervical_1', 'Cervical_2'): continue
    base = o.matrix_world.translation
    big = 1.0 if o.name.startswith('Lumbar') else .75 if o.name.startswith('Thoracic') else .55
    for s in (-1, 1):
        start = base + Vector((s * .55, .25, -.22))
        pts = [start]; d = Vector((s * 1, random.uniform(-.25, .35), random.uniform(-.55, -.15))).normalized()
        p = start.copy()
        for k in range(4):
            p = p + d * random.uniform(.55, .9) * big
            d = (d + Vector((random.uniform(-.2, .2), random.uniform(-.3, .3), random.uniform(-.35, .05)))).normalized()
            pts.append(p.copy())
        nerve(pts, .022 * big)
        for b in range(1):                       # ramas
            i = random.randint(1, len(pts) - 2); q = pts[i].copy(); dd = (d + Vector((0, random.uniform(-.8, .8), random.uniform(-.6, .4)))).normalized()
            br = [q]
            for k in range(3):
                q = q + dd * random.uniform(.35, .6) * big; dd = (dd + Vector((random.uniform(-.3, .3),) * 3)).normalized(); br.append(q.copy())
            nerve(br, .01 * big)

# ── Anillo holográfico que acompaña al escáner ───────────────────────────────
ring_mat = glow_material('CARDIE · anillo', TEAL, 3.5, 0, .9)
bpy.ops.mesh.primitive_torus_add(major_radius=1.55, minor_radius=.012, major_segments=96, minor_segments=8)
ring = bpy.context.object; ring.name = 'Scan ring'; ring.data.materials.append(ring_mat); ring.parent = scanner
bpy.ops.mesh.primitive_circle_add(vertices=96, radius=1.55, fill_type='NGON')
plate = bpy.context.object; plate.name = 'Scan plate'; plate.parent = scanner
pm = bpy.data.materials.new('CARDIE · plano escaneo'); pm.use_nodes = True
nt = pm.node_tree; n = nt.nodes; n.clear()
out = n.new('ShaderNodeOutputMaterial'); em = n.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*TEAL, 1); em.inputs['Strength'].default_value = 1.2
tr = n.new('ShaderNodeBsdfTransparent'); mx = n.new('ShaderNodeMixShader')
tc = n.new('ShaderNodeTexCoord'); grad = n.new('ShaderNodeTexGradient'); grad.gradient_type = 'SPHERICAL'
mapn = n.new('ShaderNodeMapping'); mapn.inputs['Scale'].default_value = (.66, .66, .66)
nt.links.new(tc.outputs['Object'], mapn.inputs[0]); nt.links.new(mapn.outputs[0], grad.inputs[0])
inv = n.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1; nt.links.new(grad.outputs['Fac'], inv.inputs[1])
pw = n.new('ShaderNodeMath'); pw.operation = 'MULTIPLY'; pw.inputs[1].default_value = .22; nt.links.new(inv.outputs[0], pw.inputs[0])
# borde más visible: 1 - gradiente invertido → anillo suave
nt.links.new(pw.outputs[0], mx.inputs['Fac'])
nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
plate.data.materials.append(pm)
for ob in (ring, plate):
    ob.visible_shadow = False

# ── Partículas flotantes (polvo de luz, desenfocadas por la profundidad) ─────
dust_mat = glow_material('CARDIE · polvo', (.85, 1, .97), 2.2, 4, .8)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1)
proto = bpy.context.object; proto.data.materials.append(dust_mat); proto_mesh = proto.data
bpy.data.objects.remove(proto, do_unlink=True)
for i in range(170):
    o = bpy.data.objects.new('Dust', proto_mesh); sc.collection.objects.link(o)
    a = random.uniform(0, math.tau); r = random.uniform(1.4, 7.5)
    z = random.uniform(-6, 8)
    o.location = (math.cos(a) * r, math.sin(a) * r, z)
    s = random.uniform(.012, .04); o.scale = (s, s, s); o.visible_shadow = False
    amp = random.uniform(.15, .45); period = random.choice((60, 80, 120, 240)); ph = random.randint(0, period)
    for k in range(5):
        f = 1 + ph + k * period / 4
        o.location.z = z + amp * (0, 1, 0, -1, 0)[k]
        o.location.x = math.cos(a) * r + amp * .5 * (1, 0, -1, 0, 1)[k]
        o.keyframe_insert('location', frame=f)
    ad = o.animation_data.action
    for fc in (list(ad.fcurves) if hasattr(ad, 'fcurves') else [c for l in ad.layers for s_ in l.strips for b in s_.channelbags for c in b.fcurves]):
        fc.modifiers.new('CYCLES')

# ── Cámara: vaivén cercano que sube y baja por la columna (periódico) ────────
cam = sc.camera
cam.data.type = 'PERSP'; cam.data.lens = 50; cam.data.sensor_fit = 'AUTO'
cam.data.shift_x = -.10
focus = bpy.data.objects.new('Focus', None); sc.collection.objects.link(focus)
for c in list(cam.constraints): cam.constraints.remove(c)
tt = cam.constraints.new('TRACK_TO'); tt.target = focus; tt.track_axis = 'TRACK_NEGATIVE_Z'; tt.up_axis = 'UP_Y'
cam.data.dof.use_dof = True; cam.data.dof.focus_object = focus; cam.data.dof.aperture_fstop = 1.6
for f in range(1, LOOP + 2, 2):
    t = (f - 1) / LOOP * math.tau
    zc = .2 + 2.6 * math.sin(t) + .4 * math.sin(2 * t)          # sube y baja por la zona dorsal-lumbar
    ang = math.radians(-58 + 26 * math.sin(t + 1.1))             # se mueve alrededor (vista 3/4)
    dist = 7.4 + .7 * math.cos(2 * t)
    p = spine_point(max(-4.2, min(6.5, zc)))
    focus.location = p; focus.keyframe_insert('location', frame=f)
    cam.location = p + Vector((math.sin(ang) * dist * -1, -math.cos(ang) * dist, .6 + .35 * math.sin(t)))
    cam.keyframe_insert('location', frame=f)
set_linear_cyclic(focus); set_linear_cyclic(cam)

# ── Fondo degradado que viaja con la cámara + luces ──────────────────────────
bpy.ops.mesh.primitive_plane_add(size=1)
bg = bpy.context.object; bg.name = 'Backdrop'; bg.parent = cam
bg.location = (0, 0, -40); bg.scale = (60, 60, 1); bg.rotation_euler = (0, 0, 0)
bm = bpy.data.materials.new('CARDIE · fondo'); bm.use_nodes = True
nt = bm.node_tree; n = nt.nodes; n.clear()
out = n.new('ShaderNodeOutputMaterial'); em = n.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1
tc = n.new('ShaderNodeTexCoord'); mp = n.new('ShaderNodeMapping'); mp.inputs['Location'].default_value = (-.15, -.25, 0); mp.inputs['Scale'].default_value = (3, 3, 1)
grad = n.new('ShaderNodeTexGradient'); grad.gradient_type = 'SPHERICAL'
ramp = n.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].color = (.13, .24, .27, 1); ramp.color_ramp.elements[1].color = (.66, .77, .77, 1)
ramp.color_ramp.elements.new(.55).color = (.33, .47, .50, 1)
nt.links.new(tc.outputs['Object'], mp.inputs[0]); nt.links.new(mp.outputs[0], grad.inputs[0])
nt.links.new(grad.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], em.inputs['Color']); nt.links.new(em.outputs[0], out.inputs[0])
bg.data.materials.append(bm)
bg.visible_diffuse = bg.visible_glossy = bg.visible_shadow = bg.visible_transmission = bg.visible_volume_scatter = False

sc.world.use_nodes = True
wb = sc.world.node_tree.nodes.get('Background')
if wb: wb.inputs['Color'].default_value = (.30, .40, .42, 1); wb.inputs['Strength'].default_value = .55
for name, loc, power in [('Key', (-7, -9, 9), 2200), ('Fill', (8, -6, -1), 900), ('Rim', (3, 7, 6), 2600)]:
    l = bpy.data.objects[name]; l.location = loc; l.data.energy = power
    l.rotation_euler = (Vector((0, 0, 0)) - l.location).to_track_quat('-Z', 'Y').to_euler()
bpy.data.objects['Rim'].data.color = (.75, 1, .95)

# ── Render ───────────────────────────────────────────────────────────────────
sc.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
for d in prefs.devices: d.use = d.type == 'OPTIX'
sc.cycles.device = 'GPU'
sc.cycles.samples = 64; sc.cycles.use_denoising = True
sc.render.use_persistent_data = True
sc.cycles.adaptive_threshold = .02
sc.render.film_transparent = False
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = LOOP
sc.render.resolution_x, sc.render.resolution_y = RES
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass

# Brillo (glare) en el compositor, si la API lo permite
try:
    if hasattr(sc, 'compositing_node_group'):
        tree = bpy.data.node_groups.new('CARDIE glow', 'CompositorNodeTree')
        sc.compositing_node_group = tree
        rl = tree.nodes.new('CompositorNodeRLayers'); gl = tree.nodes.new('CompositorNodeGlare')
        outn = tree.nodes.new('NodeGroupOutput'); tree.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
        for sock, val in (('Type', 'Bloom'), ('Quality', 'High'), ('Threshold', 1.1), ('Strength', .35), ('Size', .7), ('Saturation', .8)):
            if sock in gl.inputs: gl.inputs[sock].default_value = val
        tree.links.new(rl.outputs['Image'], gl.inputs['Image']); tree.links.new(gl.outputs['Image'], outn.inputs[0])
    else:
        sc.use_nodes = True; tree = sc.node_tree; tree.nodes.clear()
        rl = tree.nodes.new('CompositorNodeRLayers'); gl = tree.nodes.new('CompositorNodeGlare'); comp = tree.nodes.new('CompositorNodeComposite')
        gl.glare_type = 'FOG_GLOW'; gl.threshold = 1.2; gl.mix = -.6
        tree.links.new(rl.outputs['Image'], gl.inputs['Image']); tree.links.new(gl.outputs['Image'], comp.inputs['Image'])
    print('CARDIE glow: ok')
except Exception as e:
    print('CARDIE glow: omitido', e)

bpy.ops.wm.save_as_mainfile(filepath=str(ART / 'cardie-hero-video.blend'), copy=True)


def render_frames(frames, folder, scale=100, samples=None):
    folder.mkdir(parents=True, exist_ok=True)
    sc.render.resolution_percentage = scale
    if samples: sc.cycles.samples = samples
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
    for f in frames:
        sc.frame_set(f); sc.render.filepath = str(folder / f'f_{f:04d}.png')
        bpy.ops.render.render(write_still=True)


if MODE == 'preview':
    render_frames([1, 121], RENDER / 'preview', 50, 48)
elif MODE in ('frames', 'all'):
    render_frames(range(1, LOOP + 1), RENDER / 'frames')
print('CARDIE_VIDEO_SCENE_DONE', MODE)

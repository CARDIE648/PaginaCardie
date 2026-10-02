"""Original sculpted pelvic geometry; Blender Z up, -Y anterior.
Landmarks informed by the supplied diagrams and OpenStax A&P 7.3 / 8.3.
An artistic model, not a segmented scan or validated clinical reference.
"""
import bpy, math
from mathutils import Vector


def build_pelvis(root, bone, cartilage, mesh, tube, join):
    def apply(obj, modifier):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    def ellipsoid(name, center, scale, mat=bone):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=center)
        o = bpy.context.object; o.name = name; o.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        o.data.materials.append(mat)
        for p in o.data.polygons: p.use_smooth = True
        return o

    def subtract(obj, cutter, name):
        mod = obj.modifiers.new(name, 'BOOLEAN'); mod.operation = 'DIFFERENCE'
        mod.solver = 'EXACT'; mod.object = cutter; apply(obj, mod)
        bpy.data.objects.remove(cutter, do_unlink=True)

    def finish(o, region, note):
        o.parent = root; o['region'] = region; o['anatomy'] = note
        for p in o.data.polygons: p.use_smooth = True
        return o

    def catmull(points, steps=7):
        """Interpolated paths avoid angular, pipe-like pelvic rami."""
        pts = [Vector(p) for p in points]; result = []
        for i in range(len(pts)-1):
            a, b, c, d = pts[max(i-1,0)], pts[i], pts[i+1], pts[min(i+2,len(pts)-1)]
            for k in range(steps):
                t = k/steps
                result.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)))
        return result+[tuple(pts[-1])]

    def sculpt_path(name, points, radius):
        p = catmull(points)
        rs = [radius*(.92+.13*math.sin(math.pi*i/(len(p)-1))) for i in range(len(p))]
        return tube(name, p, rs, bone)

    # Broad sacral base, tapering toward apex; gently concave pelvic face.
    def sacral_section(t, u):
        width = 1.25*(1-t)**.73+.105
        z = -.405-2.24*t-.15*u*u*(1-t)
        mid = -.49+.82*math.sin(math.pi*.82*t)
        thick = .68*(1-t)+.27*t
        front = mid-thick*.5+.105*(1-u*u)*math.sin(math.pi*t)
        back = mid+thick*.5+.075*(1-u*u)
        return u*width, front, back, z

    columns, rows = 33, 49
    vs=[]; fs=[]
    for side in range(2):
        for j in range(rows):
            for i in range(columns):
                x, front, back, z = sacral_section(j/(rows-1), -1+2*i/(columns-1))
                vs.append((x, front if side==0 else back, z))
    layer=columns*rows
    for side in range(2):
        for j in range(rows-1):
            for i in range(columns-1):
                k=side*layer+j*columns+i
                face=(k,k+1,k+1+columns,k+columns)
                fs.append(face if side==0 else tuple(reversed(face)))
    for j in range(rows-1):
        a=j*columns; b=(j+1)*columns
        fs.append((a,b,b+layer,a+layer))
        a+=columns-1; b+=columns-1
        fs.append((a,a+layer,b+layer,b))
    for i in range(columns-1):
        fs.append((i,i+layer,i+layer+1,i+1))
        a=(rows-1)*columns+i
        fs.append((a,a+1,a+layer+1,a+layer))
    sac=mesh('Sacrum',vs,fs,bone)
    parts=[sac]
    # Rounded alae and S1 load-bearing plateau soften the triangular silhouette.
    parts.append(ellipsoid('S1_body',(0,-.49,-.62),(.74,.43,.225)))
    for s in [-1,1]:
        parts.append(ellipsoid('Sacral_ala',(s*.96,-.32,-.69),(.39,.34,.25)))
    # Fused segment ridges on pelvic face and median crest on dorsal face.
    for t in [.285,.48,.675,.865]:
        points=[]
        for i in range(19):
            u=-.48+.96*i/18; x,f,b,z=sacral_section(t,u)
            points.append((x,f-.035,z+.03*(1-u*u)))
        parts.append(tube('Sacral_transverse_ridge',points,[.064]*len(points),bone))
    for t in [.10,.28,.46,.64,.81]:
        x,f,b,z=sacral_section(t,0)
        parts.append(ellipsoid('Median_sacral_crest',(0,b-.01,z),(.12,.15,.18)))
    sac=join(parts,'Sacrum',True)
    # Four actual bilateral tunnels, retained after smoothing.
    for level,t in enumerate([.17,.37,.57,.77],1):
        for s in [-1,1]:
            x,f,b,z=sacral_section(t,s*.57)
            radius=.145-.015*(level-1)
            cutter=ellipsoid('foramen_cutter',(x,(f+b)*.5,z),(radius,1.3,radius*.90))
            subtract(sac,cutter,f'Sacral foramen {level}')
            opening=ellipsoid('anterior_foramen_recess',(x,f-.025,z),(radius*1.38,.16,radius*1.12))
            subtract(sac,opening,'Recessed anterior foramen margin')
    # Superior canal opening behind the first sacral body.
    cutter=ellipsoid('canal_cutter',(0,-.16,-.43),(.19,.17,.36))
    subtract(sac,cutter,'Superior sacral canal')
    bevel=sac.modifiers.new('Foramen edge softness','BEVEL'); bevel.width=.026; bevel.segments=2
    apply(sac,bevel)
    finish(sac,'Sacral','Triangular sacrum; 4 paired foramina, transverse fusion lines, median crest')

    # Four small, progressively tapering coccygeal segments, curving anteriorly.
    for i,(y,z,r) in enumerate([(-.05,-2.75,.14),(-.16,-2.94,.115),(-.29,-3.08,.085),(-.41,-3.17,.05)],1):
        c=ellipsoid(f'Coccyx_{i}',(0,y,z),(r,r*.82,r*1.05))
        finish(c,'Sacral','Segmented coccyx, anterior curve')

    # Both innominate bones: ilium is a broad curved plate, not an extruded wing.
    for s,label in [(-1,'Left'),(1,'Right')]:
        def mirror(p): return (s*p[0],p[1],p[2])
        crest=catmull([(1.16,.53,-.38),(1.46,.77,.12),(2.04,.49,.56),(2.53,-.12,.66),(2.61,-.80,.39),(2.33,-1.29,-.21)],8)
        base=catmull([(1.14,.37,-1.07),(1.23,.22,-1.40),(1.49,-.16,-1.51),(1.78,-.55,-1.42),(1.91,-.87,-1.30),(1.99,-1.08,-.96)],8)
        vs=[]; fs=[]; n=len(crest); rows=19
        for j in range(rows):
            v=j/(rows-1)
            for i in range(n):
                u=i/(n-1)
                p=Vector(base[i]).lerp(Vector(crest[i]),v)
                p.x += .24*math.sin(math.pi*v)*math.sin(math.pi*u)
                p.y += .18*math.sin(math.pi*v)*math.sin(math.pi*u)
                vs.append(mirror(p))
        for j in range(rows-1):
            for i in range(n-1):
                k=j*n+i; fs.append((k,k+1,k+1+n,k+n))
        ilium=mesh('Iliac_fossa',vs,fs,bone)
        mod=ilium.modifiers.new('Iliac cortical plate','SOLIDIFY'); mod.thickness=.17; mod.offset=0; apply(ilium,mod)
        parts=[ilium, tube('Iliac_crest',[mirror(p) for p in crest],[.105]*n,bone)]
        parts.append(ellipsoid('Auricular_surface',mirror((1.17,.28,-.78)),(.23,.34,.51)))
        parts.append(ellipsoid('Acetabular_body',mirror((1.77,-.76,-1.57)),(.52,.53,.54)))
        parts.append(sculpt_path('Superior_pubis',[mirror(p) for p in [(1.82,-.90,-1.54),(1.18,-1.40,-1.66),(.55,-1.78,-1.88),(.12,-1.87,-2.20)]],.175))
        parts.append(sculpt_path('Inferior_pubis',[mirror(p) for p in [(.12,-1.87,-2.20),(.31,-1.77,-2.52),(.87,-1.37,-2.78),(1.36,-.81,-2.81)]],.145))
        parts.append(sculpt_path('Ischium',[mirror(p) for p in [(1.80,-.74,-1.62),(1.58,-.37,-1.97),(1.52,-.38,-2.39),(1.36,-.81,-2.81)]],.225))
        parts.append(ellipsoid('Ischial_tuberosity',mirror((1.38,-.72,-2.68)),(.27,.29,.30)))
        parts.append(sculpt_path('Ischial_spine',[mirror(p) for p in [(1.55,-.32,-1.96),(1.34,.02,-1.93),(1.24,.17,-1.88)]],.105))
        hip=join(parts,'Pelvis_'+label,True)
        # A deep socket opens inferolaterally; each cavity has a real floor.
        cavity=ellipsoid('acetabulum_cutter',mirror((2.02,-.98,-1.60)),(.445,.44,.42))
        subtract(hip,cavity,'Acetabulum socket')
        bevel=hip.modifiers.new('Socket edge softness','BEVEL'); bevel.width=.024; bevel.segments=2; apply(hip,bevel)
        finish(hip,'Pelvic','Iliac fossa and crest, acetabulum, sciatic notch, ischium, pubic rami, obturator foramen')

    # Separate, restrained joint surface closes the anterior pelvic ring.
    symphysis=ellipsoid('Pubic_symphysis',(0,-1.87,-2.22),(.085,.14,.21),cartilage)
    finish(symphysis,'Pelvic','Pubic symphysis between right and left pubic bodies')
    return {'sacral_foramina_pairs':4,'hip_bones':2,'acetabula':2,'obturator_foramina':2,'coccygeal_segments':4}

"""Run against the saved .blend to verify the revised closed bone surfaces."""
import bpy, bmesh, json
from pathlib import Path

result={}
for name in ['Sacrum','Pelvis_Left','Pelvis_Right']:
    o=bpy.data.objects[name]
    bm=bmesh.new(); bm.from_mesh(o.data)
    result[name]={'vertices':len(bm.verts),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'volume':round(bm.calc_volume(signed=False),4)}
    assert result[name]['non_manifold_edges']==0, f'{name}: open edges'
    assert result[name]['volume']>0, f'{name}: empty mesh'
    bm.free()
root=bpy.data.objects['CARDIE_Spine']
assert root.animation_data and root.animation_data.action
assert len([o for o in root.children if o.name.startswith('Coccyx_')])==4
result['animation']=root.animation_data.action.name
(Path(__file__).parent/'review'/'geometry-validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

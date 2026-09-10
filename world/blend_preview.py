# quick turntable preview of a GLB: blender -b -P blend_preview.py -- in.glb out.png
import bpy, sys, math
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:]; IN,OUT=argv[0],argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=IN)
sc=bpy.context.scene; ms=[o for o in sc.objects if o.type=='MESH']
lo=Vector((1e9,)*3); hi=Vector((-1e9,)*3)
for m in ms:
    for v in m.bound_box:
        w=m.matrix_world@Vector(v); lo=Vector(map(min,lo,w)); hi=Vector(map(max,hi,w))
c=(lo+hi)/2; sz=max(hi-lo)
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
views=[(0,-1),(1,0),(0,1)]   # front(-Y), side(+X), back(+Y)
import os
sc.render.engine='BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
sc.render.resolution_x=600; sc.render.resolution_y=800; sc.render.film_transparent=False
w=bpy.data.worlds.new('w'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs[1].default_value=1.0; sc.world=w
for i,(dx,dy) in enumerate(views):
    cam.location=(c.x+dx*sz*2.6,c.y+dy*sz*2.6,c.z+sz*.15); cam.rotation_euler=(Vector((c.x,c.y,c.z))-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.lens=50
    sc.render.filepath=OUT.replace('.png',f'_{i}.png'); bpy.ops.render.render(write_still=True)
print('ok',[round(x,2) for x in (hi-lo)])

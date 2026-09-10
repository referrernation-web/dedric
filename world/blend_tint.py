# Darken skin-toned texels toward a deep bronze so the stylized body matches Dedric. blender -b -P blend_tint.py -- in.glb out.glb
import bpy, sys, numpy as np
argv=sys.argv[sys.argv.index('--')+1:]; IN,OUT=argv[0],argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=IN)
n=0
for img in bpy.data.images:
    if not img.has_data or img.size[0]==0: continue
    px=np.array(img.pixels[:],dtype=np.float32).reshape(-1,4); rgb=px[:,:3]
    mx=rgb.max(1); mn=rgb.min(1); v=mx; s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    r,g,b=rgb[:,0],rgb[:,1],rgb[:,2]
    skin=(r>g)&(g>b)&(s>.18)&(s<.75)&(v>.35)&((r-b)>.12)         # warm light skin: r>g>b, moderate saturation, bright
    k=skin.astype(np.float32)[:,None]
    target=rgb*np.array([.55,.40,.30],dtype=np.float32)              # deep bronze
    px[:,:3]=rgb*(1-k)+target*k
    img.pixels=px.ravel().tolist(); img.pack(); n+=int(skin.sum())
print('tinted texels',n)
bpy.ops.export_scene.gltf(filepath=OUT,export_format='GLB',export_apply=False)
print('exported',OUT)

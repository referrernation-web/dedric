# Pack Blender frame PNGs into 8-frame sprite strips (WebP, transparent) the mascot game expects.
# python strip.py <frames_dir> <out_dir> <prefix> [key ...]   e.g. python strip.py spr_dedric ../assets/spr d run jump cling sit
# Same finishing as Mark's hd.py: union bbox across the 8 frames (so the character never shifts), bottom/center align,
# 1px alpha erode + 0.7 gaussian to kill edge fringe. Writes/updates out_dir/meta.json {"d-run":[w,h],...}.
import sys, os, json
from PIL import Image, ImageFilter
src, out, pre = sys.argv[1], sys.argv[2], sys.argv[3]
keys = sys.argv[4:] or ["run", "jump", "cling", "sit"]
os.makedirs(out, exist_ok=True)
meta_p = os.path.join(out, "meta.json")
meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
for key in keys:
    frames = []
    for i in range(8):
        p = os.path.join(src, f"{key}_{i}.png")
        if not os.path.exists(p):
            break
        frames.append(Image.open(p).convert("RGBA"))
    if len(frames) < 8:
        print("skip", key, "frames found:", len(frames)); continue
    boxes = [f.getbbox() for f in frames]
    x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
    w, h = x1 - x0, y1 - y0
    strip = Image.new("RGBA", (w * 8, h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        cell = f.crop((x0, y0, x1, y1))
        a = cell.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.7))
        cell.putalpha(a)
        strip.paste(cell, (i * w, 0), cell)
    name = f"{pre}-{key}"
    strip.save(os.path.join(out, name + ".webp"), "WEBP", quality=88, method=6)
    strip.crop((0, 0, w, h)).resize((max(1, w // 4), max(1, h // 4))).save(os.path.join(out, name + "-fb.png"))   # tiny fallback frame
    meta[name] = [w, h]
    print(name, w, "x", h, "->", os.path.getsize(os.path.join(out, name + ".webp")) // 1024, "KB")
json.dump(meta, open(meta_p, "w"), indent=0)
print("meta", meta)

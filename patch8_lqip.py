import base64, io
from PIL import Image, ImageFilter
def lqip(f):
    if not f.exists(): return ""
    im = Image.open(f).convert("RGB").resize((24, 13), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=40)
    return base64.b64encode(buf.getvalue()).decode()

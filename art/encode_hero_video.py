"""Codifica los PNG de art/render/frames/ en los videos web del hero.

Uso:
  blender --background --factory-startup --python art/encode_hero_video.py

Genera en static/video/:
  hero-spine.mp4       960×1080 (escritorio)
  hero-spine-sm.mp4    540×608  (celular)
  (WebM/VP9 salía más pesado que H.264, por eso solo MP4)
  hero-spine-poster.webp / .jpg             primer fotograma (carga instantánea)
"""
import bpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAMES = sorted((ROOT / 'art' / 'render' / 'frames').glob('f_*.png'))
OUT = ROOT / 'static' / 'video'
OUT.mkdir(parents=True, exist_ok=True)
assert FRAMES, 'Primero renderiza los fotogramas (build_hero_video.py -- frames)'

sc = bpy.context.scene
sc.render.fps = 24
sc.frame_start = 1
sc.frame_end = len(FRAMES)
sc.view_settings.view_transform = 'Standard'   # los PNG ya vienen con su transformación
sc.sequence_editor_create()
strips = sc.sequence_editor.strips
st = strips.new_image('frames', str(FRAMES[0]), 1, 1)
for f in FRAMES[1:]:
    st.elements.append(f.name)
st.frame_final_duration = len(FRAMES)


def encode(name, size, container, codec, crf):
    sc.render.resolution_x, sc.render.resolution_y = size
    sc.render.resolution_percentage = 100
    im = sc.render.image_settings
    im.media_type = 'VIDEO'
    im.file_format = 'FFMPEG'
    ff = sc.render.ffmpeg
    ff.format = container
    ff.codec = codec
    ff.constant_rate_factor = crf
    ff.ffmpeg_preset = 'BEST'
    ff.gopsize = 48
    ff.audio_codec = 'NONE'
    sc.render.filepath = str(OUT / name)
    sc.render.use_file_extension = False
    bpy.ops.render.render(animation=True)
    print('CARDIE_ENCODED', name, (OUT / name).stat().st_size)


encode('hero-spine.mp4', (960, 1080), 'MPEG4', 'H264', 'LOW')
encode('hero-spine-sm.mp4', (540, 608), 'MPEG4', 'H264', 'MEDIUM')

# Póster: el primer fotograma, para que la portada pinte al instante
img = bpy.data.images.load(str(FRAMES[0]))
img.scale(960, 1080)
for fmt, ext, q in (('WEBP', 'webp', 78), ('JPEG', 'jpg', 80)):
    s = sc.render.image_settings
    s.media_type = 'IMAGE'; s.file_format = fmt; s.quality = q; s.color_mode = 'RGB'
    img.save_render(str(OUT / f'hero-spine-poster.{ext}'), scene=sc)
    print('CARDIE_ENCODED', ext, (OUT / f'hero-spine-poster.{ext}').stat().st_size)

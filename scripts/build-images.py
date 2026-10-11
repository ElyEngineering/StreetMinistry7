#!/usr/bin/env python3
"""Build step: write full-color responsive WebP into assets/img/, plus the portrait and credits.html.
Reads assets-src/credits.json (required). Scene photos are not graded."""
import json, os, html
from PIL import Image, ImageEnhance
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
credits=json.load(open('assets-src/credits.json'))
def vivid(im):
    im=ImageEnhance.Color(im).enhance(1.25)
    return ImageEnhance.Contrast(im).enhance(1.08)
os.makedirs('assets/img',exist_ok=True)
for p in credits['photos']:
    src=f"assets-src/raw/{p['key']}.jpg"
    im=vivid(Image.open(src).convert('RGB'))
    for w in (800,1600):
        r=im.copy(); r.thumbnail((w,w*2)); r.save(f"assets/img/{p['key']}-c2-{w}.webp",'WEBP',quality=74,method=6)
# portrait: left as the existing natural-color crop
pt=Image.open('assets/jayson.jpg').convert('RGB')
for w in (480,960):
    r=pt.copy(); r.thumbnail((w,w))
    r.save(f'assets/img/jayson-{w}.webp','WEBP',quality=82,method=6)
    r.save(f'assets/img/jayson-{w}.jpg','JPEG',quality=84,optimize=True,progressive=True)
rows='\n'.join(f'<li><a href="{html.escape(p["source"])}" rel="noopener">{html.escape(p["title"])}</a> — {html.escape(p["author"])} · <a href="{html.escape(p["license_url"] or p["source"])}" rel="noopener">{html.escape(p["license"])}</a></li>' for p in credits['photos'])
tpl=open('credits.template.html').read()
open('credits.html','w').write(tpl.replace('<!--CREDITS-->',rows))
print('built',len(credits['photos']),'photos')

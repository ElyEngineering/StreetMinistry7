#!/usr/bin/env python3
"""Build step: grade photos in assets-src/raw/ to the site palette and write
responsive WebP into assets/img/, plus the portrait (webp + jpg) and credits.html.
Reads assets-src/credits.json (required)."""
import json, os, html
from PIL import Image, ImageOps
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
credits=json.load(open('assets-src/credits.json'))
# light tritone: navy steel, cool gray, near-white sky
stops=[(0,(30,48,78)),(0.42,(88,116,154)),(0.74,(186,200,216)),(1,(248,250,252))]
def lut():
    out=[[],[],[]]
    for i in range(256):
        t=i/255
        for a,b in zip(stops,stops[1:]):
            if t<=b[0]:
                f=(t-a[0])/(b[0]-a[0]); col=[a[1][k]+(b[1][k]-a[1][k])*f for k in range(3)]; break
        for k in range(3): out[k].append(int(col[k]))
    return out
L=lut()
def grade(im):
    g=ImageOps.autocontrast(im.convert('L'),cutoff=1)
    return Image.merge('RGB',[g.point(L[k]) for k in range(3)])
os.makedirs('assets/img',exist_ok=True)
# Landing bridge stays the original color. Every other photo is still graded.
NATURAL={'duluth-lift-bridge'}
for p in credits['photos']:
    src=f"assets-src/raw/{p['key']}.jpg"
    im=Image.open(src).convert('RGB')
    if p['key'] not in NATURAL:
        im=grade(im)
    for w in (800,1600):
        r=im.copy(); r.thumbnail((w,w*2)); r.save(f"assets/img/{p['key']}-{w}.webp",'WEBP',quality=74,method=6)
# portrait: natural color, gentle crop, webp + jpg
pt=Image.open('assets/jayson.jpg').convert('RGB')
for w in (480,960):
    r=pt.copy(); r.thumbnail((w,w))
    r.save(f'assets/img/jayson-{w}.webp','WEBP',quality=82,method=6)
    r.save(f'assets/img/jayson-{w}.jpg','JPEG',quality=84,optimize=True,progressive=True)
rows='\n'.join(f'<li><a href="{html.escape(p["source"])}" rel="noopener">{html.escape(p["title"])}</a> — {html.escape(p["author"])} · <a href="{html.escape(p["license_url"] or p["source"])}" rel="noopener">{html.escape(p["license"])}</a></li>' for p in credits['photos'])
tpl=open('credits.template.html').read()
open('credits.html','w').write(tpl.replace('<!--CREDITS-->',rows))
print('built',len(credits['photos']),'photos')

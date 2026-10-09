import json,sys,urllib.request,urllib.parse,re
UA={'User-Agent':'StreetMinistry7SiteBuilder/1.0 (contact: none)'}
def api(params):
    params.update(format='json')
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 8
d=api(dict(action='query',generator='search',gsrsearch='filetype:bitmap '+q,gsrnamespace=6,gsrlimit=n,prop='imageinfo',iiprop='url|size|extmetadata',iiurlwidth=400))
for p in sorted(d.get('query',{}).get('pages',{}).values(),key=lambda x:x['index']):
    ii=p['imageinfo'][0]; m=ii['extmetadata']
    lic=m.get('LicenseShortName',{}).get('value','?')
    art=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','?')).strip()
    print(f"{p['title']} | {ii['width']}x{ii['height']} | {lic} | {art[:40]}")

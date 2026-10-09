import json,urllib.request,urllib.parse,re,sys,os,time
UA={'User-Agent':'StreetMinistry7SiteBuilder/1.0 (static site credits)'}
picks=json.load(open('picks.json'))
out=[]
for key,title in picks.items():
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',titles=title,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=2400,format='json'))
    p=list(json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))['query']['pages'].values())[0]
    ii=p['imageinfo'][0]; m=ii['extmetadata']; g=lambda k:re.sub('<[^>]+>','',m.get(k,{}).get('value','')).strip()
    dest=f'raw/{key}.jpg'
    if not os.path.exists(dest):
        for a in range(4):
            try:
                open(dest,'wb').write(urllib.request.urlopen(urllib.request.Request(ii['thumburl'],headers=UA)).read()); break
            except Exception as e: print('retry',key,e); time.sleep(3)
        time.sleep(1)
    out.append(dict(key=key,title=title.replace('File:',''),author=g('Artist'),license=g('LicenseShortName'),license_url=m.get('LicenseUrl',{}).get('value',''),source=ii['descriptionurl']))
    print(key,out[-1]['license'],out[-1]['author'][:40])
json.dump(out,open('credits.raw.json','w'),indent=2)

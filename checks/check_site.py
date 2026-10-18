from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.imgs=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.add(d['id'])
  if t=='h1':self.h1+=1
  if t=='img':self.imgs.append(d)
  for k in ['href','src']:
   if k in d:self.links.append(d[k])
pages={p.name:Page() for p in ROOT.glob('*.html')}
for name,p in pages.items():p.feed((ROOT/name).read_text());assert p.h1==1,(name,p.h1)
for name,p in pages.items():
 for a in p.imgs:assert 'alt' in a,(name,a)
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or href.startswith('//'):continue
  path=unquote(u.path) or name
  assert (ROOT/path).is_file(),(name,href)
  if u.fragment and path in pages:assert u.fragment in pages[path].ids,(name,href)
projects=json.loads((ROOT/'data/projects.json').read_text());pubs=json.loads((ROOT/'data/publications.json').read_text())
assert len({p['id'] for p in pubs})==len(pubs)
assert len({p['id'] for p in projects})==len(projects)
print(f'PASS: {len(pages)} pages; local links, assets, headings, and image alt text; {len(pubs)} publication records.')

#!/usr/bin/env python3
"""Lightweight, offline SEO consistency checker for this GitHub Pages site.
Run from anywhere: python3 tools/check_seo.py
No additional Python dependencies required.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
BASE='https://rmichielan.github.io/site/'
PAGES={
 'index.html':'',
 'research.html':'research.html',
 'publications.html':'publications.html',
 'interactive-papers.html':'interactive-papers.html',
 'about.html':'about.html',
 'contacts.html':'contacts.html',
 'paine.html':'paine.html',
 'interactive-papers/planted-cliques-rgg/index.html':'interactive-papers/planted-cliques-rgg/',
}
class HeadParser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.inhead=False; self.injson=False; self.json='';self.scripts=[];self.metas=[];self.links=[];self.title=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='head':self.inhead=True
  if not self.inhead:return
  if tag=='meta':self.metas.append(a)
  elif tag=='link':self.links.append(a)
  elif tag=='script' and a.get('type')=='application/ld+json':self.injson=True;self.json=''
  elif tag=='title':self.intitle=True
 def handle_endtag(self,tag):
  if tag=='script' and self.injson:self.injson=False;self.scripts.append(self.json)
  elif tag=='title':self.intitle=False
  elif tag=='head':self.inhead=False
 def handle_data(self,data):
  if self.injson:self.json+=data
  if getattr(self,'intitle',False):self.title+=data

def report():
 errors=[]; counted=0
 def ensure(condition,msg):
  nonlocal counted
  counted+=1
  if not condition:errors.append(msg)
 urls=[]
 for file,rel in PAGES.items():
  p=ROOT/file; txt=p.read_text(encoding='utf8'); parse=HeadParser();parse.feed(txt)
  canonical=BASE+rel
  for label in ('canonical',):
   tags=[l for l in parse.links if label in l.get('rel','').split()]
   ensure(len(tags)==1 and tags[0].get('href')==canonical,f'{file}: bad {label}')
  for key,expected in [('og:url',canonical),('og:site_name','Riccardo Michielan')]:
   matching=[m for m in parse.metas if m.get('property')==key]
   ensure(len(matching)==1 and matching[0].get('content')==expected,f'{file}: bad {key}')
  ensure(bool(parse.title.strip()),f'{file}: missing title')
  desc=[m for m in parse.metas if m.get('name')=='description']
  ensure(len(desc)==1 and len(desc[0].get('content',''))>=40,f'{file}: missing description')
  for field in ('og:image','twitter:image'):
   prop='property' if field.startswith('og:') else 'name'
   ms=[m for m in parse.metas if m.get(prop)==field]
   good=len(ms)==1 and ms[0].get('content','').startswith(BASE)
   ensure(good,f'{file}: bad {field}')
   if good:
    image=ROOT/unquote(urlsplit(ms[0]['content']).path.removeprefix('/site/'))
    ensure(image.is_file(),f'{file}: missing {image}')
    if image.is_file():
     import struct
     with image.open('rb') as fp:
      header=fp.read(24)
     valid=header[:8]==b'\x89PNG\r\n\x1a\n' and len(header)==24 and struct.unpack('>II',header[16:24])==(1200,630)
     ensure(valid,f'{file}: nonstandard social image dimensions {image}')
  ensure(len(parse.scripts)==1,f'{file}: JSON-LD count')
  if parse.scripts:
   try:
    data=json.loads(parse.scripts[0])
    page=data['@graph'][0]
    ensure(page['@type']=='WebPage' and page['url']==canonical,f'{file}: invalid JSON-LD page reference')
    ensure(page['isPartOf']['@id']==BASE+'#website',f'{file}: invalid site reference')
    if file=='publications.html':
     items=page['mainEntity']['itemListElement']
     ensure(len(items)==page['mainEntity']['numberOfItems'],f'{file}: articles count mismatch')
   except (ValueError,KeyError,TypeError,IndexError) as exc:errors.append(f'{file}: invalid JSON-LD: {exc}')
  ensure('https://riccardo1803.github.io/site/' not in txt,f'{file}: obsolete URL')
  urls.append(canonical)
 sm=ET.parse(ROOT/'sitemap.xml').getroot()
 locations=[x.text for x in sm.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
 ensure(len(locations)==len(set(locations))==len(urls) and set(locations)==set(urls),'sitemap URLs do not match canonical URLs')
 source=(ROOT/'src/pages/interactive-papers.html').read_text(encoding='utf8')
 ensure(BASE+'interactive-papers.html' in source,'editable source SEO is out of date')
 ensure((ROOT/'.nojekyll').is_file(),'missing .nojekyll')
 print(f'SEO checks: {counted-len(errors)}/{counted} passed on {len(PAGES)} pages.')
 for e in errors:print('FAIL:',e)
 return not errors

if __name__=='__main__':
 raise SystemExit(0 if report() else 1)

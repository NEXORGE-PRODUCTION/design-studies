from pathlib import Path
from html import escape as e
import json
root=Path(__file__).parent
designs=[r.split('|') for r in (root/'concepts.tsv').read_text().splitlines()]
def page(title,body,css,theme,fg,mode):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · Nexorge Design Studies</title><link rel="stylesheet" href="{css}"></head><body class="{mode}" style="--paper:#{theme};--accent:#{fg}">{body}</body></html>'''
def nav(name,section):
 return f'<header><a class="word" href="index.html">{e(name)}</a><nav><a href="collection.html">{e(section)}</a><a href="studio.html">About</a><a href="../index.html">Portfolio ↗</a></nav></header>'
def art(slug,mode,cat):
 if mode.startswith('photo'):return f'<img class="photo" src="../assets/{slug}.jpg" alt="{e(cat)} editorial photograph">'
 return '<div class="art" aria-hidden="true"><i></i><i></i><i></i></div>'
gallery=[]
for idx,(slug,name,cat,title,sub,section,*rest) in enumerate(designs):
 items=[item.split('~') for item in rest[:3]]
 bg,fg,mode=rest[3:]
 dark=slug in ['ember-table','ledger-counsel','orbit-mind']
 d=root/slug;d.mkdir(exist_ok=True)
 def write(file,label,body):
  (d/file).write_text(page(label,nav(name,section)+body+'<footer>Nexorge Design Studies <span>Independent portfolio concept</span></footer>','../style.css',bg,fg,('dark ' if dark else '')+f'layout{idx%3}'))
 def cards():
  return '<div class="cards">'+''.join(f'<a href="story-{j}.html"><small>{e(section)}</small><h3>{e(h)}</h3><p>{e(b)}</p><b>Explore ↗</b></a>' for j,(h,b) in enumerate(items))+'</div>'
 hero=art(slug,mode,cat)
 write('index.html',name,f'<main><section class="hero"><div><small>{e(cat)}</small><h1>{e(title)}</h1><p>{e(sub)}</p><a class="button" href="collection.html">Explore {e(section.lower())} ↗</a></div>{hero}</section><section><h2>{e(section)}</h2>{cards()}</section></main>')
 write('collection.html',section,f'<main><section><small>{e(name)}</small><h1>{e(section)}</h1><p>{e(sub)}</p>{cards()}</section></main>')
 for j,(h,b) in enumerate(items):
  nxt=(j+1)%len(items)
  write(f'story-{j}.html',h,f'<main><section class="hero"><div><small>{e(section)}</small><h1>{e(h)}</h1><p>{e(b)}</p><a class="button" href="story-{nxt}.html">Next · {e(items[nxt][0])} →</a></div>{hero}</section></main>')
 write('studio.html','About '+name,f'<main><section><small>About the concept</small><h1>{e(name)}</h1><p>{e(sub)}</p><h2>What to explore</h2>{cards()}</section></main>')
 gallery.append(f'<a class="tile" style="--tile:#{bg};color:#{fg}" href="{slug}/"><small>{e(cat)}</small><h3>{e(name)}</h3><span>{e(title)} ↗</span></a>')
(root/'index.html').write_text(page('Portfolio','<header><strong>NEXORGE</strong><span>Design portfolio</span></header><main><section><small>Independent web concepts</small><h1>Design studies.</h1><div class="gallery">'+''.join(gallery)+'</div></section></main>','style.css','f7f6f0','163c32',''))

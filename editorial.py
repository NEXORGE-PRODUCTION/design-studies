from pathlib import Path
from html import escape as esc
ROOT=Path(__file__).parent
def load(name):
    rows=[line.split('|') for line in (ROOT/name).read_text().splitlines()]
    return {row[0]:row[1:] for row in rows}
SCENES=load('scenes.tsv')
BRIEFS=load('briefs.tsv')
SELECTORS=load('selectors.tsv')
def render(slug,name,cat,title,sub,section,items,mode):
    model,layout,order,desk,object_title,p1,p2=SCENES[slug]
    essay,intro,*tail=BRIEFS[slug]
    notes=tail[:3]
    tool,prompt=tail[3:]
    photos=[f'../assets/editorial/{p}.jpg' for p in (p1,p2)]
    cover=f'../assets/{slug}.jpg' if mode.startswith('photo') else photos[0]
    def img(src,hero=False):
        return f'<img src="{src}" alt="" {"fetchpriority=high" if hero else "loading=lazy"}>'
    def image_label(i):
        return f'<a class="plate" href="story-{i}.html">{img([photos[0],photos[1],cover][i])}<div><h3>{items[i][0]}</h3><p>{items[i][1]}</p><span>Read more ↗</span></div></a>'
    plates=f'<section class="chapter collection"><div class="line"><h2>{section}</h2><a href="collection.html">View all ↗</a></div><div class="plates">' + ''.join(image_label(i) for i in range(3))+'</div></section>'
    journal=f'<section class="chapter essay">{img(photos[1])}<div><small>{desk}</small><h2>{essay}</h2><p>{intro}</p><p>{notes[0]}</p><a href="studio.html">About {name} →</a></div></section>'
    studio=f'<section class="chapter studio" data-model="{model}"><div><small>Interactive study</small><h2>{object_title}</h2><p class="model-note">Drag the model to inspect its form, or use the rotation buttons.</p><button disabled data-turn="-.45" aria-label="Rotate left">←</button> <button disabled data-turn=".45" aria-label="Rotate right">→</button></div><div class="viewport">{img(cover)}</div></section>'
    cards=''.join(f'<details {"open" if i==0 else ""}><summary>{h}</summary><p>{notes[i]}</p><a href="story-{i}.html">Explore {h.lower()} →</a></details>' for i,(h,b) in enumerate(items))
    guide=f'<section class="chapter guide"><div><small>{section}</small><h2>{desk}</h2></div><div>{cards}</div></section>'
    options=''.join(f'<option>{h}</option>' for h,b in items)
    workbook=f'<section class="chapter workbook-section"><div><small>Take it with you</small><h2>{tool}</h2><p>Choose a focus and download your notes as a text file.</p></div><form class="workbook" data-slug="{slug}" data-title="{tool}"><label>Focus<select name="focus">{options}</select></label><label>{prompt}<textarea name="notes" rows="3"></textarea></label><button class="button">Download my notes ↓</button></form></section>'
    opening=f'<section class="opening {layout}"><div class="opening-copy"><small>{cat}</small><h1>{title}</h1><p>{sub}</p><a class="button" href="#collection">Explore {section.lower()} ↘</a></div><div class="opening-image">{img(cover,True)}</div></section>'
    contents={'plates':plates.replace('class="chapter collection"','id="collection" class="chapter collection"'),'journal':journal,'studio':studio}
    question,*choices=SELECTORS[slug]
    tabs=''.join(f'<button type="button" data-choice="{i}" aria-pressed="{str(i==0).lower()}">{esc(label)}</button>' for i,label in enumerate(choices))
    answers=''.join(f'<div data-answer="{i}" {"" if i==0 else "hidden"}><h3>{esc(h)}</h3><p>{esc(notes[i])}</p><a href="story-{i}.html">Explore {esc(h.lower())} ↗</a></div>' for i,(h,b) in enumerate(items))
    chooser=f'<section class="chapter chooser"><h2>{esc(question)}</h2><div class="choice-shell"><div class="choices">{tabs}</div><div class="answers" aria-live="polite">{answers}</div></div></section>'
    return '<main>'+opening+contents[order.split()[0]]+chooser+''.join(contents[k] for k in order.split()[1:])+guide+workbook+'</main><script type="module" src="../assets/study.js"></script>'

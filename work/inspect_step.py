import re,json
from pathlib import Path
src=Path('C:/Users/brian/Downloads/raspberry-pi-4-model-b-1.snapshot.3/Raspberry Pi 4 Model B.STEP')
s=src.read_text()
es={int(k):v for k,v in re.findall(r'#(\d+)\s*=\s*(.*?);',s,re.S)}
refs={k:list(map(int,re.findall(r'#(\d+)',v))) for k,v in es.items()}
rev={}
for k,rs in refs.items():
 for r in rs:rev.setdefault(r,[]).append(k)
def follow(k,typ):return [r for r in rev.get(k,[]) if es[r].lstrip().startswith(typ+' ')]
def descendants(k):
 seen=set();todo=[k]
 while todo:
  i=todo.pop()
  if i in seen:continue
  seen.add(i);todo+=refs.get(i,[])
 return seen
results=[]
for k,v in es.items():
 if not v.startswith('PRODUCT ') or "'PCB," not in v:continue
 forms=follow(k,'PRODUCT_DEFINITION_FORMATION')
 for f in forms:
  for d in follow(f,'PRODUCT_DEFINITION'):
   for p in follow(d,'PRODUCT_DEFINITION_SHAPE'):
    for sd in follow(p,'SHAPE_DEFINITION_REPRESENTATION'):
     rep=refs[sd][-1]
     seen=descendants(rep)
     # representation relationships can connect topology-bearing reps
     for rel in follow(rep,'SHAPE_REPRESENTATION_RELATIONSHIP'):
      seen|=descendants(rel)
     verts=[];cyl=[]
     for i in seen:
      if es[i].startswith('VERTEX_POINT '):
       point=es[refs[i][-1]]
       nums=re.search(r'\(\s*([^()]*)\)\s*\)',point)
       if nums:verts.append(list(map(float,nums[1].split(','))))
      if es[i].startswith('CYLINDRICAL_SURFACE '):cyl.append((i,es[i]))
     results.append({'product':k,'definition':d,'representation':rep,'vertices':len(verts),'bounds':[[min(v[j] for v in verts) for j in range(3)],[max(v[j] for v in verts) for j in range(3)]] if verts else None,'cylinders':cyl})
print(json.dumps(results,indent=2))
Path('work/step_pcb_analysis.json').write_text(json.dumps(results,indent=2))

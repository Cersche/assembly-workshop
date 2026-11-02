import re,sys
from collections import Counter
for f in sys.argv[1:]:
    t=open(f).read(); v=[tuple(map(float,m)) for m in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)',t)]
    e=Counter(); par={}
    def find(a):
        while par.setdefault(a,a)!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for i in range(0,len(v),3):
        for a,b in ((0,1),(1,2),(2,0)): e[tuple(sorted((v[i+a],v[i+b])))]+=1
        par[find(v[i])]=find(v[i+1]); par[find(v[i+1])]=find(v[i+2])
    comps=len({find(x) for x in set(v)})
    print(f,len(v)//3,'tris | open edges',sum(c!=2 for c in e.values()),'| pieces',comps,'|',' '.join('%.1f..%.1f'%(min(c[i] for c in v),max(c[i] for c in v)) for i in range(3)))

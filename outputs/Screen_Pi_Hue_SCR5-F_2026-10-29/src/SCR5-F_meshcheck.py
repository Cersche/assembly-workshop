"""SCR5-C mesh checks: shells, closure, winding, volume, bounds. Python 3.10 stdlib."""
import struct, sys
from collections import defaultdict
def read(p):
    d=open(p,'rb').read(); n=struct.unpack_from('<I',d,80)[0]; V={}; T=[]
    for i in range(n):
        c=struct.unpack_from('<9f',d,96+50*i); t=[]
        for k in (0,3,6):
            q=c[k:k+3]; t.append(V.setdefault(q,len(V)))
        T.append(t)
    return list(V),T
def check(p):
    V,T=read(p); E=defaultdict(int); par={}
    def f(a):
        while par.setdefault(a,a)!=a: par[a]=par[par[a]]; a=par[a]
        return a
    deg=0
    for a,b,c in T:
        if len({a,b,c})<3: deg+=1
        for u,v in ((a,b),(b,c),(c,a)): E[(u,v)]+=1; par[f(u)]=f(v)
    bad=sum(1 for (u,v),k in E.items() if k!=1 or E.get((v,u),0)!=1)
    comps=defaultdict(list)
    for t in T: comps[f(t[0])].append(t)
    vols=[]
    for ts in comps.values():
        s=0
        for a,b,c in ts:
            (x1,y1,z1),(x2,y2,z2),(x3,y3,z3)=V[a],V[b],V[c]
            s+=(x1*(y2*z3-y3*z2)-x2*(y1*z3-y3*z1)+x3*(y1*z2-y2*z1))/6
        bb=[[min(V[i][k] for t in ts for i in t),max(V[i][k] for t in ts for i in t)] for k in range(3)]
        vols.append((round(s,2),len(ts),[[round(a,2),round(b,2)] for a,b in bb]))
    bb=[[round(min(v[k] for v in V),3),round(max(v[k] for v in V),3)] for k in range(3)]
    print(p,'tris',len(T),'degenerate',deg,'bad_edges',bad,'bounds',bb)
    for v in vols: print('  shell vol',v)
for p in sys.argv[1:]: check(p)

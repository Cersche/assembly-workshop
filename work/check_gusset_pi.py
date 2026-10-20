exec(open('work/analyze_pi.py').read().split('rs=[]')[0])
pts=[(v[0]-44,69-v[2],v[1]+13.900009155273438) for v in par]
hits=[]
for x,y,z in pts:
 for cx in [-46,-34,34,46]:
  top=16.5-max(0,y-11)*6.3/11
  if abs(x-cx)<.999 and 9.001<y<21.999 and 10.001<z<top-.001:hits.append((x,y,z,cx,top-z))
print('penetrating Pi vertices in gussets',len(hits));print(hits[:10]);print('maxdepth',max((p[-1] for p in hits),default=0))

exec(open('work/analyze_pi.py').read().split('rs=[]')[0])
from collections import Counter
for digits in [5,4,3]:
 counts=Counter()
 for t in ts:
  q=[tuple(round(x,digits) for x in v) for v in t]
  if len(set(q))<3:continue
  for j in range(3):counts[tuple(sorted([q[j],q[(j+1)%3]]))]+=1
 print(digits,Counter(counts.values()))

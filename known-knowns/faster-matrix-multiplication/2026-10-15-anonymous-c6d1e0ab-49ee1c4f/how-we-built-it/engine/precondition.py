"""Exact invertible coordinate shears for sparse rational tensor factors."""
import time
from collections import Counter,defaultdict
from fractions import Fraction

def clean(rows,limit=5,return_moves=False):
 moves=[]
 d=max(k for x in rows for k in x)+1
 for step in range(limit):
  dense=[x for x in rows if len(x)>d//3]
  if not dense:break
  counts=Counter(k for x in rows if len(x)<=d//3 for k in x)
  ks=sorted(range(d),key=lambda k:(counts[k],k))[:8]
  best=None
  # Prototype of up to 33 evenly spaced dense rows, coefficientwise mode after pivot normalization.
  sample=dense[::max(1,len(dense)//33)][:33]
  for k in ks:
   usable=[x for x in sample if x.get(k)]
   if len(usable)<len(sample)*.8:continue
   mode=defaultdict(Counter)
   for x in usable:
    pivot=x[k]
    for j,v in x.items():mode[j][v/pivot]+=1
   base={j:max(ct,key=ct.get) for j,ct in mode.items() if max(ct.values())>len(usable)//2}
   base[k]=Fraction(1)
   # Estimate exact nnz cost on sample and small-row pivot incidence.
   cost=counts[k]*len(base)
   for x in sample:
    if k not in x:cost+=len(x)*max(1,len(dense)//len(sample));continue
    ratio=x[k];support=set(x)|set(base)
    cost+=(1+sum(x.get(j,0)!=ratio*base.get(j,0) for j in support if j!=k))*max(1,len(dense)//len(sample))
   if best is None or cost<best[0]:best=(cost,k,base)
  if best is None:break
  _,k,base=best;t0=time.time();out=[]
  for x in rows:
   if k not in x:out.append(x);continue
   ratio=x[k]/base[k];rr=dict(x)
   for j,v in base.items():
    if j==k:continue
    y=rr.get(j,0)-ratio*v
    if y:rr[j]=y
    else:rr.pop(j,None)
   out.append(rr)
  before=sum(map(len,rows));after=sum(map(len,out))
  print('mode step',step,'base',len(base),'pivot',k,'inc',counts[k],'nnz',before,'->',after,'dense',len(dense),'time',time.time()-t0,flush=True)
  if after>=before:break
  rows=out
  moves.append((k,base))
 return (rows,moves) if return_moves else rows

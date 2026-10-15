"""Sparse exact-coordinate absorption for LITA. See NOTES.md.
Modular kernels only propose dependencies. All lifted dependencies are checked
after denominator clearing with signed integers before absorption over Q.
"""
import sys,os,json,struct,subprocess,time,signal,random,math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'data'))
import sa
from flint import nmod_mat
WORK=Path('work');SERIAL=0

def canonical(raw,p,r):
 if not raw:return []
 M=nmod_mat(len(raw),r,[row.get(str(t),0) for row in raw for t in range(r)],p)
 R,rank=M.rref();assert rank==len(raw)
 return [{t:int(R[i,t]) for t in range(r) if R[i,t]} for i in range(rank)]

def reconstruct(collected):
 pivots=[tuple(min(v) for v in rows) for p,rows in collected]
 if any(x!=pivots[0] for x in pivots):return None
 basis=[]
 for i in range(len(collected[0][1])):
  support=set().union(*(set(rows[i]) for p,rows in collected));vec={}
  for t in support:
   val,mod=0,1
   for p,rows in collected:
    val+=mod*((rows[i].get(t,0)-val)*pow(mod%p,-1,p)%p);mod*=p
   x=sa._ratrec(val,mod)
   if x is None:return None
   if x:vec[t]=x
  basis.append(vec)
 return basis

def integer_factors(uv):
 D=[1,1]
 for row in uv:
  for j in range(2):
   for x in row[j].values():D[j]=math.lcm(D[j],x.denominator)
 out=[]
 for row in uv:
  out.append(tuple([(k,x.numerator*(D[j]//x.denominator)) for k,x in row[j].items()] for j in range(2)))
 return out

def verify_basis(basis,uvint,dv):
 for vec in basis:
  dl=1
  for x in vec.values():dl=math.lcm(dl,x.denominator)
  acc={}
  for t,lam in vec.items():
   li=lam.numerator*(dl//lam.denominator);u,v=uvint[t]
   for a,ua in u:
    au=li*ua;base=a*dv
    for b,vb in v:
     k=base+b;acc[k]=acc.get(k,0)+au*vb
  if any(acc.values()):return False
 return True

def exact_kernel(n,terms,rng=None,max_primes=6):
 global SERIAL
 SERIAL+=1;prefix=WORK/f'kernel_{os.getpid()}_{SERIAL}'
 from precondition import clean
 uv=[(t[0],t[1]) for t in terms];rawcost=sum(len(u)*len(v) for u,v in uv);ref=None
 if rawcost>10000000:
  U=clean([u for u,v in uv]);V=clean([v for u,v in uv]);transformed=list(zip(U,V));newcost=sum(len(u)*len(v) for u,v in transformed)
  if newcost<rawcost:uv=transformed;ref='mode'
 print(f'  kernel {SERIAL} n={n} r={len(terms)} ref={ref} outer_nnz={sum(len(u)*len(v) for u,v in uv)}',flush=True)
 uvint=None;collected=[];bestdim=None
 for pi,p in enumerate(sa.PRIMES[:max_primes]):
  path=prefix.with_suffix(f'.p{pi}.bin');logpath=prefix.with_suffix(f'.p{pi}.log');outpath=prefix.with_suffix(f'.p{pi}.json')
  with open(path,'wb') as f:
   f.write(struct.pack('<IIII',len(terms),n[1]*n[2],n[0]*n[1]*n[1]*n[2],p))
   for u,v in uv:
    rows=[]
    for row in (u,v):
     r=[]
     for k,x in row.items():
      m=x.numerator%p*pow(x.denominator%p,-1,p)%p
      if m:r.append((k,m))
     rows.append(r)
    f.write(struct.pack('<II',len(rows[0]),len(rows[1])))
    for row in rows:
     for k,m in row:f.write(struct.pack('<II',k,m))
  engine=WORK/('dual_kernel' if rawcost>10000000 else 'sparse_kernel')
  with open(logpath,'w') as err:
   proc=subprocess.Popen(['nice','-n','19',str(engine),str(path),str(outpath),'180'],stderr=err)
   prefix.with_suffix(f'.p{pi}.pid').write_text(str(proc.pid))
   try:rc=proc.wait(timeout=190)
   except BaseException:
    proc.kill();proc.wait();raise
  if rc:raise RuntimeError(f'sparse kernel failed: {logpath}')
  raw=json.load(open(outpath));path.unlink()
  if not raw:print(f'  exact kernel dimension=0 (full rank mod p); {logpath}',flush=True);return []
  rows=canonical(raw,p,len(terms))
  if bestdim is None or len(rows)<bestdim:collected=[];bestdim=len(rows)
  if len(rows)>bestdim:continue
  collected.append((p,rows));basis=reconstruct(collected)
  if basis is None:print('  reconstruction needs another prime',flush=True);continue
  if uvint is None:uvint=integer_factors(uv)
  if verify_basis(basis,uvint,n[1]*n[2]):
   print(f'  exact kernel dimension={len(basis)} verified, primes={len(collected)}; {logpath}',flush=True);return basis
  print('  exact dependency test rejected one-prime lift; collecting another prime',flush=True)
 raise RuntimeError('rational kernel reconstruction did not verify')

sa.exact_nullspace_crt=exact_kernel

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('parent');ap.add_argument('--axis',type=int,default=0);ap.add_argument('--top',type=int,default=1);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--out',default='work');ap.add_argument('--cap',type=int,default=1800);a=ap.parse_args()
 signal.alarm(a.cap);print('PID',os.getpid(),flush=True)
 sa.run(a.parent,a.axis,a.top,a.seed,a.out,verify=False,verbose=True)
if __name__=='__main__':main()

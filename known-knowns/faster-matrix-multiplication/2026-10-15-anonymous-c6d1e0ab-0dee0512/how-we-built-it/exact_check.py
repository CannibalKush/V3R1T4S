#!/usr/bin/env python3
"""Independent exact checker. Applies invertible shears to the candidate and
matrix-multiplication definition, then checks every coefficient with a rigorous
CRT residual bound. Requires the adjacent tensor_check.cpp and a C++ compiler.
No search engine is imported. See NOTES.md for the proof and validation.
"""
import sys,os,json,math,time,signal,struct,subprocess,hashlib,argparse
from pathlib import Path
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


def is_prime(n):
 if n<2:return False
 for p in (2,3,5,7,11,13,17,19,23,29,31,37):
  if n%p==0:return n==p
 d,s=n-1,0
 while d%2==0:d//=2;s+=1
 for a in (2,3,5,7,11,13,17,19,23,29,31,37):
  x=pow(a,d,n)
  if x in (1,n-1):continue
  for _ in range(s-1):
   x=x*x%n
   if x==n-1:break
  else:return False
 return True

def apply_moves(x,moves):
 for k,base in moves:
  if k not in x:continue
  ratio=x[k]/base[k];rr=dict(x)
  for j,v in base.items():
   if j==k:continue
   y=rr.get(j,0)-ratio*v
   if y:rr[j]=y
   else:rr.pop(j,None)
  x=rr
 return x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('scheme');ap.add_argument('--expect-rank',type=int);ap.add_argument('--cap',type=int,default=900);ap.add_argument('--no-precondition',action='store_true');ap.add_argument('--work',default='work');a=ap.parse_args()
 signal.alarm(a.cap);print('PID',os.getpid(),flush=True);work=Path(a.work);work.mkdir(exist_ok=True)
 d=json.load(open(a.scheme));n1,n2,n3=d['n'];dims=[n1*n2,n2*n3,n3*n1]
 if d.get('encoding')!='sparse_flat_pairs':raise ValueError('expected sparse_flat_pairs')
 axes=[]
 for name,dim in zip('uvw',dims):
  rows=[]
  for row in d[name]:
   if len(row)%2:raise ValueError('odd sparse row')
   x={}
   for k,v in zip(row[::2],row[1::2]):
    if type(k) is not int or not 0<=k<dim or type(v) not in (int,str):raise ValueError('invalid coefficient/index')
    x[k]=x.get(k,0)+Fraction(v)
   rows.append({k:v for k,v in x.items() if v})
  axes.append(rows)
 if len(set(map(len,axes)))!=1:raise ValueError('unequal term counts')
 original=[t for t in zip(*axes) if all(t)];rank=len(original)
 if a.expect_rank is not None and rank!=a.expect_rank:raise ValueError('rank mismatch')
 axes=[list(x) for x in zip(*original)];transformed=[];moves=[]
 for j,rows in enumerate(axes):
  if not a.no_precondition and sum(map(len,rows))>rank*40:
   out,mm=clean(rows,return_moves=True)
  else:out,mm=rows,[]
  transformed.append(out);moves.append(mm)
  print('axis',j,'moves',len(mm),'nnz',sum(map(len,rows)),'->',sum(map(len,out)),flush=True)
 terms=list(zip(*transformed));unit=[[apply_moves({i:Fraction(1)},moves[j]) for i in range(dim)] for j,dim in enumerate(dims)]
 for i in range(n1):
  for j in range(n2):
   for k in range(n3):terms.append(({b:-v for b,v in unit[0][i*n2+j].items()},unit[1][j*n3+k],unit[2][k*n1+i]))
 D=1;S=Fraction(0);products=0
 for term in terms:
  maximum=Fraction(1)
  for row in term:
   for x in row.values():D=math.lcm(D,x.denominator)
   maximum*=max(map(abs,row.values()))
  S+=maximum;products+=math.prod(map(len,term))
 bound=(2*D**3*S.numerator+S.denominator-1)//S.denominator
 print('exact-bound D=',D,'S=',S,'bound_bits=',bound.bit_length(),'products_per_prime=',products,flush=True)
 source=work/'tensor_check_embedded.cpp';binary=work/'tensor_check'
 if not source.exists() or source.read_text()!=CPP_SOURCE:source.write_text(CPP_SOURCE)
 if not binary.exists() or binary.stat().st_mtime<source.stat().st_mtime:
  subprocess.run(['nice','-n','19','cc','-O3','-std=c++17','-x','c++',str(source),'-lc++','-o',str(binary)],check=True,timeout=60)
 prime=(1<<61)-1;prod=1;np=0
 while prod<=bound:
  while not is_prime(prime) or D%prime==0:prime-=2
  checkpoint=work/f'check_{os.getpid()}_p{np}.bin'
  with checkpoint.open('wb') as f:
   f.write(struct.pack('<IIIIQ',*dims,len(terms),prime))
   for term in terms:
    f.write(struct.pack('<III',*(len(x) for x in term)))
    for row in term:
     for k,x in row.items():f.write(struct.pack('<IQ',k,x.numerator%prime*pow(x.denominator%prime,-1,prime)%prime))
  proc=subprocess.Popen(['nice','-n','19',str(binary),str(checkpoint),str(a.cap)])
  (work/f'check_{os.getpid()}_p{np}.pid').write_text(str(proc.pid))
  try:rc=proc.wait(timeout=a.cap+5)
  except BaseException:proc.kill();proc.wait();raise
  checkpoint.unlink()
  if rc:print('FAIL exact coefficient comparison or computational limit',flush=True);return 1
  prod*=prime;np+=1;prime-=2
 print(f'PASS exact-CRT format={n1}x{n2}x{n3} rank={rank} primes={np} D={D} bound_bits={bound.bit_length()} product_bits={prod.bit_length()}',flush=True)
 print('PROVED-HERE: transformed residual is zero by its integer bound; invertible shears imply original Brent equations.',flush=True)
 return 0
CPP_SOURCE = '// Definition-based sparse tensor coefficient checker, one output coordinate at a time.\n#include <algorithm>\n#include <chrono>\n#include <cstdint>\n#include <fstream>\n#include <iostream>\n#include <stdexcept>\n#include <vector>\n#include <unistd.h>\nusing namespace std;using E=pair<uint32_t,uint64_t>;using Row=vector<E>;uint64_t p;\nuint64_t mul(uint64_t a,uint64_t b){__uint128_t t=(__uint128_t)a*b;if(p==2305843009213693951ULL){uint64_t x=(uint64_t)(t&p)+(uint64_t)(t>>61);return x>=p?x-p:x;}return t%p;}\nuint32_t rd(ifstream&f){uint32_t x;f.read((char*)&x,4);if(!f)throw runtime_error("truncated input");return x;}\nuint64_t rd64(ifstream&f){uint64_t x;f.read((char*)&x,8);if(!f)throw runtime_error("truncated input");return x;}\nint main(int argc,char**argv){try{\n cerr<<"PID "<<getpid()<<endl;ifstream f(argv[1],ios::binary);uint32_t du=rd(f),dv=rd(f),dw=rd(f),r=rd(f);p=rd64(f);double cap=stod(argv[2]);auto start=chrono::steady_clock::now();\n vector<Row> u(r),v(r),byw(dw);uint64_t products=0;\n for(uint32_t t=0;t<r;t++){uint32_t nu=rd(f),nv=rd(f),nw=rd(f);for(uint32_t j=0;j<nu;j++){uint32_t a=rd(f);uint64_t x=rd64(f);if(x)u[t].emplace_back(a,x);}for(uint32_t j=0;j<nv;j++){uint32_t a=rd(f);uint64_t x=rd64(f);if(x)v[t].emplace_back(a,x);}for(uint32_t j=0;j<nw;j++){uint32_t a=rd(f);uint64_t x=rd64(f);if(x)byw[a].emplace_back(t,x);}}\n vector<uint64_t> acc((size_t)du*dv);vector<uint8_t> flag((size_t)du*dv);vector<uint32_t> touched;uint64_t bad=0;\n for(uint32_t c=0;c<dw;c++){\n  if(chrono::duration<double>(chrono::steady_clock::now()-start).count()>cap)throw runtime_error("time cap");\n  touched.clear();\n  for(auto tw:byw[c]){auto t=tw.first;auto w=tw.second;products+=(uint64_t)u[t].size()*v[t].size();for(auto au:u[t]){uint64_t x=mul(au.second,w);uint32_t base=au.first*dv;for(auto bv:v[t]){uint32_t k=base+bv.first;if(!flag[k]){flag[k]=1;touched.push_back(k);}uint64_t z=acc[k]+mul(x,bv.second);acc[k]=z>=p?z-p:z;}}}\n  for(auto k:touched){if(acc[k]){if(!bad)cerr<<"first_bad (a,b,c)="<<k/dv<<","<<k%dv<<","<<c<<" residual="<<acc[k]<<endl;bad++;}acc[k]=0;flag[k]=0;}\n  if(c%100==0)cerr<<"output="<<c<<"/"<<dw<<" products="<<products<<" bad="<<bad<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;\n }\n cout<<(bad?"FAIL":"PASS")<<" modulus="<<p<<" nonzero_residuals="<<bad<<" products="<<products<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;return bad?1:0;\n }catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 2;}}\n'
if __name__=='__main__':sys.exit(main())

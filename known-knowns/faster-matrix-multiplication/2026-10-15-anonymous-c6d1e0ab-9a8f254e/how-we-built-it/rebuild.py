#!/usr/bin/env python3
"""Regenerate a pinned candidate package from its exact parent snapshot."""
import argparse,hashlib,json,os,random,signal,subprocess,sys
from pathlib import Path

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(sa,n,t):
 wanted=tuple(sorted(n));a,b,c=n
 rev=((b,a,c),[({(i%b)*a+i//b:x for i,x in u.items()},{(i%a)*c+i//a:x for i,x in w.items()},{(i%c)*b+i//c:x for i,x in v.items()}) for u,v,w in t])
 for nr,tr in [(n,t),rev]:
  for axis in range(3):
   nn,tt=sa.rotate_to(nr,tr,axis)
   if nn==wanted:return nn,tt
 raise RuntimeError('dimension permutation')

def run(args,output=None,timeout=190):
 p=subprocess.Popen(args,stdout=output,stderr=subprocess.STDOUT);print('CHILD_PID',p.pid,flush=True)
 try:rc=p.wait(timeout=timeout)
 except BaseException:p.kill();p.wait();raise
 if rc:raise RuntimeError(f'command failed with status {rc}')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work-dir',required=True);a=ap.parse_args()
 root=Path(__file__).resolve().parent;cfg=json.load((root/'rebuild.json').open());manifest=json.load((root/'engine_manifest.json').open())
 for rel,expected in manifest.items():
  actual=sha(root/rel)
  if actual!=expected:raise RuntimeError(f'source checksum mismatch: {rel}')
 dest=Path(a.work_dir).resolve()
 if dest.exists() and any(dest.iterdir()):raise RuntimeError('work directory must be empty')
 dest.mkdir(parents=True,exist_ok=True);os.chdir(dest);Path('work').mkdir()
 signal.alarm(1800);os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.environ['FLINT_NUM_THREADS']='1'
 print('PID',os.getpid(),flush=True);print('Python',sys.version,flush=True)
 for name in ['sparse_kernel','dual_kernel']:
  run(['nice','-n','19','cc','-O3','-std=c++17','-Wno-unqualified-std-cast-call','-x','c++',str(root/'engine'/f'{name}.cpp'),'-lc++','-o',str(dest/'work'/name)],timeout=60)
 sys.path.insert(0,str(root/'engine'));import fast_sa as fs
 import flint,numpy
 flint.ctx.threads=1
 print('numpy',numpy.__version__,'python-flint',flint.__version__,'FLINT_threads',flint.ctx.threads,flush=True)
 # Step 0 always computes the canonical JSON from the shipped source input.
 boot=cfg.get('bootstrap')
 if boot:
  source=root/boot['file'];assert sha(source)==boot['sha256']
  if boot['kind']=='lita_npz':
   from fractions import Fraction
   z=numpy.load(source,allow_pickle=False);raw=z['metadata_json'].tolist();meta=json.loads(raw.decode() if isinstance(raw,bytes) else str(raw));n=tuple(meta.get('tensor',meta.get('n')));rank=int(meta['rank']);axes=[]
   for axis in 'uvw':
    ip,ix,nu,de=[z[f'{axis}_{key}'] for key in ['indptr','indices','numerators','denominators']];rows=[]
    for t in range(rank):
     row={}
     for k in range(ip[t],ip[t+1]):
      index=int(ix[k]);index=(index%n[2])*n[0]+index//n[2] if axis=='w' else index
      row[index]=row.get(index,0)+Fraction(int(nu[k]),int(de[k]))
     rows.append({k:v for k,v in row.items() if v})
    axes.append(rows)
   terms=list(zip(*axes))
  elif boot['kind']=='json':n,terms=fs.sa.load(source)
  else:raise RuntimeError('unknown input kind')
  n,terms=canonical(fs.sa,n,terms);current=dest/'seed.json';fs.sa.save(current,n,terms,boot['seed_note'])
  actual=sha(current);print('STEP_0_SOURCE_SHA256',boot['sha256'],'CANONICAL_SEED_SHA256',actual,flush=True)
  if actual!=cfg['parent_sha256']:raise RuntimeError('canonical seed checksum differs')
 else:
  current=root/cfg['parent_file'];assert sha(current)==cfg['parent_sha256']
 for i,step in enumerate(cfg['steps']):
  assert sha(current)==step['parent_sha256']
  n,t=fs.sa.load(current);nr,tr=fs.sa.rotate_to(n,t,step.get('axis',0))
  if step.get('operation')=='canonicalize':
   cn,ct=canonical(fs.sa,n,t);out=dest/f'step_{i+1:02d}_{fs.sa.fmt(cn)}_r{len(ct)}.json';fs.sa.save(out,cn,ct,step['note']);actual=sha(out);print('CANONICAL_ALIAS_SHA256',i+1,actual,flush=True)
   if actual!=step['sha256']:raise RuntimeError('canonical alias differs')
   current=out;continue
  f=tuple(map(tuple,step['f']));e=tuple(map(tuple,step['e']));ns,ts=fs.sa.slice_dim1(nr,tr,f,e)
  print('STEP',i+1,'parent',n,len(t),'axis',step['axis'],'f',f,'e',e,'raw',len(ts),flush=True)
  ts,k=fs.sa.absorb_all(ns,ts,random.Random(step['rng_seed']),log=lambda s:print(s,flush=True),max_rounds=step['max_rounds'])
  cn,ct=fs.sa.rotate_to(ns,ts,3-step['axis'])
  if step['canonicalize']:cn,ct=canonical(fs.sa,cn,ct)
  if list(cn)!=step['n'] or len(ct)!=step['rank']:raise RuntimeError('rebuilt dimensions/rank differ')
  out=dest/f'step_{i+1:02d}_{fs.sa.fmt(cn)}_r{len(ct)}.json';fs.sa.save(out,cn,ct,step['note']);actual=sha(out)
  print('STEP_SHA256',i+1,actual,flush=True)
  if actual!=step['sha256']:raise RuntimeError(f'byte checksum differs at step {i+1}')
  current=out
 with (dest/'exact_check_output.txt').open('w') as f:run(['nice','-n','19',sys.executable,str(root/'exact_check.py'),str(current),'--expect-rank',str(cfg['steps'][-1]['rank']),'--work',str(dest/'verify_work'),'--cap','900'],output=f,timeout=905)
 result=dict(scheme=str(current),sha256=sha(current),expected_sha256=cfg['steps'][-1]['sha256'],steps=len(cfg['steps']),exact_check='PASS')
 (dest/'result.json').write_text(json.dumps(result,indent=2));print('REBUILD PASS',json.dumps(result),flush=True)
if __name__=='__main__':main()

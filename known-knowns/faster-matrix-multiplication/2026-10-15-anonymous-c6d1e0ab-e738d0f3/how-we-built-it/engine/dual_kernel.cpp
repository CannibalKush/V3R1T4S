// Sparse coordinate equations for the left kernel of rows U tensor V.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <unistd.h>
#include <stdexcept>
#include <vector>
using namespace std;using E=pair<uint32_t,uint32_t>;using Row=vector<E>;uint32_t p;
uint32_t power(uint32_t a,uint32_t e){uint64_t y=1;while(e){if(e&1)y=y*a%p;a=(uint64_t)a*a%p;e>>=1;}return y;}
Row sub(const Row&a,const Row&b,uint32_t f){Row c;c.reserve(a.size()+b.size());size_t i=0,j=0;while(i<a.size()||j<b.size()){uint32_t k,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){c.push_back(a[i++]);continue;}if(i==a.size()||b[j].first<a[i].first){k=b[j].first;x=(p-(uint64_t)f*b[j++].second%p)%p;}else{k=a[i].first;x=(a[i++].second+p-(uint64_t)f*b[j++].second%p)%p;}if(x)c.emplace_back(k,x);}return c;}
uint32_t rd(ifstream&f){uint32_t x;f.read((char*)&x,4);if(!f)throw runtime_error("truncated input");return x;}
int main(int argc,char**argv){try{
 ifstream f(argv[1],ios::binary);uint32_t r=rd(f),dv=rd(f),dc=rd(f);p=rd(f);double cap=stod(argv[3]);auto start=chrono::steady_clock::now();
 vector<Row> eq(dc);uint64_t inputnnz=0;vector<uint32_t> coords;
 for(uint32_t t=0;t<r;t++){uint32_t nu=rd(f),nv=rd(f);Row u,v;for(uint32_t j=0;j<nu;j++){uint32_t a=rd(f),x=rd(f);u.emplace_back(a,x);}for(uint32_t j=0;j<nv;j++){uint32_t a=rd(f),x=rd(f);v.emplace_back(a,x);}for(auto a:u)for(auto b:v){uint32_t x=(uint64_t)a.second*b.second%p;if(x){uint32_t c=a.first*dv+b.first;eq[c].emplace_back(t,x);inputnnz++;if(inputnnz>150000000ULL)throw runtime_error("input storage cap");}}}
 for(uint32_t c=0;c<dc;c++)if(!eq[c].empty())coords.push_back(c);
 for(auto c:coords){uint32_t inv=power(eq[c][0].second,p-2);for(auto &x:eq[c])x.second=(uint64_t)x.second*inv%p;}
 sort(coords.begin(),coords.end(),[&](uint32_t a,uint32_t b){if(eq[a].size()!=eq[b].size())return eq[a].size()<eq[b].size();return eq[a]<eq[b];});
 coords.erase(unique(coords.begin(),coords.end(),[&](uint32_t a,uint32_t b){return eq[a]==eq[b];}),coords.end());
 if(coords.size()<15ULL*r){cerr<<"Hybrid: row elimination selected, r="<<r<<" coordinates="<<coords.size()<<endl;char* call[]={const_cast<char*>("work/sparse_kernel"),argv[1],argv[2],argv[3],nullptr};execv(call[0],call);throw runtime_error("row engine exec failed");}

 vector<Row> piv(r);uint64_t stored=0,ops=0;uint32_t rank=0;vector<uint8_t> used(dc);
 cerr<<"r="<<r<<" coordinates="<<coords.size()<<" inputnnz="<<inputnnz<<endl;
 auto expired=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count()>cap;};
 auto insert=[&](uint32_t c){
  used[c]=1;Row row=eq[c];
  while(!row.empty()&&!piv[row[0].first].empty()){
   if(expired())throw runtime_error("time cap");
   uint32_t k=row[0].first,fac=row[0].second;ops+=row.size()+piv[k].size();row=sub(row,piv[k],fac);
   if(ops>40000000000ULL)throw runtime_error("operation cap");
  }
  if(row.empty())return false;
  uint32_t k=row[0].first,inv=power(row[0].second,p-2);for(auto &x:row)x.second=(uint64_t)x.second*inv%p;
  stored+=row.size();if(stored>30000000ULL)throw runtime_error("pivot storage cap");piv[k]=move(row);rank++;return true;
 };
 // Begin with low-degree equations, then sample across the remaining degrees.
 size_t low=min< size_t >(r,coords.size());for(size_t ix=0;ix<low;ix++)insert(coords[ix]);
 vector<uint32_t> rest(coords.begin()+low,coords.end());mt19937 gen(1);shuffle(rest.begin(),rest.end(),gen);
 size_t pos=0,initial=min< size_t >(4ULL*r,rest.size());for(;pos<initial;pos++)insert(rest[pos]);
 vector<Row> basis;
 for(uint32_t round=0;;round++){
  if(expired())throw runtime_error("time cap");
  while(r-rank>128&&pos<rest.size()){size_t stop=min(pos+r,rest.size());for(;pos<stop;pos++)if(!used[rest[pos]])insert(rest[pos]);}
  basis.clear();vector<vector<uint32_t>> dense;
  for(uint32_t free=0;free<r;free++)if(piv[free].empty()){
   vector<uint32_t>x(r);x[free]=1;
   for(int k=r-1;k>=0;k--)if(!piv[k].empty()){
    uint64_t val=0;for(size_t j=1;j<piv[k].size();j++){auto a=piv[k][j];val+=(uint64_t)a.second*x[a.first];}val%=p;x[k]=val?p-val:0;
   }
   Row row;for(uint32_t k=0;k<r;k++)if(x[k])row.emplace_back(k,x[k]);basis.push_back(move(row));dense.push_back(move(x));
  }
  vector<uint32_t> violated;
  for(auto &x:dense){
   for(auto c:coords){if(used[c])continue;uint64_t val=0;for(auto a:eq[c])val+=(uint64_t)a.second*x[a.first];
    if(val%p){violated.push_back(c);break;}
   }
  }
  cerr<<"round="<<round<<" rank="<<rank<<" nullity="<<basis.size()<<" violated="<<violated.size()<<" stored="<<stored<<" ops="<<ops<<endl;
  if(violated.empty())break;
  uint32_t oldrank=rank;for(auto c:violated)if(!used[c])insert(c);
  if(oldrank==rank)throw runtime_error("adaptive refinement stalled");
 }
 ofstream out(argv[2]);out<<"[";for(size_t i=0;i<basis.size();i++){if(i)out<<",";out<<"{";for(size_t j=0;j<basis[i].size();j++){if(j)out<<",";out<<"\""<<basis[i][j].first<<"\":"<<basis[i][j].second;}out<<"}";}out<<"]\n";
 cerr<<"DONE rank="<<rank<<" nullity="<<basis.size()<<" stored="<<stored<<" ops="<<ops<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 }catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 2;}}

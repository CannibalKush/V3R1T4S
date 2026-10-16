// Exact-coordinate modular row elimination; dependencies are checked over Q in fast_sa.py.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using namespace std;
using E=pair<uint32_t,uint32_t>; using Row=vector<E>;
uint32_t p;
uint32_t power(uint32_t a,uint32_t e){uint64_t y=1;while(e){if(e&1)y=y*a%p;a=(uint64_t)a*a%p;e>>=1;}return y;}
Row sub(const Row&a,const Row&b,uint32_t f){Row c;c.reserve(a.size()+b.size());size_t i=0,j=0;while(i<a.size()||j<b.size()){uint32_t k,x;if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){c.push_back(a[i++]);continue;}if(i==a.size()||b[j].first<a[i].first){k=b[j].first;x=(p-(uint64_t)f*b[j++].second%p)%p;}else{k=a[i].first;x=(a[i++].second+p-(uint64_t)f*b[j++].second%p)%p;}if(x)c.emplace_back(k,x);}return c;}
uint32_t rd(ifstream&f){uint32_t x;f.read((char*)&x,4);if(!f)throw runtime_error("truncated input");return x;}
int main(int argc,char**argv){try{
 ifstream retired("work/retired_jobs.txt");string retired_pid;while(retired>>retired_pid)if(string(argv[1]).find("kernel_"+retired_pid+"_")!=string::npos)throw runtime_error("driver retired cooperatively");
 ifstream f(argv[1],ios::binary);uint32_t r=rd(f),dv=rd(f),dc=rd(f);p=rd(f);double cap=stod(argv[3]);auto start=chrono::steady_clock::now();
 vector<Row> us(r),vs(r);vector<uint32_t> deg(dc),order(r);uint64_t inputnnz=0;
 for(uint32_t t=0;t<r;t++){uint32_t nu=rd(f),nv=rd(f);for(uint32_t j=0;j<nu;j++){uint32_t a=rd(f),v=rd(f);us[t].emplace_back(a,v);}for(uint32_t j=0;j<nv;j++){uint32_t a=rd(f),v=rd(f);vs[t].emplace_back(a,v);}for(auto a:us[t])for(auto b:vs[t]){deg[a.first*dv+b.first]++;inputnnz++;}}
 vector<uint32_t> coord;for(uint32_t c=0;c<dc;c++)if(deg[c])coord.push_back(c);
 stable_sort(coord.begin(),coord.end(),[&](uint32_t a,uint32_t b){return deg[a]<deg[b];});
 vector<uint32_t> perm(dc);for(uint32_t i=0;i<coord.size();i++)perm[coord[i]]=i;
 iota(order.begin(),order.end(),0);stable_sort(order.begin(),order.end(),[&](uint32_t a,uint32_t b){return us[a].size()*vs[a].size()<us[b].size()*vs[b].size();});
 vector<Row> piv(coord.size()),comb(coord.size()),basis;uint64_t stored=0,ops=0;uint32_t rank=0;
 cerr<<"r="<<r<<" coordinates="<<coord.size()<<" inputnnz="<<inputnnz<<endl;
 for(uint32_t ix=0;ix<r;ix++){
  if(chrono::duration<double>(chrono::steady_clock::now()-start).count()>cap)throw runtime_error("time cap");
  uint32_t t=order[ix];Row row,c={{t,1}};row.reserve(us[t].size()*vs[t].size());for(auto a:us[t])for(auto b:vs[t]){uint32_t val=(uint64_t)a.second*b.second%p;if(val)row.emplace_back(perm[a.first*dv+b.first],val);}sort(row.begin(),row.end());
  while(!row.empty()&&!piv[row[0].first].empty()){uint32_t k=row[0].first,fac=row[0].second;ops+=row.size()+piv[k].size();row=sub(row,piv[k],fac);c=sub(c,comb[k],fac);if(ops>20000000000ULL)throw runtime_error("operation cap");}
  if(row.empty())basis.push_back(move(c));else{uint32_t k=row[0].first,inv=power(row[0].second,p-2);for(auto &x:row)x.second=(uint64_t)x.second*inv%p;for(auto &x:c)x.second=(uint64_t)x.second*inv%p;stored+=row.size()+c.size();if(stored>50000000)throw runtime_error("memory cap");piv[k]=move(row);comb[k]=move(c);rank++;}
  if(ix%1000==0)cerr<<"step="<<ix<<" rank="<<rank<<" nullity="<<basis.size()<<" stored="<<stored<<" ops="<<ops<<endl;
 }
 ofstream out(argv[2]);out<<"[";for(size_t i=0;i<basis.size();i++){if(i)out<<",";out<<"{";for(size_t j=0;j<basis[i].size();j++){if(j)out<<",";out<<"\""<<basis[i][j].first<<"\":"<<basis[i][j].second;}out<<"}";}out<<"]\n";
 cerr<<"DONE rank="<<rank<<" nullity="<<basis.size()<<" stored="<<stored<<" ops="<<ops<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 }catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 2;} }

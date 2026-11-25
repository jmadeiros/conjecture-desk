// Coefficients A_k(n) of F^k, F = f6/(f1 f2 f3) (k-tuples of partitions with designated summands), modulo M=3^E.
// Usage: pdk k N E  ; prints min 3-adic valuation (capped at E) of A_k(n) along the progressions of
// arXiv:2611.05623v1 Conjectures 6.3 / 6.4 for n<=N, and the first index where the minimum is attained.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static long N; static uint32_t M;
static void mulf(uint32_t*a,long d){ // a *= f_d
  uint32_t*t=malloc(sizeof(uint32_t)*(N+1)); memcpy(t,a,sizeof(uint32_t)*(N+1));
  for(long k=1;;k++){ long e1=d*(k*(3*k-1)/2), e2=d*(k*(3*k+1)/2); if(e1>N)break;
    if(k&1){ for(long i=e1;i<=N;i++){ a[i]+=M-t[i-e1]; if(a[i]>=M)a[i]-=M; } if(e2<=N) for(long i=e2;i<=N;i++){ a[i]+=M-t[i-e2]; if(a[i]>=M)a[i]-=M; } }
    else   { for(long i=e1;i<=N;i++){ a[i]+=t[i-e1]; if(a[i]>=M)a[i]-=M; } if(e2<=N) for(long i=e2;i<=N;i++){ a[i]+=t[i-e2]; if(a[i]>=M)a[i]-=M; } } }
  free(t);
}
static void divf(uint32_t*a,long d){ // a /= f_d : b(n) = a(n) - sum_{k>=1} (-1)^k [ b(n-d p1) + b(n-d p2) ]
  long np=0; long*pe=malloc(sizeof(long)*100000); int*ps=malloc(sizeof(int)*100000);
  for(long k=1;;k++){ long e1=d*(k*(3*k-1)/2), e2=d*(k*(3*k+1)/2); if(e1>N)break; pe[np]=e1;ps[np]=(k&1);np++; if(e2<=N){pe[np]=e2;ps[np]=(k&1);np++;} }
  for(long n=0;n<=N;n++){
    uint64_t pos=a[n], neg=0;
    for(long j=0;j<np&&pe[j]<=n;j++){ if(ps[j]) pos+=a[n-pe[j]]; else neg+=a[n-pe[j]]; }
    a[n]=(uint32_t)((pos + (uint64_t)M*((neg/M)+1) - neg)%M);
  }
  free(pe);free(ps);
}
static int v3(uint32_t x,int E){ if(x==0) return E; int v=0; while(x%3==0){x/=3;v++;} return v; }
int main(int argc,char**argv){
  int k=atoi(argv[1]); N=atol(argv[2]); int E=atoi(argv[3]); M=1; for(int i=0;i<E;i++) M*=3;
  uint32_t*a=calloc(N+1,sizeof(uint32_t)); a[0]=1;
  for(int i=0;i<k;i++){ mulf(a,6); divf(a,1); divf(a,2); divf(a,3); }
  printf("k=%d N=%ld mod 3^%d ; first coefficients:",k,N,E); for(int n=0;n<8;n++) printf(" %u",a[n]); printf("\n");
  int progs[][2]={{12,10},{12,7},{12,11},{6,5},{18,15},{3,2},{3,1}};
  for(int p=0;p<7;p++){
    int m=progs[p][0], r=progs[p][1]; int mn=E; long arg=-1; long cnt=0; long hist[16]={0};
    for(long n=r;n<=N;n+=m){ int v=v3(a[n],E); hist[v]++; cnt++; if(v<mn){mn=v;arg=n;} }
    printf("  progression %dn+%d: terms=%ld min v3=%d%s (first at n=%ld) ; histogram v3=0..%d:",m,r,cnt,mn,(mn==E?"+":""),arg,E);
    for(int v=0;v<=E;v++) printf(" %ld",hist[v]); printf("\n");
  }
  if(argc>4){ FILE*f=fopen(argv[4],"wb"); fwrite(a,sizeof(uint32_t),N+1,f); fclose(f); }
  return 0;
}

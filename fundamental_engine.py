import pandas as pd
def fundamental_score(r):
 s=50
 for k,p in [("revenue_yoy",10),("ebitda_yoy",12),("net_income_yoy",14),("fcf_yoy",8)]:
  if pd.notna(r.get(k)): s+=p if r[k]>0 else -p
 if pd.notna(r.get("net_debt")) and pd.notna(r.get("ebitda")) and r["ebitda"]>0:
  ratio=r["net_debt"]/r["ebitda"]; s+=8 if ratio<1.5 else (-8 if ratio>4 else 0)
 return float(max(0,min(100,s)))
def valuation_score(r):
 s=50
 for k,good,bad,p in [("pe",10,25,12),("pb",2,5,8),("ev_ebitda",8,18,12)]:
  v=r.get(k)
  if pd.notna(v): s+=p if v<good else (-p if v>bad else 0)
 if pd.notna(r.get("dividend_yield")): s+=min(10,max(0,r["dividend_yield"]*1.2))
 return float(max(0,min(100,s)))

import pandas as pd
from analysis_engine import indicators,technical_score,momentum_score,trend_score,signals
from fundamental_engine import fundamental_score,valuation_score
from news_engine import news_score
def scan(p):
 prices=p.prices(); funds=p.fundamentals(); news=p.news(); rows=[]
 if prices.empty: return pd.DataFrame()
 for ticker,g in prices.groupby("ticker"):
  d=indicators(g); r=d.iloc[-1].to_dict()
  ff=funds[funds.ticker==ticker]; f=ff.iloc[-1].to_dict() if not ff.empty else {}
  ts,ms,tr=technical_score(r),momentum_score(r),trend_score(r)
  fs=fundamental_score(f) if f else 50; vs=valuation_score(f) if f else 50
  ns,nc,head=news_score(news,ticker)
  risk=min(20,float(r.get("atr14",0)/r["close"]*200)) if pd.notna(r.get("atr14")) and r["close"] else 0
  if f and pd.notna(f.get("net_debt")) and pd.notna(f.get("ebitda")) and f["ebitda"]>0 and f["net_debt"]/f["ebitda"]>4: risk+=15
  score=max(0,min(100,.16*ts+.13*ms+.11*tr+.15*fs+.12*vs+.09*ns+.18*50-.06*risk))
  completeness=sum(pd.notna(v) for v in [r.get("sma200"),f.get("revenue_yoy"),f.get("pe")])/3
  confidence=min(100,100*(.55*completeness+.30*nc+.15))
  rows.append({"ticker":ticker,"price":r.get("close"),"score":round(score,1),"confidence":round(confidence,1),"technical":round(ts,1),"momentum":round(ms,1),"trend":round(tr,1),"fundamental":round(fs,1),"valuation":round(vs,1),"news":round(ns,1),"risk_penalty":round(risk,1),"signals":", ".join(signals(r)),"headlines":" | ".join(head)})
 return pd.DataFrame(rows).sort_values("score",ascending=False)

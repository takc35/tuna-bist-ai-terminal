import pandas as pd
from score_config import SOURCE_RELIABILITY
def news_score(news,ticker):
 if news.empty: return 50.0,0.0,[]
 d=news[news.ticker.astype(str).str.upper()==str(ticker).upper()].copy()
 if d.empty: return 50.0,0.0,[]
 d["rel"]=d.source.map(SOURCE_RELIABILITY).fillna(.5)
 d["impact"]=pd.to_numeric(d.sentiment,errors="coerce").fillna(0)*pd.to_numeric(d.importance,errors="coerce").fillna(1)*d.rel
 d=d.tail(30); score=max(0,min(100,50+d.impact.sum()*5))
 return float(score),min(1,.2+len(d)/20),d.sort_values("importance",ascending=False).title.head(3).tolist()

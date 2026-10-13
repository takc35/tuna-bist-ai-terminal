import numpy as np
import pandas as pd
def clamp(x): return float(max(0,min(100,x)))
def indicators(df):
 d=df.copy(); d["date"]=pd.to_datetime(d["date"]); d=d.sort_values("date")
 for n in [5,10,20,25,50,100,200]: d[f"sma{n}"]=d.close.rolling(n).mean()
 d["ema12"]=d.close.ewm(span=12,adjust=False).mean(); d["ema26"]=d.close.ewm(span=26,adjust=False).mean()
 delta=d.close.diff(); gain=delta.clip(lower=0).rolling(14).mean(); loss=(-delta.clip(upper=0)).rolling(14).mean()
 d["rsi14"]=100-100/(1+gain/loss.replace(0,np.nan)); d["macd"]=d.ema12-d.ema26; d["macd_signal"]=d.macd.ewm(span=9,adjust=False).mean()
 tr=pd.concat([d.high-d.low,(d.high-d.close.shift()).abs(),(d.low-d.close.shift()).abs()],axis=1).max(axis=1)
 d["atr14"]=tr.rolling(14).mean(); d["vol_ratio"]=d.volume/d.volume.rolling(20).mean()
 d["roc20"]=d.close.pct_change(20)*100; d["roc60"]=d.close.pct_change(60)*100
 d["high20_prev"]=d.high.rolling(20).max().shift(1); d["high252"]=d.high.rolling(252).max()
 return d
def technical_score(r):
 s=50
 if pd.notna(r.get("rsi14")): s+=10 if 50<=r["rsi14"]<=68 else (-8 if r["rsi14"]>75 else 0)
 if pd.notna(r.get("macd")) and pd.notna(r.get("macd_signal")): s+=10 if r["macd"]>r["macd_signal"] else -8
 for ma,p in [("sma25",6),("sma50",8),("sma200",10)]:
  if pd.notna(r.get(ma)): s+=p if r["close"]>r[ma] else -p
 if pd.notna(r.get("vol_ratio")) and r["vol_ratio"]>=1.5: s+=6
 return clamp(s)
def momentum_score(r):
 s=50
 for k,w in [("roc20",.9),("roc60",.5)]:
  if pd.notna(r.get(k)): s+=float(np.clip(r[k]*w,-20,20))
 return clamp(s)
def trend_score(r):
 s=50
 for a,b in [("sma25","sma50"),("sma50","sma200")]:
  if pd.notna(r.get(a)) and pd.notna(r.get(b)): s+=12 if r[a]>r[b] else -12
 if pd.notna(r.get("sma200")): s+=12 if r["close"]>r["sma200"] else -12
 return clamp(s)
def signals(r):
 x=[]
 if pd.notna(r.get("high20_prev")) and r["close"]>r["high20_prev"]: x.append("20D_BREAKOUT")
 if pd.notna(r.get("sma25")) and pd.notna(r.get("sma50")): x.append("25_ABOVE_50" if r["sma25"]>r["sma50"] else "25_BELOW_50")
 if pd.notna(r.get("sma50")) and pd.notna(r.get("sma200")) and r["sma50"]>r["sma200"]: x.append("50_ABOVE_200")
 if pd.notna(r.get("high252")) and r["close"]>=.98*r["high252"]: x.append("52W_HIGH_ZONE")
 return x

import streamlit as st
import plotly.express as px
from data_provider import CSVProvider
from scanner import scan
from analysis_engine import indicators
st.set_page_config(page_title="TUNA BIST AI TERMINAL V0.3",layout="wide")
st.title("TUNA BIST AI TERMINAL")
st.caption("V0.3 | Teknik • Temel • Haber/KAP • Risk • Hisse tarayıcı")
st.warning("Demo CSV verileri sentetiktir; gerçek piyasa verisi değildir.")
p=CSVProvider("data"); prices=p.prices(); funds=p.fundamentals(); news=p.news()
if prices.empty: st.error("data/prices.csv bulunamadı."); st.stop()
result=scan(p)
a,b,c,d=st.tabs(["BIST Tarayıcı","Hisse Detay","Haber/KAP","Veri Kalitesi"])
with a:
 x,y,z=st.columns(3); x.metric("Hisse",len(result)); y.metric("Ort. skor",f"{result.score.mean():.1f}/100"); z.metric("20g kırılım",int(result.signals.fillna("").str.contains("20D_BREAKOUT").sum()))
 st.dataframe(result,use_container_width=True,hide_index=True)
 st.plotly_chart(px.bar(result.head(15),x="ticker",y="score",hover_data=["confidence","signals"]),use_container_width=True)
with b:
 ticker=st.selectbox("Hisse",sorted(prices.ticker.unique())); d=indicators(prices[prices.ticker==ticker]); r=d.iloc[-1]
 st.metric("Son CSV kapanışı",f"{r.close:.2f}")
 st.line_chart(d.tail(250).set_index("date")[["close","sma25","sma50","sma200"]])
 st.dataframe(result[result.ticker==ticker],use_container_width=True,hide_index=True)
with c:
 st.dataframe(news.sort_values("timestamp",ascending=False),use_container_width=True,hide_index=True) if not news.empty else st.info("Haber verisi yok.")
with d:
 st.write({"fiyat_satırı":len(prices),"finansal_satırı":len(funds),"haber_satırı":len(news),"hisse_sayısı":prices.ticker.nunique(),"ilk_tarih":str(prices.date.min()),"son_tarih":str(prices.date.max())})
 st.info("Canlı kullanımda veri sağlayıcı, gecikme ve kaynak güvenilirliği denetlenmelidir.")

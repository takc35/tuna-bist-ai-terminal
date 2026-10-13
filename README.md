# TUNA BIST AI TERMINAL V0.3
CSV tabanlı BIST analiz prototipi. Örnek veriler sentetiktir, canlı piyasa verisi değildir.

## Çalıştırma
pip install -r requirements.txt
streamlit run app.py

## Veri dosyaları
data/prices.csv: date,ticker,open,high,low,close,volume
data/fundamentals.csv: ticker,sector,revenue,ebitda,net_income,net_debt,equity,assets,revenue_yoy,ebitda_yoy,net_income_yoy,fcf_yoy,pe,pb,ev_ebitda,dividend_yield
data/news.csv: timestamp,source,ticker,title,category,sentiment,importance

Canlı kullanım için doğrulanmış CSV veya lisanslı veri sağlayıcısı entegrasyonu gerekir. Araç yatırım tavsiyesi ya da emir üretmez.

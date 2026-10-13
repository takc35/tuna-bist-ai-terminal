from pathlib import Path
import pandas as pd
class CSVProvider:
 def __init__(self,data_dir="data"): self.data_dir=Path(data_dir)
 def read(self,name,dates=None):
  p=self.data_dir/name
  return pd.read_csv(p,parse_dates=dates or []) if p.exists() else pd.DataFrame()
 def prices(self): return self.read("prices.csv",["date"])
 def fundamentals(self): return self.read("fundamentals.csv")
 def news(self): return self.read("news.csv",["timestamp"])

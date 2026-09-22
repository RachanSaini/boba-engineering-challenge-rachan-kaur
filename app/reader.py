import pandas as pd

df = pd.read_excel("app/sheet/trades.xlsx", sheet_name="new_trade_data")

print(df)

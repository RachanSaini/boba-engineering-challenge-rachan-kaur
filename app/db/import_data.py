import pandas as pd


def import_data(connection):
    print("Reading Excel file...")

    # Excel file location
    file_path = "app/db/sheet/trades.xlsx"

    # Read Excel sheet
    df = pd.read_excel(
        file_path,
        sheet_name="new_trade_data"
    )

    print(f"Read {len(df)} rows from Excel")    

    df = df.rename(columns={
        "Trade ID": "trade_id",
        "Realised (R)/Unrealised(UR)": "trade_status",
        "Broker": "broker",
        "Date": "trade_date",
        "Type": "trade_type",
        "Commodity": "commodity",
        "Contract": "contract",
        "Size": "size",
        "Entry Price": "entry_price",
        "Order ID": "order_id",
        "Trader": "trader",
        "TraderA": "trader_a",
        "TraderB": "trader_b",
        "TraderC": "trader_c",
        "TraderD": "trader_d",
        "Trader E": "trader_e",
        "Total Exchange Fees (basis fixed FX rates on date) (USD)": "total_exchange_fees_usd",
        "Total Brokerage Fees (USD)": "total_brokerage_fees_usd",
        "Total Carry Broker Fees (USD)": "total_carry_broker_fees_usd",
        "Total NFA Fees (USD)": "total_nfa_fees_usd",
        "Total Commission (USD conv)": "total_commission_usd",
        "Average Stop": "average_stop"
    })

    print("\nColumns after normalization:")
    print(df.columns.tolist())


    # Insert data into PostgreSQL
    df.to_sql(
        "tradesdb",
        connection,
        if_exists="append",
        index=False
    )

    print(f"Successfully imported {len(df)} rows into PostgreSQL")

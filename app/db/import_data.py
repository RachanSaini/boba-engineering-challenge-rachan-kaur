import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = [
    "trade_id",
    "commodity",
    "contract",
    "trader"
]

def import_data(connection):
    print("Reading Excel file...")

    # Excel file location
    file_path = "app/db/sheet/trades.xlsx"

# Read Data
    # Read Excel sheet
    df = pd.read_excel(
        file_path,
        sheet_name="new_trade_data"
    )

    print(f"Read {len(df)} rows from Excel")

    # Add source filename
    df["source_file"] = Path(file_path).name

# Validate data
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

    print("\nColumns normalization done")

    print("\nValidating data...")


    # Checking required columns exist
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )
    
    # remove missing rows (future)

    # Clean whitespaces
    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].apply(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )
    
    # Check required fields are not empty
    invalid_required = df[
        df[REQUIRED_COLUMNS].isnull().any(axis=1)
    ]

    print(
        f"Rows missing required values: "
        f"{len(invalid_required)}"
    )

    # Validate trade_id
    invalid_trade_id = df[
        pd.to_numeric(df["trade_id"], errors="coerce").isnull()
    ]

    print(
        f"Rows with invalid trade_id: "
        f"{len(invalid_trade_id)}"
    )

    # Validate size
    invalid_size = df[
        pd.to_numeric(df["size"], errors="coerce").isnull()
    ]

    print(
        f"Rows with invalid size: "
        f"{len(invalid_size)}"
    )

    # Check duplicate trade IDs
    duplicate_trade_ids = df[
        df["trade_id"].duplicated(keep=False)
    ]

    print(
        f"Rows with duplicate trade IDs: "
        f"{len(duplicate_trade_ids)}"
    )

# Insert valid data
    df.to_sql(
        "tradesdb",
        connection,
        if_exists="append",
        index=False
    )

    print(
        f"Successfully imported "
        f"{len(df)} rows"
    )

    print(f"Successfully imported {len(df)} rows into PostgreSQL")

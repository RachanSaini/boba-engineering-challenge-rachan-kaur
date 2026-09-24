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

    # Show the columns we received
    print("Columns:")
    print(df.columns.tolist())

    # Insert data into PostgreSQL
    df.to_sql(
        "traderdb",
        connection,
        if_exists="append",
        index=False
    )

    print(f"Successfully imported {len(df)} rows into PostgreSQL")

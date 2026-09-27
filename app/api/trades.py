from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.config import connect_to_database
from typing import Optional,Literal

router = APIRouter()

def get_connection():
    return connect_to_database()

# Search Trades via filtering
@router.get("/trades")
def get_tradesbyfilter(
    commodity: Optional[str] = None,
    contract: Optional[str] = None,
    trader: Optional[str] = None,
    trade: Optional[Literal["R", "UR"]] = None
):
    try:
        connection = get_connection()
        query = """
            SELECT * FROM trades WHERE 1 = 1
        """

        parameters = {}
        if commodity is not None:
            query += " AND commodity = :commodity"
            parameters["commodity"] = commodity
        if contract is not None:
            query += " AND contract = :contract"
            parameters["contract"] = contract
        if trader is not None:
            query += " AND trader = :trader"
            parameters["trader"] = trader
        if trade is not None:
            query += " AND trade_status = :trade"
            parameters["trade"] = trade

        with connection.connect() as db:
            result = db.execute(
                text(query),
                parameters
            )
        rows = result.mappings().all()

        return rows
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve trades: {str(e)}"
        )

# Get historical trade summary
@router.get("/trades/history")
def get_trade_history():
    try:
        connection = get_connection()
        query = text("""
            SELECT
                commodity,
                contract,
                COUNT(*) AS trade_count,
                SUM(size) AS net_quantity,
                SUM(ABS(size)) AS total_traded_quantity,
                AVG(entry_price) AS average_entry_price,
                MIN(trade_date) AS first_trade_date,
                MAX(trade_date) AS last_trade_date
            FROM trades
            GROUP BY
                commodity,
                contract
            ORDER BY
                commodity,
                contract
        """)

        with connection.connect() as db:
            result = db.execute(query)
            history = result.mappings().all()

        return history

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve trade history: {str(e)}"
        ) 

# Retrieve a Trade by its ID
@router.get("/trades/{trade_id}")
def get_trades(trade_id: int):
    try:
        connection = get_connection()
        query = text("""
            SELECT * FROM trades WHERE trade_id = :trade_id
        """)

        with connection.connect() as db:
            result = db.execute(
                query,
                {"trade_id": trade_id}
            )
            trade = result.mappings().first()
        if trade is None:
            raise HTTPException(
                status_code=404,
                detail=f"Trade {trade_id} not found"
            )

        return trade
    
    except Exception as e:
        print(f"Error: {e}")

        raise HTTPException(
            status_code=404,
            detail=f"Trade not found: {str(e)}"
        )
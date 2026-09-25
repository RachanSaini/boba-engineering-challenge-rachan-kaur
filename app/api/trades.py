from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.config import connect_to_database
from typing import Optional

router = APIRouter()

connection = connect_to_database()

# Retrieve a Trade by its ID
@router.get("/trades/{trade_id}")
def get_trades(trade_id: int):
    try:
        query = text("""
            SELECT * FROM tradesdb WHERE trade_id = :trade_id
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve trade: {str(e)}"
        )

# Search Trades via filtering
@router.get("/trades")
def get_tradesbyfilter(
    commodity: Optional[str] = None,
    contract: Optional[str] = None,
    trader: Optional[str] = None
):
    try:
        query = """
            SELECT * FROM tradesdb WHERE 1 = 1
        """

        parameters = {}
        if commodity is not None:
            query += " AND commodity = :commodity"
            parameters["commodity"] = commodity
        if contract is not None:
            query += " AND contract = :contract"
            parameters["contract"] = contract
        if commodity is not None:
            query += " AND trader = :trader"
            parameters["trader"] = trader

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


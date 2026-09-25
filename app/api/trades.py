from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.config import connect_to_database

router = APIRouter()

connection = connect_to_database()

@router.get("/trades")
def get_trades():
    with connection.connect() as db:
        result = db.execute(
            text("SELECT * FROM traderdb")
        )

        rows = result.mappings().all()
    
    return rows
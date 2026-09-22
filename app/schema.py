from datetime import date
from decimal import Decimal
from typing import Literal

class TradeBase(BaseModel):
    trade_id: str
    realised: Literal["R", "UR"]
    broker: str
    date: date
    trade_type: str
    commodity: str
    contract: str
    size: Decimal
    entry_price: Decimal
    order_id: str
    trader: str

    trader_a: Decimal
    trader_b: Decimal
    trader_c: Decimal
    trader_d: Decimal

    total_exchange_fees: Decimal
    total_brokerage_fees: Decimal
    total_carry_broker_fees: Decimal
    total_nfa_fees_usd: Decimal
    total_commission: Decimal
    average_stop: Decimal
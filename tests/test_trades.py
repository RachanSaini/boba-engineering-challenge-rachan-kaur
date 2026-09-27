from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from app.main import app

client = TestClient(app)

# mock test data
MOCK_TRADES = [
{
"trade_id": 10000,
"commodity": "Gold",
"contract": "Dec-26",
"size": 10,
"trader": "Trader A",
"source_file": "trades.xlsx"
},
{
"trade_id": 10001,
"commodity": "Gold",
"contract": "Dec-26",
"size": -5,
"trader": "Trader A",
"source_file": "trades1.xlsx"
},
{
"trade_id": 10002,
"commodity": "Silver",
"contract": "Jan-27",
"size": 20,
"trader": "Trader B",
"source_file": "trades.xlsx"
}
]

def create_mock_connection(mock_data):
    mock_connection = MagicMock()
    mock_result = MagicMock()

    mock_result.mappings.return_value.all.return_value = mock_data
    mock_result.mappings.return_value.first.return_value = (
        mock_data[0] if mock_data else None
    )

    mock_connection.connect.return_value.__enter__.return_value.execute.return_value = (
        mock_result
    )

    return mock_connection

# Testing get trades
def test_get_trades():
    mock_connection = create_mock_connection(MOCK_TRADES)

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/trades")

    assert response.status_code == 200

    trades = response.json()

    assert isinstance(trades, list)
    assert len(trades) == 3

# Testing get trades by ID
def test_get_trade():
    mock_connection = create_mock_connection([MOCK_TRADES[0]])
    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/trades/10000")

    assert response.status_code == 200

    trade = response.json()

    assert trade["trade_id"] == 10000
    assert trade["commodity"] == "Gold"
    assert trade["contract"] == "Dec-26"
    assert trade["size"] == 10
    assert trade["trader"] == "Trader A"
    assert trade["source_file"] == "trades.xlsx"

# Trade not found by ID
def test_get_trade_not_found():
    mock_connection = create_mock_connection([])

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/trades/999999")

    assert response.status_code == 404

# Testing get trades filter by commodity
def test_filter_by_commodity():
    mock_data = [
    MOCK_TRADES[0],
    MOCK_TRADES[1]
    ]

    mock_connection = create_mock_connection(mock_data)

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get(
            "/trades",
            params={"commodity": "Gold"}
        )

    assert response.status_code == 200

    trades = response.json()

    for trade in trades:
        assert trade["commodity"] == "Gold"

# Testing get trades filter by commodity
def test_filter_by_contract():
    mock_data = [
    MOCK_TRADES[0],
    MOCK_TRADES[1]
    ]

    mock_connection = create_mock_connection(mock_data)

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get(
            "/trades",
            params={"contract": "Dec-26"}
        )

    assert response.status_code == 200

    trades = response.json()

    for trade in trades:
        assert trade["contract"] == "Dec-26"

# Testing get trades filter by trader
def test_filter_by_trader():
    mock_data = [
    MOCK_TRADES[0],
    MOCK_TRADES[1]
    ]

    mock_connection = create_mock_connection(mock_data)

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get(
            "/trades",
            params={"trader": "Trader A"}
        )

    assert response.status_code == 200

    trades = response.json()

    for trade in trades:
        assert trade["trader"] == "Trader A"


def test_multiple_filters():
    mock_data = [
    MOCK_TRADES[0],
    MOCK_TRADES[1]
    ]

    mock_connection = create_mock_connection(mock_data)

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get(
            "/trades",
            params={
                "commodity": "Gold",
                "contract": "Dec-26",
                "trader": "Trader A"
            }
        )

    assert response.status_code == 200

    trades = response.json()

    for trade in trades:
        assert trade["commodity"] == "Gold"
        assert trade["contract"] == "Dec-26"
        assert trade["trader"] == "Trader A"

# Testing Get trades history
def test_get_trade_history():
    mock_connection = create_mock_connection([
    {
    "commodity": "Gold",
    "contract": "Dec-26",
    "trade_count": 2,
    "net_quantity": 5
    },
    {
    "commodity": "Silver",
    "contract": "Jan-27",
    "trade_count": 1,
    "net_quantity": 20
    }
    ])

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/trades/history")

    assert response.status_code == 200

    history = response.json()

    assert isinstance(history, list)
    assert len(history) == 2

    for item in history:
        assert "commodity" in item
        assert "contract" in item
        assert "trade_count" in item
        assert "net_quantity" in item

# Testing positions endpoint
def test_get_positions():
    mock_connection = create_mock_connection([
        {
            "commodity": "Gold",
            "contract": "Dec-26",
            "net_quantity": 5
        },
        {
            "commodity": "Silver",
            "contract": "Jan-27",
            "net_quantity": 20
        }
    ])

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/positions")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["net_quantity"] == 5


def test_filter_positions_by_commodity():
    mock_connection = create_mock_connection([
        {
            "commodity": "Gold",
            "contract": "Dec-26",
            "net_quantity": 5
        }
    ])

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/positions?commodity=Gold")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["commodity"] == "Gold"


def test_filter_positions_by_contract():
    mock_connection = create_mock_connection([
        {
            "commodity": "Gold",
            "contract": "Dec-26",
            "net_quantity": 5
        }
    ])

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get("/positions?contract=Dec-26")

    assert response.status_code == 200
    assert all(
        position["contract"] == "Dec-26"
        for position in response.json()
    )


def test_filter_positions_by_both():
    mock_connection = create_mock_connection([

        {
            "commodity": "Gold",
            "contract": "Dec-26",
            "net_quantity": 5
        }
    ])

    with patch(
        "app.api.trades.get_connection",
        return_value=mock_connection
    ):
        response = client.get(
            "/positions?commodity=Gold&contract=Dec-26"
        )

    assert response.status_code == 200
    assert response.json() == [
        {
            "commodity": "Gold",
            "contract": "Dec-26",
            "net_quantity": 5
        }
    ]
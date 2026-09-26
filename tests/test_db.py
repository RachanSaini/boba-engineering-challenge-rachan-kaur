from sqlalchemy import inspect, text

from app.db.config import connect_to_database


def get_test_connection():
    connection = connect_to_database()

    assert connection is not None, "Could not connect to PostgreSQL"

    return connection


def test_database_connection():
    connection = get_test_connection()

    with connection.connect() as db:
        result = db.execute(text("SELECT 1"))
        value = result.scalar()

    assert value == 1


def test_trades_table_exists():
    connection = get_test_connection()

    inspector = inspect(connection)

    tables = inspector.get_table_names()

    assert "trades" in tables


def test_trades_table_has_data():
    connection = get_test_connection()

    with connection.connect() as db:
        result = db.execute(
            text("SELECT COUNT(*) FROM trades")
        )

        count = result.scalar()

    assert count > 0


def test_trades_table_columns():
    connection = get_test_connection()

    inspector = inspect(connection)

    columns = inspector.get_columns("trades")

    column_names = [
        column["name"]
        for column in columns
    ]

    expected_columns = [
        "trade_id",
        "commodity",
        "contract",
        "size",
        "trader",
        "source_file"
    ]

    for column in expected_columns:
        assert column in column_names


def test_trade_id_has_data():
    connection = get_test_connection()

    with connection.connect() as db:
        result = db.execute(
            text("""
                SELECT COUNT(*)
                FROM trades
                WHERE trade_id IS NOT NULL
            """)
        )

        count = result.scalar()

    assert count > 0


def test_source_file_has_data():
    connection = get_test_connection()

    with connection.connect() as db:
        result = db.execute(
            text("""
                SELECT COUNT(*)
                FROM trades
                WHERE source_file IS NOT NULL
            """)
        )

        count = result.scalar()

    assert count > 0


def test_trade_size_has_data():
    connection = get_test_connection()

    with connection.connect() as db:
        result = db.execute(
            text("""
                SELECT COUNT(*)
                FROM trades
                WHERE size IS NOT NULL
            """)
        )

        count = result.scalar()

    assert count > 0
from sqlalchemy import create_engine, text

DB_USER = "rachan"
DB_PASSWORD = "saini"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "traderdb"

connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)

with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    print(result.fetchone())
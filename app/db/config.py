from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_database():
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    print("Connecting to PostgreSQL...")

    connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    try:
        engine = create_engine(connection_string)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print(result.fetchone())
            print("Connected to PostgreSQL")

        return engine
    except Exception as e:
        print("PostgreSQL connection failed")
        print(e)
        return None
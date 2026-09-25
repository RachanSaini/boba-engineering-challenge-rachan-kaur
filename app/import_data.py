from app.db.config import connect_to_database
from app.db.import_data import import_data


def main():
    print("Application started")

    print("Database connection started")
    connection = connect_to_database()

    print("Importing data from sheet to database")
    import_data(connection)

    print("Import completed")


if __name__ == "__main__":
    main()
# Trade API

A FastAPI application for importing trade data from Excel into PostgreSQL and exposing the data through REST API endpoints.

The application supports:

* Importing trade data from the supplied Excel file
* Data validation and normalization during import
* Retrieving individual trades
* Filtering trades by commodity, contract, trader and Realeased or Unrealeased trades
* Providing historical trade summaries
* API tests using mock database data
* Database integration tests against PostgreSQL

---

## Project Structure

```text
boba-engineering-challenge-rachan-kaur/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── import_data.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── trades.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── config.py
│       ├── import_data.py
│       └── sheet/
│           └── trades.xlsx
│
├── tests/
│   ├── __init__.py
│   ├── test_trades.py
│   └── test_db.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# 1. Prerequisites

The project requires:

* Python 3.9+
* PostgreSQL
* pip
* Git

Check your Python version:

```bash
python --version
```

Check PostgreSQL:

```bash
psql --version
```

---

# 2. Clone the Project

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd boba-engineering-challenge-rachan-kaur
```

---

# 3. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

# 4. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The main dependencies include:

* FastAPI - REST API framework
* Uvicorn - ASGI: Async server gateway interface
* Pandas - Excel/data processing
* OpenPyXL - Excel file support
* SQLAlchemy - database connectivity
* psycopg2-binary - PostgreSQL driver
* python-dotenv - environment variable management
* pytest - testing
* httpx - FastAPI test client support

---

# 5. Configure PostgreSQL

Create a PostgreSQL database.

For example:

```bash
createdb -U postgres tradesdb
```

Exit PostgreSQL:

```sql
\q
```

---

# 6. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```text
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tradesdb
```

The `.env` file should **not** be committed to source control.

Add it to `.gitignore`:

```text
.env
.venv/
__pycache__/
.pytest_cache/
/app/db/sheet
```

---

# 7. Import the Supplied Excel File

The supplied Excel file is expected at:

```text
app/db/sheet/trades.xlsx
```

The importer reads the `new_trade_data` worksheet.

The importer:

1. Reads the Excel file using Pandas
2. Normalizes the column names
3. Adds the source filename to each record
4. Removes leading/trailing whitespace from string values
5. Checks that required columns exist
6. Checks required fields
7. Validates `trade_id`
8. Validates `size`
9. Checks for duplicate trade IDs
10. Inserts the data into the PostgreSQL `trades` table

Run the import from the project root:

```bash
python -m app.import_data
```

The expected output includes messages showing the database connection, number of Excel rows read, validation results, and number of rows imported.

---

# 8. Verify the Imported Data

Connect to PostgreSQL:

```bash
psql -U postgres -d tradesdb
```

Check the tables:

```sql
\dt
```

The `trades` table should be present.

Check the number of records:

```sql
SELECT COUNT(*) FROM trades;
```

---

# 9. Start the API

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```
or

```text
http://localhost:8000
```
---

# 10. API Endpoints

I used Postman for testing endpoints or simply curl commands to test endpoints.

## Get all trades

```http
GET /trades
```

Example:

```text
http://localhost:8000/trades
```

---

## Filter trades by commodity

```http
GET /trades?commodity={commodity}
```

---

## Filter trades by contract

```http
GET /trades?contract={contract}
```

---

## Filter trades by trader

```http
GET /trades?trader={trader}
```

---

## Filter trades by Released or Unreleased trades

For released reades
```http
GET /trades?trade=R
```

For unreleased reades
```http
GET /trades?trade=UR
```

## Multiple filters can be combined:

```http
GET /trades?commodity={commodity}&contract={contract}&trader=Trader{trader}
```

---

## Get a trade by ID

```http
GET /trades/{trade_id}
```

Example:

```http
GET /trades/10000
```

The response contains the key trade information including:

* `trade_id`
* `commodity`
* `contract`
* `size`
* `trader`
* `source_file`

If the trade does not exist, the API returns HTTP error.

---

## Get trade history

```http
GET /trades/history
```

The historical summary groups trades by commodity and contract.

It provides information such as:

* Number of trades
* Net quantity
* Total traded quantity
* Average entry price
* First trade date
* Last trade date

---

# 11. Running the Tests

Run all tests:

```bash
python -m pytest -v
```

There are two types of tests.

## API Tests

`tests/test_trades.py`

These tests use mocked database responses.

Run only the API tests:

```bash
python -m pytest tests/test_trades.py -v
```

---

## Database Integration Tests

`tests/test_db.py`

These tests connect to the configured PostgreSQL database and verify things such as:

* PostgreSQL connection
* `trades` table existence
* Imported data availability
* Expected database columns

Run only the database tests:

```bash
python -m pytest tests/test_db.py -v
```

These tests require PostgreSQL to be running and the Excel data to have been imported.

---

# 12. Data Validation and Assumptions

The supplied data may contain incomplete or inconsistent records, so the import process performs basic validation before loading data.

The following fields are treated as required:

```text
trade_id
commodity
contract
trader
```

The following numeric fields are validated:

```text
trade_id
size
```

String fields are stripped of leading and trailing whitespace.

### Trade IDs

`trade_id` is expected to identify a trade uniquely.

Duplicate trade IDs are detected during import and reported.

---

# 13. Technical Decisions

### FastAPI

FastAPI was selected to provide a lightweight REST API with automatic OpenAPI documentation and straightforward request handling.

### PostgreSQL

PostgreSQL is used as the persistent database because the application involves structured trade records and aggregation queries.

### SQLAlchemy

SQLAlchemy is used for database connectivity and parameterized SQL execution.

### Pandas

Pandas is used to read and transform the supplied Excel data before loading it into PostgreSQL.

### Separate Import Script

The Excel import is separated from the API startup.

The import is run explicitly:

```bash
python -m app.import_data
```

This prevents the Excel file from being imported every time the API starts.

### Mocked API Tests

API tests use mock database responses so that they test API behavior independently of the current development database.

### Database Integration Tests

A separate test file checks the actual PostgreSQL setup and imported data.

---

# 14. Assumptions

The implementation makes the following assumptions:

1. The supplied Excel file is located at `app/db/sheet/trades.xlsx`. which in future can be moved to insertion by user as its being handled separately from API.
2. The relevant Excel worksheet is named `new_trade_data`.
3. `trade_id` is intended to uniquely identify a trade.
4. `source_file` should contain the filename of the imported source file.
5. PostgreSQL is available locally during development.
6. Database credentials are provided through environment variables.
7. The initial import is performed manually rather than automatically when the API starts.
8. The API operates against the `trades` PostgreSQL table.

---

# 16. Quick Start

For a clean development environment, the main workflow is:

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create PostgreSQL database
createdb -U postgres tradesdb

# 4. Configure .env
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=tradesdb

# 5. Import Excel data
python -m app.import_data

# 6. Start API
python -m uvicorn app.main:app --reload

# 7. Run tests
python -m pytest -v
```

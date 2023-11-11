import sqlite3


def create_connection(db_file: str) -> sqlite3.Connection:
    """
    creates a database connection to the SQLite database
    specified by db_file

    Args:
        db_file: Database file

    Returns:
        conn: Established connection
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn: sqlite3.Connection, create_table_sql: str):
    """
    Creates a table from the create_table_sql statement

    Args:
        conn: Connection object
        create_table_sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def add_ticker(conn: sqlite3.Connection, ticker: list[str]) -> int:
    """
    Creates a new ticker into the tickers table

    Args:
        conn: Connection object to the db
        ticker: A list of tickers

    Returns:
        int: id of the inserted ticker
    """
    sql = """
        INSERT INTO Tickers(name)
        VALUES(?)
    """
    cur = conn.cursor()
    try:
        cur.execute(sql, ticker)
    except sqlite3.IntegrityError as e:
        print(f"{e.args[0]}: {ticker[0]} already exists")
    conn.commit()
    return cur.lastrowid


def add_price_data(conn: sqlite3.Connection, data: tuple) -> int:
    """
    Creates a new entry in the price table
    Args:
        conn: Connection object to the db
        data: The row to be inserted

    Returns:
        int: The id of the inserted row
    """

    sql = """
        INSERT INTO StockData(ticker_id,date_time,open_price,close_price,adj_close_price,high_price,low_price,volume)
        VALUES(?,?,?,?,?,?,?,?)
    """
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

    return cur.lastrowid


if __name__ == "__main__":
    database = "C:/Users/henri/treidaus/treidaus-setti/server/server_data/test.sqlite"
    sql_create_Tickers_table = """CREATE TABLE IF NOT EXISTS Tickers (
                                ticker_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL UNIQUE
                                );"""
    sql_create_StockData_table = """CREATE TABLE IF NOT EXISTS StockData (
                                data_id INTEGER PRIMARY KEY,
                                ticker_id INTEGER,
                                date_time DATETIME,
                                open_price REAL,
                                close_price REAL,
                                adj_close_price REAL,
                                high_price REAL,
                                low_price REAL,
                                volume INTEGER,
                                FOREIGN KEY (ticker_id) REFERENCES Tickers(ticker_id)
                                );"""

    conn = create_connection(database)
    if conn is not None:
        sql_query = """SELECT name FROM sqlite_master 
            WHERE type='table';"""
        cursor = conn.cursor()
        cursor.execute(sql_query)
        tables = [i[0] for i in cursor.fetchall()]
        if "Tickers" not in tables:
            print("Adding table Tickers")
            create_table(conn, sql_create_Tickers_table)
        if "StockData" not in tables:
            print("Adding table StockData")
            create_table(conn, sql_create_StockData_table)

    else:
        print("Error! cannot create the database connection.")

    a = {
        "2023-10-27T00:00:00.000": {
            "('Adj Close', 'AAPL')": 168.2200012207,
            "('Adj Close', 'MSFT')": 329.8099975586,
            "('Close', 'AAPL')": 168.2200012207,
            "('Close', 'MSFT')": 329.8099975586,
            "('High', 'AAPL')": 168.9600067139,
            "('High', 'MSFT')": 336.7200012207,
            "('Low', 'AAPL')": 166.8300018311,
            "('Low', 'MSFT')": 328.3999938965,
            "('Open', 'AAPL')": 166.9100036621,
            "('Open', 'MSFT')": 330.4299926758,
            "('Volume', 'AAPL')": 58468600,
            "('Volume', 'MSFT')": 29835200,
        }
    }
    with conn:
        # create a new Ticker
        ticker = ("MSFT",)
        ticker_id = add_ticker(conn, ticker)

        b = [
            (
                ticker_id,
                key,
                i["Open"],
                i["Close"],
                i["Adj Close"],
                i["High"],
                i["Low"],
                i["Volume"],
            )
            for key, i in a.items()
        ]

        # create tasks
        add_price_data(conn, b[0])

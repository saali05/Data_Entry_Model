import sqlite3
from datetime import datetime


DATABASE_PATH = "data/transactions.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_PATH)


def create_table():
    """
    Create the transactions table if it doesn't already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            account_number TEXT,
            ifsc_code TEXT,
            amount REAL,
            source_message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def insert_transaction(data, source_message):
    """
    Insert a validated transaction into the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            name,
            account_number,
            ifsc_code,
            amount,
            source_message,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["account_number"],
            data["ifsc_code"],
            data["amount"],
            source_message,
            "PENDING",
            datetime.now().isoformat(),
        ),
    )

    transaction_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return transaction_id


def get_all_transactions():
    """
    Retrieve all transactions from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            account_number,
            ifsc_code,
            amount,
            source_message,
            status,
            created_at
        FROM transactions
        ORDER BY id DESC
        """
    )

    transactions = cursor.fetchall()

    connection.close()

    return transactions


if __name__ == "__main__":

    create_table()

    print("=" * 60)
    print("Database Setup")
    print("=" * 60)
    print("Transactions table created successfully.")
    print(f"Database: {DATABASE_PATH}")

    transactions = get_all_transactions()

    print("\nStored Transactions")
    print("-" * 60)

    if not transactions:
        print("No transactions found.")

    else:
        for transaction in transactions:
            print(transaction)

import os
import sqlite3
import sys
from pathlib import Path


# Database location
#
# Development:
# Keep using the existing project database.
#
# Packaged executable:
# Store data in a persistent Windows user-data folder.

if getattr(sys, "frozen", False):
    app_data = os.environ.get("LOCALAPPDATA")

    if app_data:
        BASE_DIR = Path(app_data) / "Khula"
    else:
        BASE_DIR = Path.home() / "Khula"
else:
    BASE_DIR = Path(__file__).resolve().parent


# Ensure the database directory exists.
BASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = BASE_DIR / "khula.db"


def get_connection():
    """Create a SQLite database connection."""

    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create Khula database tables if they do not exist."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                quantity INTEGER NOT NULL DEFAULT 0
                    CHECK(quantity >= 0),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL
                    CHECK(quantity > 0),
                total REAL NOT NULL CHECK(total >= 0),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id)
                    REFERENCES products(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0),
                category TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        print("Khula database initialized successfully!")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

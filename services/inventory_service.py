
import sqlite3
from database.db import get_connection


def add_product(name, price, quantity):
    """Add a new product to the inventory."""

    name = name.strip()
    price = round(float(price), 2)
    quantity = int(quantity)

    if not name:
        raise ValueError("Product name cannot be empty.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
        """, (name, price, quantity))

        connection.commit()
        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_all_products():
    """Retrieve all inventory products."""

    connection = get_connection()

    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, price, quantity
            FROM products
            ORDER BY name ASC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def update_product(product_id, name, price, quantity):
    """Update an existing product."""

    name = name.strip()
    price = round(float(price), 2)
    quantity = int(quantity)

    if not name:
        raise ValueError("Product name cannot be empty.")

    if price < 0 or quantity < 0:
        raise ValueError(
            "Price and quantity cannot be negative."
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE products
            SET name = ?, price = ?, quantity = ?
            WHERE id = ?
        """, (name, price, quantity, product_id))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_product(product_id):
    """Delete a product if it is not referenced by sales."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM products
            WHERE id = ?
        """, (product_id,))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError(
            "This product has sales records and cannot "
            "be deleted."
        )

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_inventory_summary():
    """Return the total products and available stock."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_products,
                COALESCE(SUM(quantity), 0) AS total_units
            FROM products
        """)

        result = cursor.fetchone()

        return {
            "total_products": result[0],
            "total_units": result[1]
        }

    finally:
        connection.close()

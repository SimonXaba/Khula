
import sqlite3
import math

from database.db import get_connection


# -----------------------------------------
# INPUT VALIDATION
# -----------------------------------------

def validate_product(name, price, quantity):
    """Validate and normalize inventory inputs."""

    if not isinstance(name, str):
        raise ValueError("Product name must be text.")

    name = name.strip()

    if not name:
        raise ValueError("Product name cannot be empty.")

    try:
        price = float(price)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Please enter a valid price.")

    if not math.isfinite(price):
        raise ValueError("Price must be a finite number.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    price = round(price, 2)

    if isinstance(quantity, bool):
        raise ValueError("Quantity must be a whole number.")

    try:
        quantity_value = float(quantity)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Quantity must be a whole number.")

    if not math.isfinite(quantity_value):
        raise ValueError("Quantity must be a finite number.")

    if not quantity_value.is_integer():
        raise ValueError("Quantity must be a whole number.")

    if quantity_value < 0:
        raise ValueError("Quantity cannot be negative.")

    quantity = int(quantity_value)

    return name, price, quantity


# -----------------------------------------
# ADD PRODUCT
# -----------------------------------------

def add_product(name, price, quantity):
    """Add a validated product to inventory."""

    name, price, quantity = validate_product(
        name, price, quantity
    )

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


# -----------------------------------------
# GET ALL PRODUCTS
# -----------------------------------------

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


# -----------------------------------------
# UPDATE PRODUCT
# -----------------------------------------

def update_product(product_id, name, price, quantity):
    """Update an existing product."""

    name, price, quantity = validate_product(
        name, price, quantity
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


# -----------------------------------------
# DELETE PRODUCT
# -----------------------------------------

def delete_product(product_id):
    """Delete a product unless referenced by sales."""

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


# -----------------------------------------
# INVENTORY SUMMARY
# -----------------------------------------

def get_inventory_summary():
    """Return total products and available stock."""

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

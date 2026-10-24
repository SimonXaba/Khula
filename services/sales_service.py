
import sqlite3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from database.db import get_connection


def record_sale(product_id, quantity):
    """Record a sale and reduce stock atomically."""

    try:
        product_id = int(product_id)
        quantity = int(quantity)
    except (ValueError, TypeError):
        raise ValueError("Invalid product or quantity.")

    if product_id <= 0:
        raise ValueError("Invalid product selected.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    connection = get_connection()

    try:
        # Begin a write transaction to protect stock updates.
        connection.execute("BEGIN IMMEDIATE")

        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, price, quantity
            FROM products
            WHERE id = ?
        """, (product_id,))

        product = cursor.fetchone()

        if product is None:
            raise ValueError("Product not found.")

        name, price, available_stock = product

        if quantity > available_stock:
            raise ValueError(
                f"Insufficient stock. Only "
                f"{available_stock} units available."
            )

        try:
            unit_price = Decimal(str(price))
            if not unit_price.is_finite() or unit_price < 0:
                raise ValueError("Invalid product price.")

            total = (
                unit_price * Decimal(quantity)
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        except InvalidOperation:
            raise ValueError("Invalid product price.")

        cursor.execute("""
            UPDATE products
            SET quantity = quantity - ?
            WHERE id = ? AND quantity >= ?
        """, (quantity, product_id, quantity))

        if cursor.rowcount != 1:
            raise ValueError("Stock update failed.")

        cursor.execute("""
            INSERT INTO sales (product_id, quantity, total)
            VALUES (?, ?, ?)
        """, (product_id, quantity, float(total)))

        sale_id = cursor.lastrowid
        connection.commit()

        return {
            "sale_id": sale_id,
            "product": name,
            "quantity": quantity,
            "total": float(total)
        }

    except (ValueError, sqlite3.Error):
        connection.rollback()
        raise

    finally:
        connection.close()


def get_all_sales():
    """Retrieve recorded sales."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                sales.id,
                products.name AS product,
                sales.quantity,
                sales.total,
                sales.created_at
            FROM sales
            JOIN products
                ON sales.product_id = products.id
            ORDER BY sales.id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_sales_summary():
    """Calculate total sales revenue and transactions."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(total), 0)
            FROM sales
        """)

        count, revenue = cursor.fetchone()

        return {
            "transactions": count,
            "revenue": round(revenue, 2)
        }

    finally:
        connection.close()

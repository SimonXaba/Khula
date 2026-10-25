
import math
import sqlite3

from database.db import get_connection


def add_expense(description, amount, category):
    """Validate and save a business expense."""

    if not isinstance(description, str):
        raise ValueError("Expense description must be text.")

    if not isinstance(category, str):
        raise ValueError("Expense category must be text.")

    description = description.strip()
    category = category.strip()

    if not description:
        raise ValueError("Expense description is required.")

    if not category:
        raise ValueError("Expense category is required.")

    try:
        amount = float(amount)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Please enter a valid amount.")

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError(
            "Expense amount must be greater than zero."
        )

    amount = round(amount, 2)

    if amount <= 0:
        raise ValueError(
            "Expense amount must be at least R0.01."
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses (
                description,
                amount,
                category
            )
            VALUES (?, ?, ?)
        """, (description, amount, category))

        connection.commit()
        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_all_expenses():
    """Retrieve all recorded expenses."""

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                description,
                amount,
                category,
                created_at
            FROM expenses
            ORDER BY id DESC
        """)

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


def delete_expense(expense_id):
    """Delete an expense by ID."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (expense_id,))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_expense_summary():
    """Calculate total spending and expense count."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0)
            FROM expenses
        """)

        count, total = cursor.fetchone()

        return {
            "total_expenses": count,
            "total_spending": round(total, 2)
        }

    finally:
        connection.close()

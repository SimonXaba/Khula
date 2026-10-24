
from database.db import get_connection


def get_financial_report():
    """
    Generate a financial summary using locally
    stored sales, expenses, and inventory data.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Total sales revenue
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(total), 0)
            FROM sales
        """)

        sales_count, total_sales = cursor.fetchone()

        # Total recorded expenses
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0)
            FROM expenses
        """)

        expense_count, total_expenses = cursor.fetchone()

        # Current inventory valuation
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(quantity), 0),
                COALESCE(SUM(price * quantity), 0)
            FROM products
        """)

        product_count, stock_units, inventory_value = (
            cursor.fetchone()
        )

        # Simplified financial balance
        estimated_balance = total_sales - total_expenses

        return {
            "sales_count": sales_count,
            "total_sales": round(total_sales, 2),
            "expense_count": expense_count,
            "total_expenses": round(total_expenses, 2),
            "estimated_balance": round(
                estimated_balance, 2
            ),
            "product_count": product_count,
            "stock_units": stock_units,
            "inventory_value": round(
                inventory_value, 2
            )
        }

    finally:
        connection.close()

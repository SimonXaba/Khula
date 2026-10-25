
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from database.db import initialize_database
from services.sales_service import record_sale


passed = 0
failed = 0


def check(name, condition):
    global passed, failed

    if condition:
        passed += 1
        print(f"PASS - {name}")
    else:
        failed += 1
        print(f"FAIL - {name}")


with tempfile.TemporaryDirectory() as folder:

    test_db = Path(folder) / "test_khula.db"

    def test_connection():
        connection = sqlite3.connect(test_db)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    # Redirect database operations to temporary storage.
    with patch(
        "database.db.get_connection",
        side_effect=test_connection
    ), patch(
        "services.sales_service.get_connection",
        side_effect=test_connection
    ):

        initialize_database()

        connection = test_connection()

        connection.execute("""
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
        """, ("Test Sugar", 25.00, 10))

        product_id = connection.execute(
            "SELECT id FROM products"
        ).fetchone()[0]

        connection.commit()
        connection.close()

        def get_stock():
            connection = test_connection()
            try:
                return connection.execute(
                    "SELECT quantity FROM products WHERE id = ?",
                    (product_id,)
                ).fetchone()[0]
            finally:
                connection.close()

        def get_sale_count():
            connection = test_connection()
            try:
                return connection.execute(
                    "SELECT COUNT(*) FROM sales"
                ).fetchone()[0]
            finally:
                connection.close()

        # Test 1: Reject zero quantity
        try:
            record_sale(product_id, 0)
            check("Zero quantity rejected", False)
        except ValueError:
            check("Zero quantity rejected", True)

        # Test 2: Reject negative quantity
        try:
            record_sale(product_id, -5)
            check("Negative quantity rejected", False)
        except ValueError:
            check("Negative quantity rejected", True)

        # Test 3: Reject insufficient stock
        try:
            record_sale(product_id, 100)
            check("Insufficient stock rejected", False)
        except ValueError:
            check("Insufficient stock rejected", True)

        # Test 4: Failed sale does not change stock
        check(
            "Stock unchanged after failed sales",
            get_stock() == 10
        )

        # Test 5: Failed sales create no transactions
        check(
            "No transactions created by failed sales",
            get_sale_count() == 0
        )

        # Test 6: Reject nonexistent product
        try:
            record_sale(999999, 1)
            check("Nonexistent product rejected", False)
        except ValueError:
            check("Nonexistent product rejected", True)

        # Test 7: Record a valid sale
        try:
            result = record_sale(product_id, 3)

            check(
                "Valid sale recorded",
                result["total"] == 75.00
            )
        except Exception as error:
            print(f"Unexpected error: {error}")
            check("Valid sale recorded", False)

        # Test 8: Stock reduced correctly
        check(
            "Stock reduced correctly",
            get_stock() == 7
        )

        # Test 9: Sale saved exactly once
        check(
            "Sale transaction saved",
            get_sale_count() == 1
        )


print("\n-----------------------------")
print(f"Tests passed: {passed}")
print(f"Tests failed: {failed}")
print("-----------------------------")

if failed == 0:
    print("Sales security tests PASSED!")
else:
    print("Sales security tests FAILED!")

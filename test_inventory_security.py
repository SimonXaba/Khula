
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from database.db import initialize_database
from services.inventory_service import (
    add_product,
    get_all_products,
    update_product,
    delete_product,
    get_inventory_summary
)


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


def rejects_value(action):
    try:
        action()
        return False
    except ValueError:
        return True


with tempfile.TemporaryDirectory() as folder:

    test_db = Path(folder) / "test_inventory.db"

    def test_connection():
        connection = sqlite3.connect(test_db)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    with patch(
        "database.db.get_connection",
        side_effect=test_connection
    ), patch(
        "services.inventory_service.get_connection",
        side_effect=test_connection
    ):

        initialize_database()

        # Test 1: Add a valid product
        product_id = add_product("Sugar", 25, 10)

        check(
            "Valid product added",
            product_id > 0
        )

        # Test 2: Reject empty name
        check(
            "Empty product name rejected",
            rejects_value(
                lambda: add_product("", 25, 10)
            )
        )

        # Test 3: Reject negative price
        check(
            "Negative price rejected",
            rejects_value(
                lambda: add_product("Sugar", -5, 10)
            )
        )

        # Test 4: Reject negative quantity
        check(
            "Negative quantity rejected",
            rejects_value(
                lambda: add_product("Sugar", 25, -3)
            )
        )

        # Test 5: Reject decimal quantity
        check(
            "Decimal quantity rejected",
            rejects_value(
                lambda: add_product("Sugar", 25, 3.8)
            )
        )

        # Test 6: Reject non-finite price
        check(
            "Non-finite price rejected",
            rejects_value(
                lambda: add_product("Sugar", float("nan"), 5)
            )
        )

        # Test 7: Reject infinite price
        check(
            "Infinite price rejected",
            rejects_value(
                lambda: add_product("Sugar", float("inf"), 5)
            )
        )

        # Test 8: Update existing product
        updated = update_product(
            product_id, "Brown Sugar", 30, 15
        )

        check(
            "Product updated",
            updated
        )

        # Test 9: Verify update persisted
        products = get_all_products()

        check(
            "Updated data persisted",
            len(products) == 1
            and products[0]["name"] == "Brown Sugar"
            and products[0]["quantity"] == 15
        )

        # Test 10: Verify inventory summary
        summary = get_inventory_summary()

        check(
            "Inventory summary correct",
            summary["total_products"] == 1
            and summary["total_units"] == 15
        )

        # Test 11: SQL injection treated as text
        malicious_name = "Sugar'); DROP TABLE products; --"

        injected_id = add_product(
            malicious_name, 20, 2
        )

        check(
            "SQL injection treated as text",
            injected_id > 0
            and len(get_all_products()) == 2
        )

        # Test 12: Delete a product
        deleted = delete_product(injected_id)

        check(
            "Product deleted",
            deleted
            and len(get_all_products()) == 1
        )


print("\n-----------------------------")
print(f"Tests passed: {passed}")
print(f"Tests failed: {failed}")
print("-----------------------------")

if failed == 0:
    print("Inventory security tests PASSED!")
else:
    print("Inventory security tests FAILED!")

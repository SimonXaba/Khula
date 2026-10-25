
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from database.db import initialize_database
from services.expense_service import (
    add_expense,
    get_all_expenses,
    delete_expense,
    get_expense_summary
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

    test_db = Path(folder) / "test_expenses.db"

    def test_connection():
        connection = sqlite3.connect(test_db)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    with patch(
        "database.db.get_connection",
        side_effect=test_connection
    ), patch(
        "services.expense_service.get_connection",
        side_effect=test_connection
    ):

        initialize_database()

        # Test 1: Add valid expense
        expense_id = add_expense(
            "Transport", 50, "Travel"
        )

        check(
            "Valid expense added",
            expense_id > 0
        )

        # Test 2: Reject empty description
        check(
            "Empty description rejected",
            rejects_value(
                lambda: add_expense("", 50, "Travel")
            )
        )

        # Test 3: Reject empty category
        check(
            "Empty category rejected",
            rejects_value(
                lambda: add_expense("Transport", 50, "")
            )
        )

        # Test 4: Reject negative amount
        check(
            "Negative amount rejected",
            rejects_value(
                lambda: add_expense("Transport", -10, "Travel")
            )
        )

        # Test 5: Reject zero amount
        check(
            "Zero amount rejected",
            rejects_value(
                lambda: add_expense("Transport", 0, "Travel")
            )
        )

        # Test 6: Reject nonnumeric amount
        check(
            "Invalid amount rejected",
            rejects_value(
                lambda: add_expense("Transport", "abc", "Travel")
            )
        )

        # Test 7: Reject NaN
        check(
            "NaN amount rejected",
            rejects_value(
                lambda: add_expense("Transport", float("nan"), "Travel")
            )
        )

        # Test 8: Reject infinity
        check(
            "Infinite amount rejected",
            rejects_value(
                lambda: add_expense("Transport", float("inf"), "Travel")
            )
        )

        # Test 9: Reject amount rounding to zero
        check(
            "Tiny amount rejected",
            rejects_value(
                lambda: add_expense("Transport", 0.001, "Travel")
            )
        )

        # Test 10: Summary is correct
        summary = get_expense_summary()

        check(
            "Expense summary correct",
            summary["total_expenses"] == 1
            and summary["total_spending"] == 50.00
        )

        # Test 11: SQL injection treated as text
        malicious_text = "Travel'); DROP TABLE expenses; --"

        injected_id = add_expense(
            malicious_text, 20, "Other"
        )

        check(
            "SQL injection treated as text",
            injected_id > 0
            and len(get_all_expenses()) == 2
        )

        # Test 12: Delete expense
        deleted = delete_expense(injected_id)

        check(
            "Expense deleted successfully",
            deleted
            and len(get_all_expenses()) == 1
        )

        # Test 13: Invalid deletion returns False
        check(
            "Nonexistent expense deletion handled",
            delete_expense(999999) is False
        )


print("\n-----------------------------")
print(f"Tests passed: {passed}")
print(f"Tests failed: {failed}")
print("-----------------------------")

if failed == 0:
    print("Expense security tests PASSED!")
else:
    print("Expense security tests FAILED!")

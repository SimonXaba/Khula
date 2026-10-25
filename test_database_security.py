
import sqlite3

# Temporary database stored in memory
# Your real Khula database will not be modified.
connection = sqlite3.connect(":memory:")

connection.execute("PRAGMA foreign_keys = ON")

connection.execute("""
    CREATE TABLE test_products (
        id INTEGER PRIMARY KEY,
        price REAL CHECK(price >= 0),
        quantity INTEGER CHECK(quantity >= 0)
    )
""")

# Test 1: Valid product
try:
    connection.execute(
        "INSERT INTO test_products (price, quantity) VALUES (?, ?)",
        (10, 5)
    )
    print("Test 1 - Valid product: PASS")
except sqlite3.IntegrityError:
    print("Test 1 - Valid product: FAIL")


# Test 2: Negative price
try:
    connection.execute(
        "INSERT INTO test_products (price, quantity) VALUES (?, ?)",
        (-10, 5)
    )
    print("Test 2 - Negative price rejected: FAIL")
except sqlite3.IntegrityError:
    print("Test 2 - Negative price rejected: PASS")


# Test 3: Negative stock quantity
try:
    connection.execute(
        "INSERT INTO test_products (price, quantity) VALUES (?, ?)",
        (10, -5)
    )
    print("Test 3 - Negative quantity rejected: FAIL")
except sqlite3.IntegrityError:
    print("Test 3 - Negative quantity rejected: PASS")


# Test 4: Foreign key enforcement
foreign_keys = connection.execute(
    "PRAGMA foreign_keys"
).fetchone()[0]

if foreign_keys == 1:
    print("Test 4 - Foreign keys enabled: PASS")
else:
    print("Test 4 - Foreign keys enabled: FAIL")


connection.close()

print("\nDatabase security tests completed.")

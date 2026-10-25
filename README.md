# Khula — Empowering Township and Rural Entrepreneurs

**Khula** is an offline-first business management application designed to help young founders, township entrepreneurs, and rural businesses manage their daily operations.

Khula means *grow* in isiZulu, reflecting our mission to help small businesses grow through accessible digital tools.

## The Problem

Many small businesses in underserved communities face challenges such as:

- Limited access to affordable digital business tools.
- Unreliable internet connectivity.
- Difficulty tracking inventory, sales, and expenses.
- Limited visibility into business performance.
- Reliance on paper-based recordkeeping.

## Our Solution

Khula provides a simple desktop application that enables entrepreneurs to manage essential business activities without requiring a continuous internet connection.

## Core Features

### 1. Business Dashboard
- View total sales revenue.
- Track business expenses.
- Monitor estimated balance.
- View inventory statistics.
- Navigate between business management modules.

### 2. Inventory Management
- Add new products.
- Update product information.
- Delete eligible products.
- Track stock quantities.
- Validate product prices and quantities.

### 3. Sales Management
- Record product sales.
- Calculate transaction totals.
- Automatically reduce inventory.
- Prevent sales exceeding available stock.
- View sales history.

### 4. Expense Management
- Record business expenses.
- Categorize expenses.
- View expense history.
- Delete expense records.
- Monitor total spending.

### 5. Business Reports
- Total sales revenue.
- Number of sales transactions.
- Total business expenses.
- Expense transaction count.
- Estimated balance.
- Inventory value at selling prices.
- Product count.
- Available stock units.

### 6. Offline Functionality
- Operates without an internet connection.
- Stores business information locally using SQLite.
- Preserves records after application restarts.

**Note:** Online synchronization is a planned enhancement and is not included in the current MVP.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Kivy |
| Database | SQLite |
| Development environment | Visual Studio Code |
| Version control | Git and GitHub |
| Target platform | Desktop (Windows development environment) |

## Project Structure

```text
Khula/
├── main.py
├── database/
│   └── db.py
├── screens/
│   ├── dashboard.py
│   ├── inventory.py
│   ├── sales.py
│   ├── expenses.py
│   └── reports.py
├── services/
│   ├── inventory_service.py
│   ├── sales_service.py
│   ├── expense_service.py
│   └── reports_service.py
├── test_database_security.py
├── test_sales_security.py
├── test_inventory_security.py
├── test_expense_security.py
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.13 or a compatible Python version.
- pip.
- Git (optional).

### Installation

1. Clone the repository:

   `git clone YOUR_REPOSITORY_URL`

2. Navigate to the project folder:

   `cd Khula`

3. Create a virtual environment:

   `python -m venv .venv`

4. Activate it in Windows PowerShell:

   `.\.venv\Scripts\Activate.ps1`

5. Install Kivy:

   `python -m pip install kivy==2.3.1`

6. Launch Khula:

   `python main.py`

The application initializes its SQLite database locally.

## Security and Data Integrity

Khula includes several safeguards:

- Parameterized SQL queries to reduce SQL injection risks.
- Input validation for product prices, quantities, and expense amounts.
- SQLite database constraints.
- Foreign key enforcement.
- Atomic sales transactions.
- Stock availability checks.
- Transaction rollback handling for supported database failures.

**Security scope:** This is a hackathon MVP. It does not currently provide user authentication, encrypted local storage, or cloud-based backup.

## Testing

The following checks were completed successfully:

| Test category | Passed |
|---|---:|
| Database constraints | 4/4 |
| Sales transaction security | 9/9 |
| Inventory security | 12/12 |
| Expense security | 13/13 |
| Inventory interface | 3/3 |
| Expense interface | 3/3 |
| End-to-end workflow | 6/6 |

**Total: 50/50 checks passed.**

Additional offline functionality and local data persistence tests were also completed successfully.

### Run Automated Tests

text
python test_database_security.py
python test_sales_security.py
python test_inventory_security.py
python test_expense_security.py


## Current Limitations

- No cloud synchronization.
- No online payment processing.
- No user authentication.
- No supplier or marketplace integration.
- Inventory valuation is based on selling prices, not acquisition costs.
- Estimated balance represents sales revenue minus recorded expenses, not formal accounting profit.

## Future Improvements

- Optional cloud backup and synchronization.
- Mobile application support.
- Digital payment integration.
- Supplier and marketplace connections.
- Business registration and compliance guidance.
- Advanced financial analytics.
- Multilingual accessibility.
- User authentication and stronger data protection.

## Hackathon Challenge

**Problem Statement #3:** How might digital tools help young founders and township/rural businesses start, trade, get paid, manage cash flow, and reach formal markets?

Khula addresses the business management and cash-flow visibility aspects of this challenge through an accessible, offline-first solution.

## Project Status

**Functional hackathon MVP — core features implemented and tested.**

Built with Python, Kivy, and SQLite.

**Khula — Grow Your Business.**
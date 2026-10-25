# Khula — Empowering Township and Rural Entrepreneurs

**Khula — Grow Your Business**

Khula is an offline-first business management application designed to help young founders, township entrepreneurs, and rural businesses manage their daily operations.

*Khula* means **grow** in isiZulu, reflecting our mission to help small businesses grow through accessible digital tools.

**GitHub Repository:** https://github.com/SimonXaba/Khula

## The Problem

Many small businesses in underserved communities face challenges such as:

- Limited access to affordable digital business tools.
- Unreliable internet connectivity.
- Difficulty tracking inventory, sales, and expenses.
- Limited visibility into business performance.
- Reliance on paper-based recordkeeping.

## Our Solution

Khula provides a simple desktop application that enables entrepreneurs to manage essential business activities without requiring an internet connection.

The current MVP focuses on inventory management, sales tracking, expense recording, business reporting, and offline data persistence.

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
- Track available stock quantities.
- Validate product prices and quantities.

### 3. Sales Management

- Record product sales.
- Calculate transaction totals.
- Automatically reduce inventory quantities.
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
- Number of expense transactions.
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
| Programming Language | Python 3.13 |
| User Interface | Kivy 2.3.1 |
| Database | SQLite |
| Executable Packaging | PyInstaller |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |
| Target Platform | Windows Desktop |

## Technical Architecture

Khula follows a layered architecture:

**Presentation Layer:** Kivy screens provide the dashboard, inventory, sales, expenses, and reports interfaces.

**Business Logic Layer:** Python service modules manage validation, business operations, calculations, and transactions.

**Data Layer:** SQLite provides persistent local storage for products, sales, and expenses.

**Data Flow:**

User → Kivy Interface → Python Services → SQLite Database

All core business operations are performed locally without requiring a server or internet connection.

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

### Option 1: Run the Windows Executable (Recommended for Judges)

The Windows executable is provided separately as part of the hackathon submission.

**Requirements:**

- Windows 10 or Windows 11.
- No separate Python installation required.
- No internet connection required for core functionality.

**Instructions:**

1. Download `Khula_Windows_Build.zip` from the hackathon submission.
2. Extract the ZIP file.
3. Open the extracted `Khula` folder.
4. Double-click `Khula.exe`.
5. The application will open to the Khula Dashboard.

**Demo Account Details:**

- Username: Not required.
- Password: Not required.
- Authentication: Not implemented in the current MVP.

The executable automatically creates a local SQLite database when first launched.

**Windows Database Location:**

```text
%LOCALAPPDATA%\Khula\khula.db
```

Business records remain available after closing and reopening the application.

**Important:** Keep the executable and its supporting files together in the extracted folder.

### Option 2: Run from Source Code

**Prerequisites:**

- Python 3.13.
- pip.
- Git (optional).

**Step 1 — Clone the repository**

```powershell
git clone https://github.com/SimonXaba/Khula.git
```

**Step 2 — Navigate to the project**

```powershell
cd Khula
```

**Step 3 — Create a virtual environment**

```powershell
python -m venv .venv
```

**Step 4 — Activate the virtual environment (Windows PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Step 5 — Install Kivy**

```powershell
python -m pip install Kivy==2.3.1
```

**Step 6 — Launch Khula**

```powershell
python main.py
```

When running from source, Khula initializes its SQLite database locally in the `database` directory.

## Security and Data Integrity

Khula implements the following safeguards:

- Parameterized SQL queries to reduce SQL injection risks.
- Input validation for product prices, quantities, and expense amounts.
- SQLite database constraints.
- Foreign key enforcement.
- Atomic sales transactions.
- Stock availability checks.
- Transaction rollback handling for supported database failures.

**Security Scope:** Khula is a hackathon MVP. It does not currently provide user authentication, encrypted local storage, or cloud-based backup.

## Testing and Quality Assurance

The following checks were completed successfully:

| Test Category | Passed |
|---|---|
| Database Constraints | 4/4 |
| Sales Transaction Security | 9/9 |
| Inventory Security | 12/12 |
| Expense Security | 13/13 |
| Inventory Interface | 3/3 |
| Expense Interface | 3/3 |
| End-to-End Workflow | 6/6 |
| **Total** | **50/50** |

Additional offline functionality and data persistence tests were completed successfully.

### Windows Executable Verification

The packaged executable also passed six final checks:

1. Inventory records can be created.
2. Sales transactions correctly reduce available stock.
3. Business expenses can be recorded.
4. Dashboard and reports reflect transactions.
5. Data remains available after restarting the executable.
6. The persistent SQLite database is created in the Windows application-data directory.

### Run Automated Tests

From the project root, execute the following commands separately:

```powershell
python test_database_security.py
python test_sales_security.py
python test_inventory_security.py
python test_expense_security.py
```

## Example User Journey

Consider a small township entrepreneur selling bread and everyday essentials.

1. **Start:** Open Khula without an internet connection.
2. **Inventory:** Add products, selling prices, and available stock.
3. **Sales:** Record a customer purchase.
4. **Stock Update:** Khula automatically reduces the available stock.
5. **Expenses:** Record a transport or operating expense.
6. **Reports:** Review sales revenue, expenses, and estimated balance.
7. **Persistence:** Close and reopen Khula without losing recorded information.

This workflow demonstrates how Khula supports everyday business recordkeeping.

## Current Limitations

- No cloud synchronization.
- No online payment processing.
- No user authentication.
- No supplier or marketplace integration.
- No mobile application build.
- Inventory valuation uses selling prices rather than acquisition costs.
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

**Problem Statement #3**

*How might digital tools help young founders and township/rural businesses start, trade, get paid, manage cash flow, and reach formal markets?*

Khula addresses the business management and cash-flow visibility aspects of this challenge through an accessible, offline-first solution.

## Project Status

**Functional Hackathon MVP — Core Features Implemented and Tested**

- Desktop application developed.
- Core business modules implemented.
- Offline SQLite persistence verified.
- Automated security tests passed.
- Windows executable successfully built.
- Final executable functionality verified.

**GitHub:** https://github.com/SimonXaba/Khula

**Khula — Grow Your Business.**
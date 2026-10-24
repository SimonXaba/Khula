
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.dashboard import DashboardScreen
from screens.inventory import InventoryScreen
from screens.sales import SalesScreen
from screens.expenses import ExpensesScreen
from screens.reports import ReportsScreen

from database.db import initialize_database


Window.size = (420, 700)
Window.clearcolor = (0.06, 0.10, 0.09, 1)


class KhulaApp(App):

    def build(self):
        self.title = "Khula - Business Management"

        initialize_database()

        self.manager = ScreenManager()

        # Business Dashboard
        dashboard_page = Screen(name="dashboard")
        self.dashboard = DashboardScreen()
        dashboard_page.add_widget(self.dashboard)
        self.manager.add_widget(dashboard_page)

        # Inventory Management
        inventory_page = Screen(name="inventory")
        self.inventory_screen = InventoryScreen(
            go_back=self.show_dashboard
        )
        inventory_page.add_widget(self.inventory_screen)
        self.manager.add_widget(inventory_page)

        # Sales Management
        sales_page = Screen(name="sales")
        self.sales_screen = SalesScreen(
            go_back=self.show_dashboard
        )
        sales_page.add_widget(self.sales_screen)
        self.manager.add_widget(sales_page)

        # Expense Management
        expenses_page = Screen(name="expenses")
        self.expenses_screen = ExpensesScreen(
            go_back=self.show_dashboard
        )
        expenses_page.add_widget(self.expenses_screen)
        self.manager.add_widget(expenses_page)

        # Financial Reports
        reports_page = Screen(name="reports")
        self.reports_screen = ReportsScreen(
            go_back=self.show_dashboard
        )
        reports_page.add_widget(self.reports_screen)
        self.manager.add_widget(reports_page)

        # Connect dashboard buttons
        self.dashboard.handle_action = self.handle_action

        self.manager.current = "dashboard"

        return self.manager

    def handle_action(self, button):

        if button.text == "Manage Stock":
            self.inventory_screen.refresh_products()
            self.manager.current = "inventory"

        elif button.text == "Record Sale":
            self.sales_screen.refresh_data()
            self.manager.current = "sales"

        elif button.text == "Add Expense":
            self.expenses_screen.refresh_data()
            self.manager.current = "expenses"

        elif button.text == "View Reports":
            self.reports_screen.refresh_report()
            self.manager.current = "reports"

        else:
            print(f"Selected: {button.text}")

    def show_dashboard(self):
        self.manager.current = "dashboard"


if __name__ == "__main__":
    KhulaApp().run()

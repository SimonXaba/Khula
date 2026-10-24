
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

# Import Khula application screens
from screens.dashboard import DashboardScreen
from screens.inventory import InventoryScreen
from screens.sales import SalesScreen

# Import database initialization
from database.db import initialize_database


# Khula application window settings
Window.size = (420, 700)
Window.clearcolor = (0.06, 0.10, 0.09, 1)


class KhulaApp(App):

    def build(self):
        self.title = "Khula - Business Management"

        # Initialize SQLite database
        initialize_database()

        # Create screen manager
        self.manager = ScreenManager()

        
        # BUSINESS DASHBOARD
        
        dashboard_page = Screen(name="dashboard")

        self.dashboard = DashboardScreen()

        dashboard_page.add_widget(self.dashboard)
        self.manager.add_widget(dashboard_page)

        
        # INVENTORY MANAGEMENT
        
        inventory_page = Screen(name="inventory")

        self.inventory_screen = InventoryScreen(
            go_back=self.show_dashboard
        )

        inventory_page.add_widget(self.inventory_screen)
        self.manager.add_widget(inventory_page)

        
        # SALES MANAGEMENT
        
        sales_page = Screen(name="sales")

        self.sales_screen = SalesScreen(
            go_back=self.show_dashboard
        )

        sales_page.add_widget(self.sales_screen)
        self.manager.add_widget(sales_page)

        # Connect dashboard buttons
        self.dashboard.handle_action = self.handle_action

        # Display dashboard first
        self.manager.current = "dashboard"

        return self.manager

    
    # DASHBOARD NAVIGATION
    
    def handle_action(self, button):

        if button.text == "Manage Stock":
            self.inventory_screen.refresh_products()
            self.manager.current = "inventory"

        elif button.text == "Record Sale":
            self.sales_screen.refresh_data()
            self.manager.current = "sales"

        else:
            print(f"Selected: {button.text}")

    
    # RETURN TO DASHBOARD
    
    def show_dashboard(self):
        self.manager.current = "dashboard"


if __name__ == "__main__":
    KhulaApp().run()

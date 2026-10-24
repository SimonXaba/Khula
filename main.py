
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.dashboard import DashboardScreen
from screens.inventory import InventoryScreen
from database.db import initialize_database


Window.size = (420, 700)
Window.clearcolor = (0.06, 0.10, 0.09, 1)


class KhulaApp(App):

    def build(self):
        self.title = "Khula - Business Management"

        initialize_database()

        self.manager = ScreenManager()

        dashboard_page = Screen(name="dashboard")
        self.dashboard = DashboardScreen()

        dashboard_page.add_widget(self.dashboard)
        self.manager.add_widget(dashboard_page)

        inventory_page = Screen(name="inventory")
        inventory_page.add_widget(
            InventoryScreen(go_back=self.show_dashboard)
        )
        self.manager.add_widget(inventory_page)

        # Connect the existing Manage Stock button
        self.dashboard.handle_action = self.handle_action

        return self.manager

    def handle_action(self, button):
        if button.text == "Manage Stock":
            self.manager.current = "inventory"
        else:
            print(f"Selected: {button.text}")

    def show_dashboard(self):
        self.manager.current = "dashboard"


if __name__ == "__main__":
    KhulaApp().run()

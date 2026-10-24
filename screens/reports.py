
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from services.reports_service import get_financial_report


class ReportsScreen(BoxLayout):

    def __init__(self, go_back=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        self.go_back = go_back

        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=10
        )

        back_button = Button(
            text="< Back",
            size_hint_x=0.25
        )
        back_button.bind(on_press=self.back)

        header.add_widget(back_button)
        header.add_widget(Label(
            text="Financial Reports",
            bold=True,
            font_size=20
        ))

        self.add_widget(header)

        # Scrollable report area
        scroll = ScrollView()

        self.report_layout = GridLayout(
            cols=1,
            spacing=12,
            padding=10,
            size_hint_y=None
        )

        self.report_layout.bind(
            minimum_height=self.report_layout.setter("height")
        )

        scroll.add_widget(self.report_layout)
        self.add_widget(scroll)

        # Refresh button
        refresh_button = Button(
            text="Refresh Financial Report",
            background_normal="",
            background_color=(0.12, 0.65, 0.35, 1),
            size_hint_y=None,
            height=50
        )

        refresh_button.bind(
            on_press=lambda instance: self.refresh_report()
        )

        self.add_widget(refresh_button)

        self.refresh_report()

    def add_report_item(self, title, value):
        item = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=85,
            padding=10,
            spacing=5
        )

        item.add_widget(Label(
            text=title,
            font_size=15,
            color=(0.7, 0.8, 0.75, 1)
        ))

        item.add_widget(Label(
            text=value,
            font_size=24,
            bold=True,
            color=(0.2, 0.85, 0.45, 1)
        ))

        self.report_layout.add_widget(item)

    def refresh_report(self):
        report = get_financial_report()

        self.report_layout.clear_widgets()

        self.add_report_item(
            "Total Sales Revenue",
            f"R {report['total_sales']:.2f}"
        )

        self.add_report_item(
            "Sales Transactions",
            str(report["sales_count"])
        )

        self.add_report_item(
            "Total Business Expenses",
            f"R {report['total_expenses']:.2f}"
        )

        self.add_report_item(
            "Recorded Expenses",
            str(report["expense_count"])
        )

        self.add_report_item(
            "Estimated Balance",
            f"R {report['estimated_balance']:.2f}"
        )

        self.add_report_item(
            "Inventory Value at Selling Price",
            f"R {report['inventory_value']:.2f}"
        )

        self.add_report_item(
            "Products in Inventory",
            str(report["product_count"])
        )

        self.add_report_item(
            "Available Stock Units",
            str(report["stock_units"])
        )

        self.report_layout.add_widget(Label(
            text=(
                "Estimated balance = sales - expenses.\n"
                "This is not accounting profit."
            ),
            size_hint_y=None,
            height=65,
            font_size=13,
            color=(0.8, 0.8, 0.8, 1)
        ))

    def back(self, instance):
        if self.go_back:
            self.go_back()

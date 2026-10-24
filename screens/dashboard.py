
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from services.reports_service import get_financial_report


class DashboardScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        # Store references to the statistic labels
        self.stat_labels = {}

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15,
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # Application title
        title = Label(
            text="KHULA",
            font_size=34,
            bold=True,
            color=(0.25, 0.85, 0.50, 1),
            size_hint_y=None,
            height=60
        )

        content.add_widget(title)

        # Dashboard subtitle
        subtitle = Label(
            text="Business Overview",
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=45
        )

        content.add_widget(subtitle)

        # Statistics grid
        stats = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None,
            height=190
        )

        statistics = [
            ("Total Sales", "R 0.00"),
            ("Expenses", "R 0.00"),
            ("Estimated Balance", "R 0.00"),
            ("Products", "0")
        ]

        for name, value in statistics:

            card = BoxLayout(
                orientation="vertical",
                padding=10
            )

            name_label = Label(
                text=name,
                font_size=14
            )

            value_label = Label(
                text=value,
                font_size=22,
                bold=True,
                color=(0.25, 0.85, 0.50, 1)
            )

            # Save reference for live updates
            self.stat_labels[name] = value_label

            card.add_widget(name_label)
            card.add_widget(value_label)

            stats.add_widget(card)

        content.add_widget(stats)

        # Quick Actions heading
        actions_title = Label(
            text="Quick Actions",
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=50
        )

        content.add_widget(actions_title)

        # Quick Actions buttons
        actions = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None,
            height=160
        )

        action_names = [
            "Record Sale",
            "Add Expense",
            "Manage Stock",
            "View Reports"
        ]

        for action in action_names:

            button = Button(
                text=action,
                font_size=15,
                background_normal="",
                background_color=(0.12, 0.65, 0.35, 1)
            )

            button.bind(
                on_press=self.handle_action
            )

            actions.add_widget(button)

        content.add_widget(actions)

        scroll.add_widget(content)
        self.add_widget(scroll)

        # Load current database statistics
        self.refresh_statistics()

    def refresh_statistics(self):
        """Refresh dashboard figures from SQLite."""

        report = get_financial_report()

        self.stat_labels["Total Sales"].text = (
            f"R {report['total_sales']:.2f}"
        )

        self.stat_labels["Expenses"].text = (
            f"R {report['total_expenses']:.2f}"
        )

        self.stat_labels["Estimated Balance"].text = (
            f"R {report['estimated_balance']:.2f}"
        )

        self.stat_labels["Products"].text = (
            str(report["product_count"])
        )

    def handle_action(self, button):
        print(f"Selected: {button.text}")

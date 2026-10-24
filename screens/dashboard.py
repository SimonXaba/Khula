
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class DashboardScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

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

        title = Label(
            text="KHULA",
            font_size=34,
            bold=True,
            color=(0.25, 0.85, 0.50, 1),
            size_hint_y=None,
            height=60
        )

        content.add_widget(title)

        subtitle = Label(
            text="Business Overview",
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=45
        )

        content.add_widget(subtitle)

        stats = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None,
            height=190
        )

        statistics = [
            ("Total Sales", "R 0.00"),
            ("Expenses", "R 0.00"),
            ("Estimated Profit", "R 0.00"),
            ("Products", "0")
        ]

        for name, value in statistics:

            card = BoxLayout(
                orientation="vertical",
                padding=10
            )

            card.add_widget(
                Label(
                    text=name,
                    font_size=14
                )
            )

            card.add_widget(
                Label(
                    text=value,
                    font_size=22,
                    bold=True,
                    color=(0.25, 0.85, 0.50, 1)
                )
            )

            stats.add_widget(card)

        content.add_widget(stats)

        actions_title = Label(
            text="Quick Actions",
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=50
        )

        content.add_widget(actions_title)

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

    def handle_action(self, button):
        print(f"Selected: {button.text}")

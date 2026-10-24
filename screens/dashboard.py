
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

from services.reports_service import get_financial_report


# -----------------------------------------
# KHULA COLOUR THEME
# -----------------------------------------

BACKGROUND = (0.06, 0.10, 0.08, 1)
CARD_BACKGROUND = (0.11, 0.18, 0.14, 1)
GREEN = (0.25, 0.85, 0.50, 1)
BUTTON_GREEN = (0.12, 0.48, 0.28, 1)
WHITE = (1, 1, 1, 1)
MUTED = (0.68, 0.78, 0.71, 1)


# -----------------------------------------
# ROUNDED CARD COMPONENT
# -----------------------------------------

class RoundedCard(BoxLayout):

    def __init__(self, bg_color=CARD_BACKGROUND, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*bg_color)

            self.background_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

    def update_background(self, *args):
        self.background_rect.pos = self.pos
        self.background_rect.size = self.size


# -----------------------------------------
# DASHBOARD SCREEN
# -----------------------------------------

class DashboardScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.stat_labels = {}

        # Main background
        with self.canvas.before:
            Color(*BACKGROUND)

            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[0]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # Scrollable dashboard
        scroll = ScrollView(
            do_scroll_x=False
        )

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=18,
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # ---------------------------------
        # APPLICATION HEADER
        # ---------------------------------

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=105,
            spacing=5
        )

        title = Label(
            text="khula.",
            font_size=40,
            bold=True,
            color=GREEN,
            halign="left"
        )

        title.bind(
            size=lambda instance, size:
            setattr(instance, "text_size", size)
        )

        subtitle = Label(
            text="Your business, growing.",
            font_size=15,
            color=MUTED,
            halign="left"
        )

        subtitle.bind(
            size=lambda instance, size:
            setattr(instance, "text_size", size)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        content.add_widget(header)

        # ---------------------------------
        # BUSINESS OVERVIEW
        # ---------------------------------

        overview_title = Label(
            text="Business Overview",
            font_size=23,
            bold=True,
            color=WHITE,
            halign="left",
            size_hint_y=None,
            height=45
        )

        overview_title.bind(
            size=lambda instance, size:
            setattr(instance, "text_size", size)
        )

        content.add_widget(overview_title)

        overview_subtitle = Label(
            text="Your business at a glance",
            font_size=14,
            color=MUTED,
            halign="left",
            size_hint_y=None,
            height=25
        )

        overview_subtitle.bind(
            size=lambda instance, size:
            setattr(instance, "text_size", size)
        )

        content.add_widget(overview_subtitle)

        # ---------------------------------
        # STATISTICS GRID
        # ---------------------------------

        stats = GridLayout(
            cols=2,
            spacing=12,
            size_hint_y=None,
            height=220
        )

        statistics = [
            ("Total Sales", "R 0.00"),
            ("Expenses", "R 0.00"),
            ("Est. Balance", "R 0.00"),
            ("Products", "0")
        ]

        for name, value in statistics:

            card = RoundedCard(
                orientation="vertical",
                padding=12,
                spacing=8
            )

            name_label = Label(
                text=name,
                font_size=13,
                color=MUTED,
                halign="left"
            )

            name_label.bind(
                size=lambda instance, size:
                setattr(instance, "text_size", size)
            )

            value_label = Label(
                text=value,
                font_size=22,
                bold=True,
                color=WHITE,
                halign="left"
            )

            value_label.bind(
                size=lambda instance, size:
                setattr(instance, "text_size", size)
            )

            self.stat_labels[name] = value_label

            card.add_widget(name_label)
            card.add_widget(value_label)

            stats.add_widget(card)

        content.add_widget(stats)

        # ---------------------------------
        # QUICK ACTIONS
        # ---------------------------------

        actions_title = Label(
            text="Quick Actions",
            font_size=23,
            bold=True,
            color=WHITE,
            halign="left",
            size_hint_y=None,
            height=45
        )

        actions_title.bind(
            size=lambda instance, size:
            setattr(instance, "text_size", size)
        )

        content.add_widget(actions_title)

        actions = GridLayout(
            cols=2,
            spacing=12,
            size_hint_y=None,
            height=180
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
                font_size=16,
                bold=True,
                color=WHITE,
                background_normal="",
                background_color=BUTTON_GREEN
            )

            button.bind(
                on_press=self.handle_action
            )

            actions.add_widget(button)

        content.add_widget(actions)

        # ---------------------------------
        # FOOTER
        # ---------------------------------

        footer = Label(
            text="Khula | Empowering local businesses",
            font_size=12,
            color=MUTED,
            size_hint_y=None,
            height=45
        )

        content.add_widget(footer)

        scroll.add_widget(content)
        self.add_widget(scroll)

        # Load live database values
        self.refresh_statistics()

    # -------------------------------------
    # UPDATE BACKGROUND
    # -------------------------------------

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # -------------------------------------
    # REFRESH LIVE STATISTICS
    # -------------------------------------

    def refresh_statistics(self):

        report = get_financial_report()

        self.stat_labels["Total Sales"].text = (
            f"R {report['total_sales']:.2f}"
        )

        self.stat_labels["Expenses"].text = (
            f"R {report['total_expenses']:.2f}"
        )

        self.stat_labels["Est. Balance"].text = (
            f"R {report['estimated_balance']:.2f}"
        )

        self.stat_labels["Products"].text = (
            str(report["product_count"])
        )

    # -------------------------------------
    # DASHBOARD NAVIGATION
    # -------------------------------------

    def handle_action(self, button):
        print(f"Selected: {button.text}")

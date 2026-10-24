
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

from services.reports_service import get_financial_report


# -----------------------------------------
# KHULA DARK GREEN THEME
# -----------------------------------------

BACKGROUND = (0.06, 0.10, 0.08, 1)
CARD_BACKGROUND = (0.11, 0.18, 0.14, 1)
GREEN = (0.25, 0.85, 0.50, 1)
BUTTON_GREEN = (0.12, 0.48, 0.28, 1)
WHITE = (1, 1, 1, 1)
MUTED = (0.68, 0.78, 0.71, 1)


# -----------------------------------------
# ROUNDED REPORT CARD
# -----------------------------------------

class ReportCard(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*CARD_BACKGROUND)

            self.background_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[14]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

    def update_background(self, *args):
        self.background_rect.pos = self.pos
        self.background_rect.size = self.size


# -----------------------------------------
# FINANCIAL REPORTS SCREEN
# -----------------------------------------

class ReportsScreen(BoxLayout):

    def __init__(self, go_back=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=12,
            **kwargs
        )

        self.go_back = go_back

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

        # ---------------------------------
        # HEADER
        # ---------------------------------

        header = BoxLayout(
            size_hint_y=None,
            height=60,
            spacing=10
        )

        back_button = Button(
            text="< Back",
            size_hint_x=0.25,
            background_normal="",
            background_color=BUTTON_GREEN,
            color=WHITE
        )

        back_button.bind(on_press=self.back)
        header.add_widget(back_button)

        header.add_widget(Label(
            text="Financial Reports",
            bold=True,
            font_size=23,
            color=WHITE
        ))

        self.add_widget(header)

        # ---------------------------------
        # SUBTITLE
        # ---------------------------------

        subtitle = Label(
            text="Your business performance at a glance",
            font_size=14,
            color=MUTED,
            size_hint_y=None,
            height=35
        )

        self.add_widget(subtitle)

        # ---------------------------------
        # SCROLLABLE REPORT AREA
        # ---------------------------------

        scroll = ScrollView(
            do_scroll_x=False
        )

        self.report_layout = GridLayout(
            cols=2,
            spacing=12,
            padding=5,
            size_hint_y=None
        )

        self.report_layout.bind(
            minimum_height=self.report_layout.setter("height")
        )

        scroll.add_widget(self.report_layout)
        self.add_widget(scroll)

        # ---------------------------------
        # REFRESH BUTTON
        # ---------------------------------

        refresh_button = Button(
            text="Refresh Financial Report",
            bold=True,
            font_size=16,
            color=WHITE,
            background_normal="",
            background_color=BUTTON_GREEN,
            size_hint_y=None,
            height=55
        )

        refresh_button.bind(
            on_press=lambda instance: self.refresh_report()
        )

        self.add_widget(refresh_button)

        # Load report values
        self.refresh_report()

    # -------------------------------------
    # UPDATE BACKGROUND
    # -------------------------------------

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # -------------------------------------
    # CREATE FINANCIAL CARD
    # -------------------------------------

    def add_report_item(self, title, value):

        item = ReportCard(
            orientation="vertical",
            size_hint_y=None,
            height=105,
            padding=10,
            spacing=8
        )

        title_label = Label(
            text=title,
            font_size=13,
            color=MUTED,
            halign="center",
            valign="middle"
        )

        title_label.bind(
            size=lambda widget, size:
            setattr(widget, "text_size", size)
        )

        value_label = Label(
            text=value,
            font_size=20,
            bold=True,
            color=GREEN,
            halign="center",
            valign="middle"
        )

        value_label.bind(
            size=lambda widget, size:
            setattr(widget, "text_size", size)
        )

        item.add_widget(title_label)
        item.add_widget(value_label)

        self.report_layout.add_widget(item)

    # -------------------------------------
    # REFRESH FINANCIAL REPORT
    # -------------------------------------

    def refresh_report(self):

        report = get_financial_report()

        self.report_layout.clear_widgets()

        # Sales
        self.add_report_item(
            "Total Sales Revenue",
            f"R {report['total_sales']:.2f}"
        )

        self.add_report_item(
            "Sales Transactions",
            str(report["sales_count"])
        )

        # Expenses
        self.add_report_item(
            "Total Business Expenses",
            f"R {report['total_expenses']:.2f}"
        )

        self.add_report_item(
            "Recorded Expenses",
            str(report["expense_count"])
        )

        # Estimated balance
        self.add_report_item(
            "Estimated Balance",
            f"R {report['estimated_balance']:.2f}"
        )

        # Inventory
        self.add_report_item(
            "Inventory Value\nat Selling Price",
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

        # ---------------------------------
        # FINANCIAL EXPLANATION
        # ---------------------------------

        note_card = ReportCard(
            orientation="vertical",
            size_hint_y=None,
            height=100,
            padding=12,
            spacing=5
        )

        note_title = Label(
            text="Understanding Your Figures",
            font_size=15,
            bold=True,
            color=GREEN
        )

        note_text = Label(
            text=(
                "Estimated balance = sales - expenses.\n"
                "This is not accounting profit.\n"
                "Inventory value uses selling prices."
            ),
            font_size=12,
            color=MUTED,
            halign="center",
            valign="middle"
        )

        note_text.bind(
            size=lambda widget, size:
            setattr(widget, "text_size", size)
        )

        note_card.add_widget(note_title)
        note_card.add_widget(note_text)

        # Make the note span both columns
        self.report_layout.add_widget(note_card)
        self.report_layout.add_widget(
            Label(
                text="",
                size_hint_y=None,
                height=1
            )
        )

    # -------------------------------------
    # BACK TO DASHBOARD
    # -------------------------------------

    def back(self, instance):
        if self.go_back:
            self.go_back()

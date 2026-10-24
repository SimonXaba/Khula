
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle

from services.inventory_service import get_all_products
from services.sales_service import (
    record_sale,
    get_all_sales,
    get_sales_summary
)


# -----------------------------------------
# KHULA DARK GREEN THEME
# -----------------------------------------

BACKGROUND = (0.06, 0.10, 0.08, 1)
CARD_BACKGROUND = (0.11, 0.18, 0.14, 1)
INPUT_BACKGROUND = (0.14, 0.22, 0.17, 1)
GREEN = (0.25, 0.85, 0.50, 1)
BUTTON_GREEN = (0.12, 0.48, 0.28, 1)
WHITE = (1, 1, 1, 1)
MUTED = (0.68, 0.78, 0.71, 1)


# -----------------------------------------
# ROUNDED CARD COMPONENT
# -----------------------------------------

class SalesCard(BoxLayout):

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
# SALES MANAGEMENT SCREEN
# -----------------------------------------

class SalesScreen(BoxLayout):

    def __init__(self, go_back=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=12,
            **kwargs
        )

        self.go_back = go_back
        self.products = {}

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

        title = Label(
            text="Sales Management",
            bold=True,
            font_size=22,
            color=WHITE
        )

        header.add_widget(title)
        self.add_widget(header)

        # ---------------------------------
        # SALES SUMMARY
        # ---------------------------------

        summary_card = SalesCard(
            orientation="vertical",
            padding=12,
            size_hint_y=None,
            height=75
        )

        self.summary_label = Label(
            text="",
            font_size=16,
            bold=True,
            color=GREEN
        )

        summary_card.add_widget(self.summary_label)
        self.add_widget(summary_card)

        # ---------------------------------
        # RECORD SALE FORM
        # ---------------------------------

        form_title = Label(
            text="Record New Sale",
            font_size=20,
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=40
        )

        self.add_widget(form_title)

        self.product_spinner = Spinner(
            text="Select Product",
            values=[],
            size_hint_y=None,
            height=50,
            background_normal="",
            background_color=INPUT_BACKGROUND,
            color=WHITE,
            font_size=15
        )

        self.product_spinner.bind(
            text=self.update_total
        )

        self.add_widget(self.product_spinner)

        self.quantity_input = TextInput(
            hint_text="Quantity to sell",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=48,
            background_normal="",
            background_active="",
            background_color=INPUT_BACKGROUND,
            foreground_color=WHITE,
            hint_text_color=MUTED,
            cursor_color=GREEN,
            padding=[12, 12]
        )

        self.quantity_input.bind(
            text=self.update_total
        )

        self.add_widget(self.quantity_input)

        # ---------------------------------
        # LIVE SALE TOTAL
        # ---------------------------------

        total_card = SalesCard(
            orientation="vertical",
            padding=10,
            size_hint_y=None,
            height=70
        )

        self.total_label = Label(
            text="Total: R 0.00",
            bold=True,
            font_size=24,
            color=GREEN
        )

        total_card.add_widget(self.total_label)
        self.add_widget(total_card)

        # ---------------------------------
        # RECORD SALE BUTTON
        # ---------------------------------

        sale_button = Button(
            text="Record Sale",
            bold=True,
            font_size=17,
            color=WHITE,
            background_normal="",
            background_color=BUTTON_GREEN,
            size_hint_y=None,
            height=55
        )

        sale_button.bind(
            on_press=self.save_sale
        )

        self.add_widget(sale_button)

        # ---------------------------------
        # SALES HISTORY
        # ---------------------------------

        history_title = Label(
            text="Recent Sales",
            bold=True,
            font_size=20,
            color=WHITE,
            size_hint_y=None,
            height=40
        )

        self.add_widget(history_title)

        self.sales_list = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )

        self.sales_list.bind(
            minimum_height=self.sales_list.setter("height")
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        scroll.add_widget(self.sales_list)
        self.add_widget(scroll)

        # Load existing data
        self.refresh_data()

    # -------------------------------------
    # UPDATE BACKGROUND
    # -------------------------------------

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # -------------------------------------
    # POPUP MESSAGE
    # -------------------------------------

    def show_message(self, message):
        Popup(
            title="Khula",
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()

    # -------------------------------------
    # REFRESH SALES DATA
    # -------------------------------------

    def refresh_data(self):

        products = get_all_products()

        self.products = {
            f"{p['name']} (ID: {p['id']})": p
            for p in products
            if p["quantity"] > 0
        }

        self.product_spinner.values = list(
            self.products.keys()
        )

        if self.product_spinner.text not in self.products:
            self.product_spinner.text = "Select Product"

        summary = get_sales_summary()

        self.summary_label.text = (
            f"Transactions: {summary['transactions']}\n"
            f"Revenue: R {summary['revenue']:.2f}"
        )

        self.sales_list.clear_widgets()

        sales = get_all_sales()

        if not sales:
            empty_label = Label(
                text="No sales recorded yet.",
                color=MUTED,
                size_hint_y=None,
                height=60
            )

            self.sales_list.add_widget(empty_label)

        for sale in sales:

            row = SalesCard(
                orientation="vertical",
                size_hint_y=None,
                height=75,
                padding=12,
                spacing=5
            )

            product_label = Label(
                text=(
                    f"{sale['product']}  |  "
                    f"Qty: {sale['quantity']}"
                ),
                bold=True,
                font_size=15,
                color=WHITE,
                halign="left"
            )

            product_label.bind(
                size=lambda widget, size:
                setattr(widget, "text_size", size)
            )

            amount_label = Label(
                text=f"R {sale['total']:.2f}",
                font_size=16,
                bold=True,
                color=GREEN,
                halign="left"
            )

            amount_label.bind(
                size=lambda widget, size:
                setattr(widget, "text_size", size)
            )

            row.add_widget(product_label)
            row.add_widget(amount_label)

            self.sales_list.add_widget(row)

        self.update_total()

    # -------------------------------------
    # CALCULATE LIVE TOTAL
    # -------------------------------------

    def update_total(self, *args):

        selected = self.product_spinner.text

        if selected not in self.products:
            self.total_label.text = "Total: R 0.00"
            return

        try:
            quantity = int(self.quantity_input.text)
            price = self.products[selected]["price"]

            if quantity <= 0:
                self.total_label.text = "Total: R 0.00"
                return

            total = quantity * price

            self.total_label.text = (
                f"Total: R {total:.2f}"
            )

        except ValueError:
            self.total_label.text = "Total: R 0.00"

    # -------------------------------------
    # RECORD SALE
    # -------------------------------------

    def save_sale(self, instance):

        selected = self.product_spinner.text

        if selected not in self.products:
            self.show_message(
                "Please select a product."
            )
            return

        try:
            quantity = int(self.quantity_input.text)

            product = self.products[selected]

            result = record_sale(
                product["id"],
                quantity
            )

            self.quantity_input.text = ""

            self.refresh_data()

            self.show_message(
                f"Sale recorded successfully!\n"
                f"Product: {result['product']}\n"
                f"Total: R {result['total']:.2f}"
            )

        except ValueError as error:
            self.show_message(str(error))

    # -------------------------------------
    # BACK TO DASHBOARD
    # -------------------------------------

    def back(self, instance):
        if self.go_back:
            self.go_back()

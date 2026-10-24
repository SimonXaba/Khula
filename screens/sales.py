
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from services.inventory_service import get_all_products
from services.sales_service import (
    record_sale,
    get_all_sales,
    get_sales_summary
)


class SalesScreen(BoxLayout):

    def __init__(self, go_back=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        self.go_back = go_back
        self.products = {}

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
            text="Sales Management",
            bold=True,
            font_size=20
        ))
        self.add_widget(header)

        self.summary_label = Label(
            text="",
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.summary_label)

        self.product_spinner = Spinner(
            text="Select Product",
            values=[],
            size_hint_y=None,
            height=48
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
            height=45
        )
        self.quantity_input.bind(
            text=self.update_total
        )
        self.add_widget(self.quantity_input)

        self.total_label = Label(
            text="Total: R 0.00",
            bold=True,
            font_size=22,
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.total_label)

        sale_button = Button(
            text="Record Sale",
            background_normal="",
            background_color=(0.12, 0.65, 0.35, 1),
            size_hint_y=None,
            height=50
        )
        sale_button.bind(on_press=self.save_sale)
        self.add_widget(sale_button)

        self.add_widget(Label(
            text="Recent Sales",
            bold=True,
            size_hint_y=None,
            height=35
        ))

        self.sales_list = GridLayout(
            cols=1,
            spacing=8,
            size_hint_y=None
        )
        self.sales_list.bind(
            minimum_height=self.sales_list.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.sales_list)
        self.add_widget(scroll)

        self.refresh_data()

    def show_message(self, message):
        Popup(
            title="Khula",
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()

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
            f"Transactions: {summary['transactions']}  |  "
            f"Revenue: R {summary['revenue']:.2f}"
        )

        self.sales_list.clear_widgets()

        for sale in get_all_sales():
            label = Label(
                text=(
                    f"{sale['product']}  |  "
                    f"Qty: {sale['quantity']}  |  "
                    f"R {sale['total']:.2f}"
                ),
                size_hint_y=None,
                height=45
            )
            self.sales_list.add_widget(label)

        self.update_total()

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
            self.total_label.text = f"Total: R {total:.2f}"

        except ValueError:
            self.total_label.text = "Total: R 0.00"

    def save_sale(self, instance):
        selected = self.product_spinner.text

        if selected not in self.products:
            self.show_message("Please select a product.")
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

    def back(self, instance):
        if self.go_back:
            self.go_back()

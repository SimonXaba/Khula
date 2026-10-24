
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from services.inventory_service import (
    add_product,
    get_all_products,
    update_product,
    delete_product,
    get_inventory_summary
)


class InventoryScreen(BoxLayout):

    def __init__(self, go_back=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        self.go_back = go_back
        self.selected_product_id = None

        header = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=10
        )

        back_button = Button(
            text="< Back",
            size_hint_x=0.3
        )
        back_button.bind(on_press=self.back)

        header.add_widget(back_button)
        header.add_widget(Label(
            text="Inventory Management",
            bold=True,
            font_size=20
        ))
        self.add_widget(header)

        self.summary_label = Label(
            text="",
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.summary_label)

        self.name_input = TextInput(
            hint_text="Product name",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.name_input)

        self.price_input = TextInput(
            hint_text="Price (R)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.price_input)

        self.quantity_input = TextInput(
            hint_text="Quantity",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.quantity_input)

        actions = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=8
        )

        save_button = Button(
            text="Save Product",
            background_normal="",
            background_color=(0.12, 0.65, 0.35, 1)
        )
        save_button.bind(on_press=self.save_product)

        clear_button = Button(text="Clear")
        clear_button.bind(on_press=self.clear_form)

        actions.add_widget(save_button)
        actions.add_widget(clear_button)
        self.add_widget(actions)

        self.product_list = GridLayout(
            cols=1,
            spacing=8,
            size_hint_y=None
        )
        self.product_list.bind(
            minimum_height=self.product_list.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.product_list)
        self.add_widget(scroll)

        self.refresh_products()

    def show_message(self, message):
        popup = Popup(
            title="Khula",
            content=Label(text=message),
            size_hint=(0.85, 0.3)
        )
        popup.open()

    def save_product(self, instance):
        try:
            name = self.name_input.text.strip()
            price = float(self.price_input.text)
            quantity = int(self.quantity_input.text)

            if self.selected_product_id is None:
                add_product(name, price, quantity)
                message = "Product added successfully!"
            else:
                updated = update_product(
                    self.selected_product_id,
                    name,
                    price,
                    quantity
                )
                message = (
                    "Product updated successfully!"
                    if updated else "Product not found."
                )

            self.clear_form(None)
            self.refresh_products()
            self.show_message(message)

        except (ValueError, OverflowError) as error:
            self.show_message(
                f"Please check your input.\n{error}"
            )

    def refresh_products(self):
        self.product_list.clear_widgets()

        summary = get_inventory_summary()
        self.summary_label.text = (
            f"Products: {summary['total_products']}    "
            f"Stock Units: {summary['total_units']}"
        )

        for product in get_all_products():
            row = BoxLayout(
                size_hint_y=None,
                height=65,
                spacing=5
            )

            details = Label(
                text=(
                    f"{product['name']}\n"
                    f"R {product['price']:.2f} | "
                    f"Qty: {product['quantity']}"
                ),
                halign="left"
            )
            details.bind(
                size=lambda widget, size:
                    setattr(widget, "text_size", size)
            )

            edit_button = Button(
                text="Edit",
                size_hint_x=0.25
            )
            edit_button.bind(
                on_press=lambda btn, p=product:
                    self.edit_product(p)
            )

            delete_button = Button(
                text="Delete",
                size_hint_x=0.25
            )
            delete_button.bind(
                on_press=lambda btn, pid=product["id"]:
                    self.confirm_delete(pid)
            )

            row.add_widget(details)
            row.add_widget(edit_button)
            row.add_widget(delete_button)

            self.product_list.add_widget(row)

    def edit_product(self, product):
        self.selected_product_id = product["id"]
        self.name_input.text = product["name"]
        self.price_input.text = str(product["price"])
        self.quantity_input.text = str(product["quantity"])

    def confirm_delete(self, product_id):
        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        layout.add_widget(Label(
            text="Delete this product?"
        ))

        buttons = BoxLayout(
            size_hint_y=None,
            height=45,
            spacing=10
        )

        popup = Popup(
            title="Confirm Delete",
            content=layout,
            size_hint=(0.85, 0.3)
        )

        cancel = Button(text="Cancel")
        cancel.bind(on_press=popup.dismiss)

        confirm = Button(text="Delete")
        confirm.bind(
            on_press=lambda btn:
                self.remove_product(product_id, popup)
        )

        buttons.add_widget(cancel)
        buttons.add_widget(confirm)
        layout.add_widget(buttons)
        popup.open()

    def remove_product(self, product_id, popup):
        popup.dismiss()

        try:
            deleted = delete_product(product_id)

            if deleted:
                if self.selected_product_id == product_id:
                    self.clear_form(None)
                self.refresh_products()
                self.show_message("Product deleted!")
            else:
                self.show_message("Product not found.")

        except ValueError as error:
            self.show_message(str(error))

    def clear_form(self, instance):
        self.selected_product_id = None
        self.name_input.text = ""
        self.price_input.text = ""
        self.quantity_input.text = ""

    def back(self, instance):
        if self.go_back:
            self.go_back()

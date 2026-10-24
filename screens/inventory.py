
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle

from services.inventory_service import (
    add_product,
    get_all_products,
    update_product,
    delete_product,
    get_inventory_summary
)


# -----------------------------------------
# KHULA DARK GREEN THEME
# -----------------------------------------

BACKGROUND = (0.06, 0.10, 0.08, 1)
CARD_BACKGROUND = (0.11, 0.18, 0.14, 1)
INPUT_BACKGROUND = (0.14, 0.22, 0.17, 1)
GREEN = (0.25, 0.85, 0.50, 1)
BUTTON_GREEN = (0.12, 0.48, 0.28, 1)
DANGER = (0.65, 0.20, 0.20, 1)
WHITE = (1, 1, 1, 1)
MUTED = (0.68, 0.78, 0.71, 1)


# -----------------------------------------
# ROUNDED CARD
# -----------------------------------------

class InventoryCard(BoxLayout):

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
# INVENTORY MANAGEMENT SCREEN
# -----------------------------------------

class InventoryScreen(BoxLayout):

    def __init__(self, go_back=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=12,
            **kwargs
        )

        self.go_back = go_back
        self.selected_product_id = None

        # Screen background
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
            text="Inventory",
            bold=True,
            font_size=25,
            color=WHITE
        ))

        self.add_widget(header)

        # ---------------------------------
        # INVENTORY SUMMARY
        # ---------------------------------

        summary_card = InventoryCard(
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
        # PRODUCT FORM
        # ---------------------------------

        self.add_widget(Label(
            text="Product Details",
            font_size=19,
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=35
        ))

        self.name_input = TextInput(
            hint_text="Product name",
            multiline=False,
            background_normal="",
            background_active="",
            background_color=INPUT_BACKGROUND,
            foreground_color=WHITE,
            hint_text_color=MUTED,
            cursor_color=GREEN,
            padding=[12, 12],
            size_hint_y=None,
            height=48
        )

        self.add_widget(self.name_input)

        self.price_input = TextInput(
            hint_text="Price (R)",
            multiline=False,
            input_filter="float",
            background_normal="",
            background_active="",
            background_color=INPUT_BACKGROUND,
            foreground_color=WHITE,
            hint_text_color=MUTED,
            cursor_color=GREEN,
            padding=[12, 12],
            size_hint_y=None,
            height=48
        )

        self.add_widget(self.price_input)

        self.quantity_input = TextInput(
            hint_text="Quantity",
            multiline=False,
            input_filter="int",
            background_normal="",
            background_active="",
            background_color=INPUT_BACKGROUND,
            foreground_color=WHITE,
            hint_text_color=MUTED,
            cursor_color=GREEN,
            padding=[12, 12],
            size_hint_y=None,
            height=48
        )

        self.add_widget(self.quantity_input)

        # ---------------------------------
        # FORM ACTIONS
        # ---------------------------------

        actions = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )

        save_button = Button(
            text="Save Product",
            bold=True,
            background_normal="",
            background_color=BUTTON_GREEN,
            color=WHITE
        )

        save_button.bind(on_press=self.save_product)

        clear_button = Button(
            text="Clear",
            background_normal="",
            background_color=CARD_BACKGROUND,
            color=WHITE
        )

        clear_button.bind(on_press=self.clear_form)

        actions.add_widget(save_button)
        actions.add_widget(clear_button)

        self.add_widget(actions)

        # ---------------------------------
        # PRODUCT LIST
        # ---------------------------------

        self.add_widget(Label(
            text="Your Products",
            font_size=20,
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=40
        ))

        self.product_list = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )

        self.product_list.bind(
            minimum_height=self.product_list.setter("height")
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        scroll.add_widget(self.product_list)
        self.add_widget(scroll)

        self.refresh_products()

    # -------------------------------------
    # UPDATE BACKGROUND
    # -------------------------------------

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # -------------------------------------
    # SHOW POPUP MESSAGE
    # -------------------------------------

    def show_message(self, message):
        popup = Popup(
            title="Khula",
            content=Label(text=message),
            size_hint=(0.85, 0.3)
        )
        popup.open()

    # -------------------------------------
    # SAVE OR UPDATE PRODUCT
    # -------------------------------------

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

    # -------------------------------------
    # REFRESH INVENTORY
    # -------------------------------------

    def refresh_products(self):
        self.product_list.clear_widgets()

        summary = get_inventory_summary()

        self.summary_label.text = (
            f"Products: {summary['total_products']}    "
            f"Stock Units: {summary['total_units']}"
        )

        products = get_all_products()

        for product in products:

            row = InventoryCard(
                orientation="horizontal",
                size_hint_y=None,
                height=85,
                padding=10,
                spacing=8
            )

            details = Label(
                text=(
                    f"{product['name']}\n"
                    f"R {product['price']:.2f}  |  "
                    f"Qty: {product['quantity']}"
                ),
                color=WHITE,
                halign="left",
                font_size=14
            )

            details.bind(
                size=lambda widget, size:
                setattr(widget, "text_size", size)
            )

            edit_button = Button(
                text="Edit",
                size_hint_x=0.23,
                background_normal="",
                background_color=BUTTON_GREEN,
                color=WHITE
            )

            edit_button.bind(
                on_press=lambda btn, p=product:
                self.edit_product(p)
            )

            delete_button = Button(
                text="Delete",
                size_hint_x=0.25,
                background_normal="",
                background_color=DANGER,
                color=WHITE
            )

            delete_button.bind(
                on_press=lambda btn, pid=product["id"]:
                self.confirm_delete(pid)
            )

            row.add_widget(details)
            row.add_widget(edit_button)
            row.add_widget(delete_button)

            self.product_list.add_widget(row)

    # -------------------------------------
    # EDIT PRODUCT
    # -------------------------------------

    def edit_product(self, product):
        self.selected_product_id = product["id"]

        self.name_input.text = product["name"]
        self.price_input.text = str(product["price"])
        self.quantity_input.text = str(product["quantity"])

    # -------------------------------------
    # CONFIRM DELETE
    # -------------------------------------

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

    # -------------------------------------
    # DELETE PRODUCT
    # -------------------------------------

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

    # -------------------------------------
    # CLEAR FORM
    # -------------------------------------

    def clear_form(self, instance):
        self.selected_product_id = None

        self.name_input.text = ""
        self.price_input.text = ""
        self.quantity_input.text = ""

    # -------------------------------------
    # BACK TO DASHBOARD
    # -------------------------------------

    def back(self, instance):
        if self.go_back:
            self.go_back()

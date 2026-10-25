
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle

from services.expense_service import (
    add_expense,
    get_all_expenses,
    delete_expense,
    get_expense_summary
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
# ROUNDED EXPENSE CARD
# -----------------------------------------

class ExpenseCard(BoxLayout):

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
# EXPENSE MANAGEMENT SCREEN
# -----------------------------------------

class ExpensesScreen(BoxLayout):

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
            text="Expense Management",
            bold=True,
            font_size=22,
            color=WHITE
        ))

        self.add_widget(header)

        # ---------------------------------
        # EXPENSE SUMMARY
        # ---------------------------------

        summary_card = ExpenseCard(
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
        # EXPENSE FORM
        # ---------------------------------

        self.add_widget(Label(
            text="Add New Expense",
            font_size=20,
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=40
        ))

        self.description_input = TextInput(
            hint_text="Expense description",
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

        self.add_widget(self.description_input)

        self.amount_input = TextInput(
            hint_text="Amount (R)",
            input_filter="float",
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

        self.add_widget(self.amount_input)

        self.category_spinner = Spinner(
            text="Select Category",
            values=[
                "Transport",
                "Rent",
                "Electricity",
                "Stock Purchases",
                "Internet",
                "Marketing",
                "Other"
            ],
            size_hint_y=None,
            height=48,
            background_normal="",
            background_color=INPUT_BACKGROUND,
            color=WHITE,
            font_size=15
        )

        self.add_widget(self.category_spinner)

        # ---------------------------------
        # SAVE EXPENSE BUTTON
        # ---------------------------------

        save_button = Button(
            text="Save Expense",
            bold=True,
            font_size=17,
            color=WHITE,
            background_normal="",
            background_color=BUTTON_GREEN,
            size_hint_y=None,
            height=55
        )

        save_button.bind(
            on_press=self.save_expense
        )

        self.add_widget(save_button)

        # ---------------------------------
        # EXPENSE HISTORY
        # ---------------------------------

        self.add_widget(Label(
            text="Recent Expenses",
            bold=True,
            font_size=20,
            color=WHITE,
            size_hint_y=None,
            height=40
        ))

        self.expense_list = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )

        self.expense_list.bind(
            minimum_height=self.expense_list.setter("height")
        )

        scroll = ScrollView(
            do_scroll_x=False
        )

        scroll.add_widget(self.expense_list)
        self.add_widget(scroll)

        # Load saved expenses
        self.refresh_data()

    # -------------------------------------
    # UPDATE BACKGROUND
    # -------------------------------------

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # -------------------------------------
    # SHOW MESSAGE
    # -------------------------------------

    def show_message(self, message):
        Popup(
            title="Khula",
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()

    # -------------------------------------
    # SAVE EXPENSE
    # -------------------------------------

    def save_expense(self, instance):

        description = self.description_input.text.strip()
        amount = self.amount_input.text.strip()
        category = self.category_spinner.text

        if category == "Select Category":
            self.show_message(
                "Please select a category."
            )
            return

        try:
            add_expense(
                description,
                amount,
                category
            )

            self.description_input.text = ""
            self.amount_input.text = ""
            self.category_spinner.text = "Select Category"

            self.refresh_data()

            self.show_message(
                "Expense saved successfully!"
            )

        except ValueError as error:
            self.show_message(str(error))

    # -------------------------------------
    # REFRESH EXPENSE DATA
    # -------------------------------------

    def refresh_data(self):

        summary = get_expense_summary()

        self.summary_label.text = (
            f"Expenses: {summary['total_expenses']}\n"
            f"Total Spending: R {summary['total_spending']:.2f}"
        )

        self.expense_list.clear_widgets()

        expenses = get_all_expenses()

        if not expenses:
            self.expense_list.add_widget(Label(
                text="No expenses recorded yet.",
                color=MUTED,
                size_hint_y=None,
                height=60
            ))

        for expense in expenses:

            row = ExpenseCard(
                orientation="horizontal",
                size_hint_y=None,
                height=85,
                padding=10,
                spacing=8
            )

            details = Label(
                text=(
                    f"{expense['description']}\n"
                    f"{expense['category']}  |  "
                    f"R {expense['amount']:.2f}"
                ),
                color=WHITE,
                font_size=14,
                halign="left"
            )

            details.bind(
                size=lambda widget, size:
                setattr(widget, "text_size", size)
            )

            delete_button = Button(
                text="Delete",
                size_hint_x=0.25,
                background_normal="",
                background_color=DANGER,
                color=WHITE
            )

            delete_button.bind(
                on_press=lambda btn, eid=expense["id"]:
                self.confirm_delete(eid)
            )

            row.add_widget(details)
            row.add_widget(delete_button)

            self.expense_list.add_widget(row)

    # -------------------------------------
    # CONFIRM DELETE
    # -------------------------------------

    def confirm_delete(self, expense_id):

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        layout.add_widget(Label(
            text="Delete this expense?"
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

        cancel_button = Button(
            text="Cancel",
            background_normal="",
            background_color=BUTTON_GREEN
        )

        cancel_button.bind(
            on_press=popup.dismiss
        )

        delete_button = Button(
            text="Delete",
            background_normal="",
            background_color=DANGER
        )

        delete_button.bind(
            on_press=lambda btn:
            self.remove_expense(expense_id, popup)
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(delete_button)

        layout.add_widget(buttons)

        popup.open()

    # -------------------------------------
    # DELETE EXPENSE
    # -------------------------------------

    def remove_expense(self, expense_id, popup):

        popup.dismiss()

        if delete_expense(expense_id):
            self.refresh_data()

            self.show_message(
                "Expense deleted successfully!"
            )
        else:
            self.show_message(
                "Expense not found."
            )

    # -------------------------------------
    # BACK TO DASHBOARD
    # -------------------------------------

    def back(self, instance):
        if self.go_back:
            self.go_back()


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from services.expense_service import (
    add_expense,
    get_all_expenses,
    delete_expense,
    get_expense_summary
)


class ExpensesScreen(BoxLayout):

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
            text="Expense Management",
            bold=True,
            font_size=20
        ))
        self.add_widget(header)

        # Expense summary
        self.summary_label = Label(
            text="",
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.summary_label)

        # Expense description
        self.description_input = TextInput(
            hint_text="Expense description",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.description_input)

        # Expense amount
        self.amount_input = TextInput(
            hint_text="Amount (R)",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.amount_input)

        # Expense category
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
            height=45
        )
        self.add_widget(self.category_spinner)

        # Save expense button
        save_button = Button(
            text="Save Expense",
            background_normal="",
            background_color=(0.12, 0.65, 0.35, 1),
            size_hint_y=None,
            height=50
        )
        save_button.bind(on_press=self.save_expense)
        self.add_widget(save_button)

        # Expense history heading
        self.add_widget(Label(
            text="Recent Expenses",
            bold=True,
            size_hint_y=None,
            height=35
        ))

        # Scrollable expense list
        self.expense_list = GridLayout(
            cols=1,
            spacing=8,
            size_hint_y=None
        )
        self.expense_list.bind(
            minimum_height=self.expense_list.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.expense_list)
        self.add_widget(scroll)

        self.refresh_data()

    def show_message(self, message):
        Popup(
            title="Khula",
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()

    def save_expense(self, instance):
        description = self.description_input.text.strip()
        amount = self.amount_input.text.strip()
        category = self.category_spinner.text

        if category == "Select Category":
            self.show_message("Please select a category.")
            return

        try:
            add_expense(description, amount, category)

            self.description_input.text = ""
            self.amount_input.text = ""
            self.category_spinner.text = "Select Category"

            self.refresh_data()
            self.show_message("Expense saved successfully!")

        except ValueError as error:
            self.show_message(str(error))

    def refresh_data(self):
        summary = get_expense_summary()

        self.summary_label.text = (
            f"Expenses: {summary['total_expenses']}  |  "
            f"Total: R {summary['total_spending']:.2f}"
        )

        self.expense_list.clear_widgets()

        for expense in get_all_expenses():
            row = BoxLayout(
                size_hint_y=None,
                height=65,
                spacing=5
            )

            details = Label(
                text=(
                    f"{expense['description']}\n"
                    f"{expense['category']} | "
                    f"R {expense['amount']:.2f}"
                ),
                halign="left"
            )

            details.bind(
                size=lambda widget, size: setattr(
                    widget, "text_size", size
                )
            )

            delete_button = Button(
                text="Delete",
                size_hint_x=0.25
            )

            delete_button.bind(
                on_press=lambda btn, eid=expense["id"]:
                self.confirm_delete(eid)
            )

            row.add_widget(details)
            row.add_widget(delete_button)
            self.expense_list.add_widget(row)

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

        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=popup.dismiss)

        delete_button = Button(text="Delete")
        delete_button.bind(
            on_press=lambda btn:
            self.remove_expense(expense_id, popup)
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(delete_button)
        layout.add_widget(buttons)

        popup.open()

    def remove_expense(self, expense_id, popup):
        popup.dismiss()

        if delete_expense(expense_id):
            self.refresh_data()
            self.show_message("Expense deleted successfully!")
        else:
            self.show_message("Expense not found.")

    def back(self, instance):
        if self.go_back:
            self.go_back()


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

# Set the application window size
Window.size = (400, 600)
Window.clearcolor = (0.06, 0.10, 0.09, 1)


class KhulaApp(App):
    def build(self):
        self.title = "Khula - Business Management"

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="KHULA",
            font_size=42,
            bold=True,
            color=(0.25, 0.85, 0.50, 1)
        )

        subtitle = Label(
            text="Your Business. Your Growth. Your Future!",
            font_size=15,
            color=(1, 1, 1, 1)
        )

        start_button = Button(
            text="Get Started",
            font_size=20,
            size_hint=(1, 0.2),
            background_normal="",
            background_color=(0.12, 0.65, 0.35, 1)
        )

        start_button.bind(on_press=self.on_get_started)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_button)

        return layout

    def on_get_started(self, instance):
        print("Welcome to Khula!")


if __name__ == "__main__":
    KhulaApp().run()

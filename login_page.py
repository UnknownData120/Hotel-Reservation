import flet as ft
import os
from database import authenticate_user, register_user  # Import database functions

class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__("/")
        self.page = page

        # Login Fields
        self.username_field = ft.TextField(label="Username")
        self.password_field = ft.TextField(label="Password", password=True)
        self.status_text = ft.Text("", color="red")
        self.login_button = ft.ElevatedButton("Login", on_click=self.login_action)
        self.switch_to_register_button = ft.TextButton("Don't have an account? Register", on_click=self.show_register)

        # Register Fields (Initially Hidden)
        self.new_username_field = ft.TextField(label="New Username")
        self.new_password_field = ft.TextField(label="New Password", password=True)
        self.confirm_password_field = ft.TextField(label="Confirm Password", password=True)
        self.register_button = ft.ElevatedButton("Register", on_click=self.register_action)
        self.switch_to_login_button = ft.TextButton("Already have an account? Login", on_click=self.show_login)

        # Layout
        self.login_form = ft.Column(
            [
                ft.Text("Welcome to Hotel Reservation System", size=20, weight="bold"),
                self.username_field,
                self.password_field,
                self.login_button,
                self.switch_to_register_button,
                self.status_text
            ]
        )

        self.register_form = ft.Column(
            [
                ft.Text("Register a New Account", size=20, weight="bold"),
                self.new_username_field,
                self.new_password_field,
                self.confirm_password_field,
                self.register_button,
                self.switch_to_login_button,
                self.status_text
            ]
        )

        self.controls.append(self.login_form)

    def login_action(self, e):
        """Handles user login by checking the database."""
        username = self.username_field.value.strip()
        password = self.password_field.value.strip()

        if not username or not password:
            self.status_text.value = "Please enter both username and password."
            self.page.update()
            return

        # Direct admin login bypassing the database
        if username == "admin" and password == "admin123":
            self.page.on_login(username)  # Call the app's login handler
            return

        role = authenticate_user(username, password)
        if role == "admin" or role == "user":
            self.page.on_login(username)  # Call the app's login handler
        else:
            self.status_text.value = "Invalid username or password."
            self.page.update()

    def register_action(self, e):
        """Handles user registration."""
        username = self.new_username_field.value.strip()
        password = self.new_password_field.value.strip()
        confirm_password = self.confirm_password_field.value.strip()

        if not username or not password or not confirm_password:
            self.status_text.value = "All fields are required."
        elif password != confirm_password:
            self.status_text.value = "Passwords do not match."
        elif register_user(username, password):
            self.status_text.value = "Registration successful! Please log in."
            self.show_login(None)  # Switch back to login after registering
        else:
            self.status_text.value = "Username already exists."

        self.page.update()

    def show_register(self, e):
        """Switches to the Register form."""
        self.controls.clear()
        self.controls.append(self.register_form)
        self.page.update()

    def show_login(self, e):
        """Switches back to the Login form."""
        self.controls.clear()
        self.controls.append(self.login_form)
        self.page.update()

# Print the absolute path of the database for debugging
print(os.path.abspath("hotel_reservation.db"))

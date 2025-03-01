import flet as ft
from login_page import LoginPage
from admin_page import AdminPage
from user_page import UserPage

class HotelReservationApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hotel Reservation System"
        self.page.on_route_change = self.route_change
        self.page.on_login = self.handle_login  # Allow LoginPage to call this
        self.logged_in_user = None  # Store the username after login
        self.page.go("/")  # Start at login page

    def handle_login(self, username):
        """Handles login and navigates based on role."""
        self.logged_in_user = username
        if username == "admin":
            self.page.go("/admin")
        else:
            self.page.go("/user")

    def route_change(self, e):
        """Handles page transitions and ensures only one page is open at a time."""
        self.page.views.clear()

        if self.page.route == "/":
            login_page = LoginPage(self.page)
            self.page.views.append(login_page)
        elif self.page.route == "/admin":
            self.page.views.append(AdminPage(self.page))
        elif self.page.route == "/user":
            if self.logged_in_user:
                self.page.views.append(UserPage(self.page, self.logged_in_user))
            else:
                self.page.go("/")  # Redirect to login if no user is set

        self.page.update()

def main(page: ft.Page):
    HotelReservationApp(page)

ft.app(target=main)

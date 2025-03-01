import flet as ft
from hoteldb import remove_booking
import sqlite3
import functools

DB_FILE = "hotel_reservation.db"

class AdminPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__("/admin")
        self.page = page

        # Title
        title = ft.Text("Admin Panel - Manage Bookings", size=20, weight="bold")

        # Buttons: Refresh and Logout
        refresh_button = ft.ElevatedButton("Refresh", on_click=lambda e: self.refresh_bookings())
        logout_button = ft.ElevatedButton("Logout", on_click=self.logout_action, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE)
        button_row = ft.Row([refresh_button, logout_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Message when there are no bookings
        self.no_bookings_message = ft.Text("", size=16, italic=True, color=ft.colors.GREY)

        # Booking Table
        self.booking_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Time")),
                ft.DataColumn(ft.Text("Room")),
                ft.DataColumn(ft.Text("Action")),
            ],
            rows=[]  # Initialize empty table
        )

        # Layout
        self.controls.append(
            ft.Column([
                title,
                button_row,
                self.no_bookings_message,  # Display message here
                self.booking_table  # Display table below
            ], spacing=15)
        )

        self.refresh_bookings()  # Load bookings initially

    def refresh_bookings(self):
        """Loads the bookings into the table with proper formatting."""
        self.booking_table.rows.clear()  # ✅ Correct reference

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date_selected, time_selected, room FROM bookings")
        bookings = cursor.fetchall()
        conn.close()

        if not bookings:
            self.no_bookings_message.value = "No bookings found."
            self.booking_table.visible = False  # Hide table if empty
        else:
            self.no_bookings_message.value = ""  # Remove message
            self.booking_table.visible = True   # Show table
            for booking in bookings:
                booking_id, name, date, time, room = booking
                self.booking_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(booking_id))),
                            ft.DataCell(ft.Text(name)),
                            ft.DataCell(ft.Text(date)),
                            ft.DataCell(ft.Text(time)),
                            ft.DataCell(ft.Text(str(room))),
                            ft.DataCell(ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_500, tooltip="Remove Booking",
                                                      on_click=functools.partial(self.remove_booking, booking_id))),
                        ]
                    )
                )

        self.page.update()

    def remove_booking(self, booking_id, e=None):
        """Removes a booking and refreshes the table."""
        remove_booking(booking_id)
        self.refresh_bookings()  # Reload table after deletion

    def logout_action(self, e):
        """Logs out the admin and redirects to the login page."""
        self.page.go("/")

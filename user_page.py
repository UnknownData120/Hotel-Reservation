import flet as ft
from hoteldb import add_booking
import sqlite3
from datetime import date, timedelta

DB_FILE = "hotel_reservation.db"

class UserPage(ft.View):
    def __init__(self, page: ft.Page, username: str):
        super().__init__("/user")
        self.page = page
        self.username = username  

        # Input Fields
        self.name_field = ft.TextField(label="Name", value=username, read_only=True, width=200)

        # Date & Time Pickers
        today = date.today()
        date_options = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        time_options = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)]
        
        self.date_picker = ft.Dropdown(label="Select Date", options=[ft.dropdown.Option(d) for d in date_options], width=150)
        self.time_picker = ft.Dropdown(label="Select Time", options=[ft.dropdown.Option(t) for t in time_options], width=150)

        # Room Selection (Dropdown)
        self.room_picker = ft.Dropdown(
            label="Select Room",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 16)],  # Rooms 1-15
            width=150
        )

        # Status Text
        self.status_text = ft.Text("", color="blue")

        # Buttons
        book_button = ft.ElevatedButton("Book Room", on_click=self.book_room)
        refresh_button = ft.ElevatedButton("Refresh", on_click=lambda e: self.load_user_bookings())
        logout_button = ft.ElevatedButton("Logout", on_click=self.logout, bgcolor=ft.colors.RED)

        # Booking Table
        self.booking_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Time")),
                ft.DataColumn(ft.Text("Room")),
                ft.DataColumn(ft.Text("Cancel")),
            ],
            rows=[]
        )
        self.booking_table_container = ft.Container(
            content=ft.Column([self.booking_table], scroll="auto"),
            width=450,
            height=300,
        )

        # Layout: Top bar with Welcome & Logout button
        self.controls.append(
            ft.Row(
                [
                    ft.Text(f"User Panel - Welcome, {self.username}", size=20, weight="bold"),
                    logout_button  # Logout button on the top right
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

        # Left: Form, Right: Table
        self.controls.append(
            ft.Row(
                [
                    # FORM SECTION (Left)
                    ft.Column(
                        [
                            self.name_field,

                            # Date & Time Fields Side by Side
                            ft.Row([self.date_picker, self.time_picker], spacing=10),

                            self.room_picker,  # Dropdown instead of text field
                            ft.Row([book_button, refresh_button], spacing=10),
                            self.status_text,
                        ],
                        spacing=15,
                        width=350,
                    ),

                    # TABLE SECTION (Right)
                    self.booking_table_container
                ],
                spacing=50,
                alignment=ft.MainAxisAlignment.START
            )
        )

        self.load_user_bookings()

    def book_room(self, e):
        """Handles room booking."""
        name = self.name_field.value
        date_selected = self.date_picker.value
        time_selected = self.time_picker.value
        room_number = self.room_picker.value  # Now selected from dropdown

        if name and date_selected and time_selected and room_number:
            if add_booking(name, date_selected, time_selected, room_number):
                self.status_text.value = "Booking successful!"
            else:
                self.status_text.value = "Room is already booked."
        else:
            self.status_text.value = "All fields are required."
        
        self.load_user_bookings()
        self.page.update()

    def load_user_bookings(self):
        """Loads only the reservations of the logged-in user."""
        self.booking_table.rows.clear()

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date_selected, time_selected, room FROM bookings WHERE name=?", (self.username,))
        bookings = cursor.fetchall()
        conn.close()

        if not bookings:
            self.status_text.value = "You have no reservations."
            self.booking_table.visible = False
        else:
            self.status_text.value = ""
            self.booking_table.visible = True
            for booking in bookings:
                booking_id, date, time, room = booking
                self.booking_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(booking_id))),
                            ft.DataCell(ft.Text(date)),
                            ft.DataCell(ft.Text(time)),
                            ft.DataCell(ft.Text(str(room))),
                            ft.DataCell(
                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, bid=booking_id: self.remove_booking(bid))
                            ),
                        ]
                    )
                )

        self.page.update()

    def remove_booking(self, booking_id):
        """Removes a booking and refreshes the list."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()

        self.load_user_bookings()
        self.status_text.value = "Booking removed."
        self.page.update()

    def logout(self, e):
        """Handles user logout by redirecting to the login page."""
        self.page.go("/")

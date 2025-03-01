import sqlite3

def init_db():
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            room INTEGER NOT NULL UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'user'))
        )
    ''')
    
    conn.commit()
    conn.close()

def add_booking(name, date_selected, time_selected, room):
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()

    # Check if the room is already booked for the same date and time
    cursor.execute("""
        SELECT * FROM bookings 
        WHERE room = ? AND date_selected = ? AND time_selected = ?
    """, (room, date_selected, time_selected))

    existing_booking = cursor.fetchone()

    if existing_booking:
        conn.close()
        return False  # Room is already booked for this date and time

    # If no conflict, add the booking
    cursor.execute("""
        INSERT INTO bookings (name, date_selected, time_selected, room)
        VALUES (?, ?, ?, ?)
    """, (name, date_selected, time_selected, room))

    conn.commit()
    conn.close()
    return True  # Booking successful

def remove_booking(booking_id):
    """Deletes a specific booking based on its ID."""
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

def get_bookings():
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def get_booking_by_room(room):
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE room = ?", (room,))
    booking = cursor.fetchone()
    conn.close()
    return booking

def register_user(username, password, role):
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def authenticate_user(username, password):
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def make_admin():
    conn = sqlite3.connect("project/hotel_reservation.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?) ON CONFLICT(username) DO NOTHING", ('admin', 'admin123', 'admin'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def cancel_booking(room):
    conn = sqlite3.connect("hotel_reservation.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE room = ?", (room,))
    conn.commit()
    conn.close()
# Initialize database
init_db()


import sqlite3

DATABASE_NAME = "events.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            event_date TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL
                CHECK(capacity > 0)
        )
    """)

    # Registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            participant_name TEXT NOT NULL,
            email TEXT NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id),
            UNIQUE(event_id, email)
        )
    """)

    # Add sample events only when the database is empty
    cursor.execute("SELECT COUNT(*) FROM events")

    if cursor.fetchone()[0] == 0:
        sample_events = [
            (
                "Python Workshop",
                "Learn Python programming from the basics.",
                "2026-11-15",
                "Computer Lab",
                50
            ),
            (
                "Web Development Bootcamp",
                "Explore HTML, CSS, JavaScript and Flask.",
                "2026-11-20",
                "Seminar Hall",
                40
            ),
            (
                "AI and Machine Learning Seminar",
                "Introduction to AI and machine learning.",
                "2026-11-25",
                "Main Auditorium",
                100
            )
        ]

        cursor.executemany("""
            INSERT INTO events
            (title, description, event_date, location, capacity)
            VALUES (?, ?, ?, ?, ?)
        """, sample_events)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")

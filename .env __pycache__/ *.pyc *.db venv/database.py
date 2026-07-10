"""
Database Module

Creates and manages the SQLite attendance database.
"""

import sqlite3

import config


def create_database():
    """
    Creates attendance table if it does not exist.
    """

    connection = sqlite3.connect(
        config.DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_attendance(
    student_id: str,
    student_name: str,
    subject: str,
    date: str,
    status: str
):
    """
    Add an attendance record.
    """

    connection = sqlite3.connect(
        config.DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO attendance
        (
            student_id,
            student_name,
            subject,
            date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            student_name,
            subject,
            date,
            status
        )
    )

    connection.commit()
    connection.close()


def insert_demo_data():
    """
    Adds sample records for testing.
    """

    connection = sqlite3.connect(
        config.DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM attendance"
    )

    count = cursor.fetchone()[0]

    connection.close()

    # Avoid duplicate demo data
    if count > 0:
        return

    demo_records = [
        (
            "101",
            "Rahul",
            "Artificial Intelligence",
            "2026-07-01",
            "Present"
        ),
        (
            "101",
            "Rahul",
            "Database Systems",
            "2026-07-02",
            "Absent"
        ),
        (
            "102",
            "Priya",
            "Artificial Intelligence",
            "2026-07-01",
            "Present"
        ),
        (
            "103",
            "Amit",
            "Database Systems",
            "2026-07-02",
            "Present"
        )
    ]

    for record in demo_records:
        add_attendance(*record)


if __name__ == "__main__":
    create_database()
    insert_demo_data()

    print(
        "Attendance database initialized successfully."
    )

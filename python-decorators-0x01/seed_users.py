import sqlite3

conn = sqlite3.connect("users.db")  # creates file in this folder
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
"""
)

cursor.executemany(
    """
INSERT INTO users (name, email) VALUES (?, ?)
""",
    [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com"),
    ],
)

conn.commit()
conn.close()
exit()

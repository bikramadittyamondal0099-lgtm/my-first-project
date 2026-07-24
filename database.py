import sqlite3

conn = sqlite3.connect("history.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS execution_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line INTEGER,
    variable TEXT,
    value TEXT
)
""")

conn.commit()


def save(line, variable, value):
    cursor.execute(
        """
        INSERT INTO execution_log(line, variable, value)
        VALUES (?, ?, ?)
        """,
        (line, variable, str(value))
    )
    conn.commit()


def clear():
    cursor.execute("DELETE FROM execution_log")
    conn.commit()


def show_records():

    cursor.execute("SELECT * FROM execution_log")

    rows = cursor.fetchall()

    print("\nDatabase Records:\n")

    for row in rows:
        print(row)
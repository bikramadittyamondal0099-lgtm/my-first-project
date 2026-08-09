import sqlite3
import time

DATABASE_NAME = "trace.db"


class Database:

    def __init__(self, database_name=DATABASE_NAME):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    # =========================================================
    # CREATE TABLE
    # =========================================================

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS variable_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frame_id INTEGER NOT NULL,
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        """)

        self.conn.commit()

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):
        self.cursor.execute(
            "DELETE FROM variable_changes"
        )

        self.conn.commit()

    # =========================================================
    # SAVE CHANGE
    # =========================================================

    def save_change(
        self,
        frame_id,
        line_number,
        variable_name,
        old_value,
        new_value
    ):
        self.cursor.execute("""
            INSERT INTO variable_changes (
                frame_id,
                line_number,
                variable_name,
                old_value,
                new_value,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            frame_id,
            line_number,
            variable_name,
            old_value,
            str(new_value),
            time.time()
        ))

        self.conn.commit()

    # =========================================================
    # GET COMPLETE HISTORY
    # =========================================================

    def get_history(self):

        self.cursor.execute("""
            SELECT
                frame_id,
                line_number,
                variable_name,
                old_value,
                new_value,
                timestamp
            FROM variable_changes
            ORDER BY frame_id ASC, id ASC
        """)

        return self.cursor.fetchall()

    # =========================================================
    # GET FRAME
    # =========================================================

    def get_frame(self, frame_id):

        self.cursor.execute("""
            SELECT
                line_number,
                variable_name,
                old_value,
                new_value
            FROM variable_changes
            WHERE frame_id = ?
            ORDER BY id ASC
        """, (frame_id,))

        return self.cursor.fetchall()

    # =========================================================
    # GET STATE AT FRAME
    # =========================================================

    def get_current_state(self, frame_id):

        self.cursor.execute("""
            SELECT
                variable_name,
                new_value
            FROM variable_changes
            WHERE frame_id <= ?
            ORDER BY id ASC
        """, (frame_id,))

        rows = self.cursor.fetchall()

        state = {}

        for variable, value in rows:
            state[variable] = value

        return state

    # =========================================================
    # GET ALL VARIABLES
    # =========================================================

    def get_variables(self):

        self.cursor.execute("""
            SELECT DISTINCT variable_name
            FROM variable_changes
            ORDER BY variable_name
        """)

        rows = self.cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]

    # =========================================================
    # GET VARIABLE HISTORY
    # =========================================================

    def get_variable_history(self, variable_name):

        self.cursor.execute("""
            SELECT
                frame_id,
                line_number,
                old_value,
                new_value
            FROM variable_changes
            WHERE variable_name = ?
            ORDER BY frame_id ASC, id ASC
        """, (variable_name,))

        return self.cursor.fetchall()

    # =========================================================
    # GET VARIABLE VALUE
    # =========================================================

    def get_variable_value(
        self,
        variable_name,
        frame_id=None
    ):

        if frame_id is None:

            self.cursor.execute("""
                SELECT new_value
                FROM variable_changes
                WHERE variable_name = ?
                ORDER BY frame_id DESC, id DESC
                LIMIT 1
            """, (variable_name,))

        else:

            self.cursor.execute("""
                SELECT new_value
                FROM variable_changes
                WHERE variable_name = ?
                AND frame_id <= ?
                ORDER BY frame_id DESC, id DESC
                LIMIT 1
            """, (
                variable_name,
                frame_id
            ))

        result = self.cursor.fetchone()

        if result:
            return result[0]

        return None

    # =========================================================
    # MAX FRAME
    # =========================================================

    def get_max_frame(self):

        self.cursor.execute("""
            SELECT MAX(frame_id)
            FROM variable_changes
        """)

        result = self.cursor.fetchone()

        if result and result[0] is not None:
            return result[0]

        return 0

    # =========================================================
    # TOTAL CHANGES
    # =========================================================

    def get_change_count(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM variable_changes
        """)

        result = self.cursor.fetchone()

        return result[0]

    # =========================================================
    # SHOW RECORDS IN TERMINAL
    # =========================================================

    def show_records(self):

        history = self.get_history()

        if not history:
            print("No execution history found.")
            return

        print()
        print("=" * 95)
        print("PYCHRONICLE EXECUTION HISTORY")
        print("=" * 95)

        print(
            f"{'Frame':<8}"
            f"{'Line':<8}"
            f"{'Variable':<18}"
            f"{'Old Value':<20}"
            f"{'New Value':<20}"
        )

        print("-" * 95)

        for record in history:

            frame = record[0]
            line = record[1]
            variable = record[2]
            old_value = record[3]
            new_value = record[4]

            if old_value is None:
                old_value = "—"

            print(
                f"{frame:<8}"
                f"{line:<8}"
                f"{variable:<18}"
                f"{str(old_value):<20}"
                f"{str(new_value):<20}"
            )

        print("-" * 95)
        print(f"Total changes: {len(history)}")

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):
        self.conn.close()


# =============================================================
# GLOBAL DATABASE
# =============================================================

database = Database()


# =============================================================
# COMPATIBILITY FUNCTIONS
# =============================================================

def save(
    frame,
    line,
    variable,
    value,
    old_value=None
):
    database.save_change(
        frame,
        line,
        variable,
        old_value,
        value
    )


def clear():
    database.clear()


def get_history():
    return database.get_history()


def get_frame(frame_id):
    return database.get_frame(frame_id)


def get_current_state(frame_id):
    return database.get_current_state(frame_id)


def get_variables():
    return database.get_variables()


def get_variable_history(variable_name):
    return database.get_variable_history(variable_name)


def get_variable_value(variable_name, frame_id=None):
    return database.get_variable_value(
        variable_name,
        frame_id
    )

def get_max_frame():
    return database.get_max_frame()


def get_change_count():
    return database.get_change_count()


def show_records():
    database.show_records()
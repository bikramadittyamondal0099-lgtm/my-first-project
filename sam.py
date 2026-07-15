import ast
import sqlite3
import time
conn = sqlite3.connect("trace.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    line_number INTEGER,
    variable_name TEXT,
    value TEXT
)
""")

conn.commit()

class VariableTracker(ast.NodeVisitor):

    def visit_Assign(self, node):
        for target in node.targets:

            if isinstance(target, ast.Name):

                variable_name = target.id
                line_no = node.lineno

                print(f"Variable: {variable_name}, Line: {line_no}")

                cursor.execute(
                    """
                    INSERT INTO traces
                    (timestamp, line_number, variable_name, value)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        time.time(),
                        line_no,
                        variable_name,
                        "Unknown"
                    )
                )

        self.generic_visit(node)
with open("main.py", "r") as file:
    code = file.read()
tree = ast.parse(code)

tracker = VariableTracker()
tracker.visit(tree)
conn.commit()
print("\nSaved Records:\n")

cursor.execute("""
SELECT line_number, variable_name, value
FROM traces
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
x = 10
y = 20
z = x + y

name = "PyChronicle"
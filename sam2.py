import ast
import sqlite3
import time

# Read target file
with open("main.py", "r") as file:
    code = file.read()

print("Reading main.py...")
print(code)

tree = ast.parse(code)

# Database setup
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

# AST Visitor
class VariableTracker(ast.NodeVisitor):

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):

                print(f"Found variable: {target.id} at line {node.lineno}")

                cursor.execute(
                    """
                    INSERT INTO traces
                    (timestamp, line_number, variable_name, value)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        time.time(),
                        node.lineno,
                        target.id,
                        "Unknown"
                    )
                )

        self.generic_visit(node)

tracker = VariableTracker()
tracker.visit(tree)

conn.commit()

# Show database contents
print("\nDatabase Records:\n")

cursor.execute("""
SELECT line_number, variable_name, value
FROM traces
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

print("\nTotal Records:", len(rows))

conn.close()
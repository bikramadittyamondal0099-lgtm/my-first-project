import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from parser import parse_file
from tracer import run
from database import clear, show_records
current_file = ""
def open_file():
    global current_file
    filename = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")]
    )
    if filename:
        current_file = filename
        with open(filename, "r") as f:
            code = f.read()
        editor.delete("1.0", tk.END)
        editor.insert(tk.END, code)
        status.config(text=f"Opened: {filename}")
def save_file():
    global current_file
    if current_file == "":
        current_file = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py")]
        )
    if current_file:
        with open(current_file, "w") as f:
            f.write(editor.get("1.0", tk.END))
        status.config(text="File Saved Successfully")
def run_project():
    global current_file
    if current_file == "":
        messagebox.showerror("Error", "Open a Python file first.")
        return
    save_file()
    output.delete("1.0", tk.END)
    clear()
    code = parse_file(current_file)
    run(code)
    output.insert(tk.END, "Execution Finished\n\n")
    output.insert(tk.END, "Database Records\n")
    output.insert(tk.END, "-" * 40 + "\n")
    import io
    import contextlib
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        show_records()
    output.insert(tk.END, buffer.getvalue())
    status.config(text="Execution Complete")
root = tk.Tk()
root.title("PyChronicle - Week 2")
root.geometry("1000x700")
top = tk.Frame(root)
top.pack(fill="x", pady=5)
tk.Button(top, text="Open", width=15, command=open_file).pack(
    side="left", padx=5
)
tk.Button(top, text="Save", width=15, command=save_file).pack(
    side="left", padx=5
)
tk.Button(top, text="Run PyChronicle", width=18, command=run_project).pack(
    side="left", padx=5
)
editor = scrolledtext.ScrolledText(root, font=("Consolas", 12), height=20)
editor.pack(fill="both", expand=True, padx=10, pady=5)
tk.Label(root, text="Execution History").pack()
output = scrolledtext.ScrolledText(root, font=("Consolas", 11), height=12)
output.pack(fill="both", expand=True, padx=10, pady=5)
status = tk.Label(root, text="Ready", anchor="w")
status.pack(fill="x")
root.mainloop()
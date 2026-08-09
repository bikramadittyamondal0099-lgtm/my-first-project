import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from parser import parse_file
from tracer import run

from database import (
    clear,
    get_history,
    get_current_state,
    get_max_frame,
    get_variables,
    get_variable_history,
    get_frame
)


# ============================================================
# GLOBAL VARIABLES
# ============================================================

current_file = ""
current_frame = 0
max_frame = 0


# ============================================================
# COLORS
# ============================================================

BG = "#0F141A"
PANEL = "#161D26"
PANEL2 = "#1D2631"
EDITOR_BG = "#0B1015"

TEXT = "#E6EDF3"
MUTED = "#8B949E"

ACCENT = "#58A6FF"
GREEN = "#3FB950"
RED = "#F85149"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("PyChronicle - Time Travel Debugger")
root.geometry("1400x900")
root.minsize(1150, 750)
root.configure(bg=BG)


# ============================================================
# OPEN FILE
# ============================================================

def open_file():

    global current_file

    filename = filedialog.askopenfilename(
        title="Open Python File",
        filetypes=[
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            code = file.read()

        current_file = filename

        editor.delete(
            "1.0",
            tk.END
        )

        editor.insert(
            tk.END,
            code
        )

        status_label.config(
            text=f"Opened: {filename}",
            fg=GREEN
        )

    except Exception as error:

        messagebox.showerror(
            "Open Error",
            str(error)
        )


# ============================================================
# SAVE FILE
# ============================================================

def save_file():

    global current_file

    if current_file == "":

        current_file = filedialog.asksaveasfilename(
            title="Save Python File",
            defaultextension=".py",
            filetypes=[
                ("Python Files", "*.py"),
                ("All Files", "*.*")
            ]
        )

    if not current_file:
        return

    try:

        code = editor.get(
            "1.0",
            tk.END
        )

        with open(
            current_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(code)

        status_label.config(
            text="File saved successfully",
            fg=GREEN
        )

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            str(error)
        )


# ============================================================
# DISPLAY EXECUTION HISTORY
# ============================================================

def display_history():

    output.delete(
        "1.0",
        tk.END
    )

    try:

        history = get_history()

        if not history:

            output.insert(
                tk.END,
                "No execution history found.\n\n"
            )

            output.insert(
                tk.END,
                "Open a Python file and press RUN."
            )

            return

        output.insert(
            tk.END,
            "PYCHRONICLE EXECUTION HISTORY\n"
        )

        output.insert(
            tk.END,
            "=" * 105 + "\n"
        )

        output.insert(
            tk.END,
            f"{'Frame':<8}"
            f"{'Line':<8}"
            f"{'Variable':<18}"
            f"{'Old Value':<25}"
            f"{'New Value':<25}\n"
        )

        output.insert(
            tk.END,
            "-" * 105 + "\n"
        )

        for record in history:

            frame = record[0]
            line = record[1]
            variable = record[2]
            old_value = record[3]
            new_value = record[4]

            if old_value is None:
                old_value = "—"

            output.insert(
                tk.END,
                f"{frame:<8}"
                f"{line:<8}"
                f"{variable:<18}"
                f"{str(old_value):<25}"
                f"{str(new_value):<25}\n"
            )

        output.insert(
            tk.END,
            "-" * 105 + "\n"
        )

        output.insert(
            tk.END,
            f"Total variable changes: {len(history)}\n"
        )

        output.see(
            tk.END
        )

    except Exception as error:

        output.insert(
            tk.END,
            f"History Error:\n{error}"
        )


# ============================================================
# UPDATE VARIABLE STATE
# ============================================================

def update_variables(frame):

    variables_text.config(
        state=tk.NORMAL
    )

    variables_text.delete(
        "1.0",
        tk.END
    )

    try:

        state = get_current_state(
            frame
        )

        if not state:

            variables_text.insert(
                tk.END,
                "No variables recorded."
            )

        else:

            for variable, value in state.items():

                variables_text.insert(
                    tk.END,
                    f"{variable:<20} {value}\n"
                )

    except Exception as error:

        variables_text.insert(
            tk.END,
            f"Error: {error}"
        )

    variables_text.config(
        state=tk.DISABLED
    )


# ============================================================
# HIGHLIGHT CURRENT LINE
# ============================================================

def update_current_line(frame):

    editor.tag_remove(
        "current_line",
        "1.0",
        tk.END
    )

    try:

        frame_data = get_frame(
            frame
        )

        if not frame_data:
            return

        line_number = frame_data[0][0]

        start = f"{line_number}.0"
        end = f"{line_number}.end"

        editor.tag_add(
            "current_line",
            start,
            end
        )

        editor.tag_config(
            "current_line",
            background="#26364A"
        )

        editor.see(
            start
        )

    except Exception:
        pass


# ============================================================
# SHOW CURRENT FRAME
# ============================================================

def update_frame(frame):

    global current_frame

    current_frame = int(
        frame
    )

    frame_label.config(
        text=f"FRAME {current_frame} / {max_frame}"
    )

    update_variables(
        current_frame
    )

    update_current_line(
        current_frame
    )

    show_selected_watch()


# ============================================================
# TIMELINE
# ============================================================

def timeline_changed(value):

    frame = int(
        float(value)
    )

    update_frame(
        frame
    )


def previous_frame():

    global current_frame

    if current_frame > 0:

        current_frame -= 1

        timeline.set(
            current_frame
        )

        update_frame(
            current_frame
        )


def next_frame():

    global current_frame

    if current_frame < max_frame:

        current_frame += 1

        timeline.set(
            current_frame
        )

        update_frame(
            current_frame
        )


# ============================================================
# UPDATE TIMELINE
# ============================================================

def update_timeline():

    global max_frame

    max_frame = get_max_frame()

    if max_frame < 1:
        max_frame = 1

    timeline.config(
        from_=0,
        to=max_frame
    )

    timeline.set(
        max_frame
    )

    update_frame(
        max_frame
    )


# ============================================================
# REFRESH WATCH VARIABLES
# ============================================================

def refresh_watch_list():

    watch_list.delete(
        0,
        tk.END
    )

    try:

        variables = get_variables()

        for variable in variables:

            watch_list.insert(
                tk.END,
                variable
            )

    except Exception as error:

        watch_history.config(
            state=tk.NORMAL
        )

        watch_history.delete(
            "1.0",
            tk.END
        )

        watch_history.insert(
            tk.END,
            f"Error: {error}"
        )

        watch_history.config(
            state=tk.DISABLED
        )


# ============================================================
# SHOW SELECTED VARIABLE HISTORY
# ============================================================

def show_selected_watch():

    selection = watch_list.curselection()

    if not selection:
        return

    variable = watch_list.get(
        selection[0]
    )

    watch_history.config(
        state=tk.NORMAL
    )

    watch_history.delete(
        "1.0",
        tk.END
    )

    try:

        history = get_variable_history(
            variable
        )

        watch_history.insert(
            tk.END,
            f"VARIABLE: {variable}\n"
        )

        watch_history.insert(
            tk.END,
            "=" * 60 + "\n\n"
        )

        if not history:

            watch_history.insert(
                tk.END,
                "No history available."
            )

        else:

            for record in history:

                frame = record[0]
                line = record[1]
                old_value = record[2]
                new_value = record[3]

                if old_value is None:
                    old_value = "—"

                watch_history.insert(
                    tk.END,
                    f"Frame : {frame}\n"
                )

                watch_history.insert(
                    tk.END,
                    f"Line  : {line}\n"
                )

                watch_history.insert(
                    tk.END,
                    f"Old   : {old_value}\n"
                )

                watch_history.insert(
                    tk.END,
                    f"New   : {new_value}\n"
                )

                watch_history.insert(
                    tk.END,
                    "\n"
                )

                watch_history.insert(
                    tk.END,
                    "-" * 60 + "\n\n"
                )

        watch_history.see(
            tk.END
        )

    except Exception as error:

        watch_history.insert(
            tk.END,
            f"Error: {error}"
        )

    watch_history.config(
        state=tk.DISABLED
    )


# ============================================================
# RUN PYCHRONICLE
# ============================================================

def run_project():

    global current_file

    if current_file == "":

        messagebox.showwarning(
            "No File",
            "Please open a Python file first."
        )

        return

    save_file()

    if not current_file:
        return

    try:

        output.delete(
            "1.0",
            tk.END
        )

        clear()

        status_label.config(
            text="Reading Python file...",
            fg=ACCENT
        )

        root.update()

        code = parse_file(
            current_file
        )

        status_label.config(
            text="Tracing execution...",
            fg=ACCENT
        )

        root.update()

        run(
            code
        )

        display_history()

        refresh_watch_list()

        update_timeline()

        status_label.config(
            text="Execution completed successfully",
            fg=GREEN
        )

    except Exception as error:

        output.delete(
            "1.0",
            tk.END
        )

        output.insert(
            tk.END,
            "EXECUTION ERROR\n"
        )

        output.insert(
            tk.END,
            "=" * 60 + "\n"
        )

        output.insert(
            tk.END,
            str(error)
        )

        status_label.config(
            text="Execution failed",
            fg=RED
        )

        messagebox.showerror(
            "PyChronicle Error",
            str(error)
        )


# ============================================================
# CLEAR OUTPUT
# ============================================================

def clear_output():

    output.delete(
        "1.0",
        tk.END
    )

    status_label.config(
        text="Output cleared",
        fg=MUTED
    )


# ============================================================
# HEADER
# ============================================================

top_bar = tk.Frame(
    root,
    bg=BG
)

top_bar.pack(
    fill="x",
    padx=18,
    pady=(15, 8)
)


title_frame = tk.Frame(
    top_bar,
    bg=BG
)

title_frame.pack(
    side="left"
)


tk.Label(
    title_frame,
    text="PYCHRONICLE",
    font=("Segoe UI", 21, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    anchor="w"
)


tk.Label(
    title_frame,
    text="TIME-TRAVEL PYTHON DEBUGGER",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg=ACCENT
).pack(
    anchor="w"
)


# ============================================================
# TOP BUTTONS
# ============================================================

buttons = tk.Frame(
    top_bar,
    bg=BG
)

buttons.pack(
    side="right"
)


button_style = {
    "font": ("Segoe UI", 9, "bold"),
    "bg": PANEL2,
    "fg": TEXT,
    "activebackground": ACCENT,
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "padx": 15,
    "pady": 8
}


tk.Button(
    buttons,
    text="OPEN",
    command=open_file,
    **button_style
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="SAVE",
    command=save_file,
    **button_style
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="RUN",
    command=run_project,
    font=("Segoe UI", 9, "bold"),
    bg=GREEN,
    fg="white",
    activebackground="#2EA043",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=22,
    pady=8
).pack(
    side="left",
    padx=4
)


# ============================================================
# MAIN AREA
# ============================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=8
)


# ============================================================
# SOURCE CODE PANEL
# ============================================================

code_panel = tk.Frame(
    main,
    bg=PANEL
)

code_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


tk.Label(
    code_panel,
    text="SOURCE CODE",
    font=("Segoe UI", 10, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(
    anchor="w",
    padx=14,
    pady=10
)


editor = scrolledtext.ScrolledText(
    code_panel,
    bg=EDITOR_BG,
    fg=TEXT,
    insertbackground=TEXT,
    selectbackground="#264F78",
    font=("Consolas", 11),
    relief="flat",
    bd=0,
    wrap=tk.NONE
)

editor.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10)
)


# ============================================================
# RIGHT PANEL
# ============================================================

right = tk.Frame(
    main,
    bg=BG,
    width=460
)

right.pack(
    side="right",
    fill="y"
)

right.pack_propagate(
    False
)


# ============================================================
# VARIABLE STATE
# ============================================================

variable_panel = tk.Frame(
    right,
    bg=PANEL,
    height=160
)

variable_panel.pack(
    fill="x",
    pady=(0, 10)
)

variable_panel.pack_propagate(
    False
)


tk.Label(
    variable_panel,
    text="VARIABLE STATE",
    font=("Segoe UI", 10, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(
    anchor="w",
    padx=14,
    pady=8
)


variables_text = scrolledtext.ScrolledText(
    variable_panel,
    bg=EDITOR_BG,
    fg=GREEN,
    font=("Consolas", 10),
    relief="flat",
    bd=0,
    wrap=tk.NONE
)

variables_text.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 8)
)

variables_text.config(
    state=tk.DISABLED
)


# ============================================================
# WATCH VARIABLES + HISTORY
# ============================================================

watch_panel = tk.Frame(
    right,
    bg=PANEL
)

watch_panel.pack(
    fill="both",
    expand=True
)


tk.Label(
    watch_panel,
    text="WATCH VARIABLES",
    font=("Segoe UI", 10, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(
    anchor="w",
    padx=14,
    pady=(10, 6)
)


# ============================================================
# WATCH LIST
# ============================================================

watch_list = tk.Listbox(
    watch_panel,
    bg=EDITOR_BG,
    fg=TEXT,
    selectbackground=ACCENT,
    selectforeground="white",
    font=("Consolas", 11),
    relief="flat",
    bd=0,
    height=6,
    activestyle="none"
)

watch_list.pack(
    fill="x",
    padx=10,
    pady=(0, 10)
)


watch_list.bind(
    "<<ListboxSelect>>",
    lambda event: show_selected_watch()
)


# ============================================================
# VARIABLE HISTORY HEADER
# ============================================================

history_header = tk.Frame(
    watch_panel,
    bg=PANEL
)

history_header.pack(
    fill="x",
    padx=10
)


tk.Label(
    history_header,
    text="VARIABLE HISTORY",
    font=("Segoe UI", 10, "bold"),
    bg=PANEL,
    fg=ACCENT
).pack(
    side="left",
    pady=(3, 7)
)


# ============================================================
# LARGE VARIABLE HISTORY
# ============================================================

watch_history = scrolledtext.ScrolledText(
    watch_panel,
    bg=EDITOR_BG,
    fg=ACCENT,
    insertbackground=TEXT,
    font=("Consolas", 10),
    relief="flat",
    bd=0,
    wrap=tk.NONE
)

watch_history.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 12)
)

watch_history.config(
    state=tk.DISABLED
)


# ============================================================
# BOTTOM AREA
# ============================================================

bottom = tk.Frame(
    root,
    bg=BG
)

bottom.pack(
    fill="both",
    padx=18,
    pady=(0, 10)
)


# ============================================================
# TIMELINE
# ============================================================

timeline_panel = tk.Frame(
    bottom,
    bg=PANEL
)

timeline_panel.pack(
    fill="x",
    pady=(0, 8)
)


frame_label = tk.Label(
    timeline_panel,
    text="FRAME 0 / 0",
    font=("Consolas", 10, "bold"),
    bg=PANEL,
    fg=ACCENT
)

frame_label.pack(
    side="left",
    padx=12
)


timeline = tk.Scale(
    timeline_panel,
    from_=0,
    to=1,
    orient="horizontal",
    command=timeline_changed,
    showvalue=False,
    bg=PANEL,
    fg=TEXT,
    troughcolor="#30363D",
    activebackground=ACCENT,
    highlightthickness=0
)

timeline.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10,
    pady=5
)


tk.Button(
    timeline_panel,
    text="◀",
    command=previous_frame,
    **button_style
).pack(
    side="left",
    padx=3
)


tk.Button(
    timeline_panel,
    text="▶",
    command=next_frame,
    **button_style
).pack(
    side="left",
    padx=(3, 8)
)


# ============================================================
# EXECUTION HISTORY
# ============================================================

history_panel = tk.Frame(
    bottom,
    bg=PANEL
)

history_panel.pack(
    fill="both",
    expand=True
)


history_top = tk.Frame(
    history_panel,
    bg=PANEL
)

history_top.pack(
    fill="x"
)


tk.Label(
    history_top,
    text="EXECUTION HISTORY",
    font=("Segoe UI", 10, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(
    side="left",
    padx=14,
    pady=8
)


tk.Button(
    history_top,
    text="CLEAR",
    command=clear_output,
    font=("Segoe UI", 8, "bold"),
    bg=PANEL2,
    fg=MUTED,
    relief="flat",
    bd=0,
    padx=10,
    pady=4
).pack(
    side="right",
    padx=10
)


output = scrolledtext.ScrolledText(
    history_panel,
    bg=EDITOR_BG,
    fg=MUTED,
    font=("Consolas", 9),
    relief="flat",
    bd=0,
    wrap=tk.NONE
)

output.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10)
)


# ============================================================
# STATUS BAR
# ============================================================

status_bar = tk.Frame(
    root,
    bg="#0B1015"
)

status_bar.pack(
    fill="x"
)


status_label = tk.Label(
    status_bar,
    text="Ready",
    bg="#0B1015",
    fg=MUTED,
    font=("Segoe UI", 9),
    anchor="w"
)

status_label.pack(
    fill="x",
    padx=18,
    pady=6
)


# ============================================================
# START
# ============================================================

root.mainloop()
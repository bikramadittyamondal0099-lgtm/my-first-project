import sys
from database import save

last_state = {}


def trace(frame, event, arg):
    if event in ("line", "return"):
        line = frame.f_lineno

        for variable, value in frame.f_locals.items():

            # Ignore Python internal variables
            if variable.startswith("__"):
                continue

            # Save only changed values
            if last_state.get(variable) != value:
                last_state[variable] = value
                print(f"Line {line}: {variable} = {value}")
                save(line, variable, value)

    return trace


def run(code):
    global last_state

    last_state = {}

    sys.settrace(trace)
    exec(code, {})
    sys.settrace(None)
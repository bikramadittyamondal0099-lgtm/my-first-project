import sys
from database import save

last_state = {}


def trace(frame, event, arg):

    if event == "line":

        line = frame.f_lineno

        for variable, value in frame.f_locals.items():

            if last_state.get(variable) != value:

                last_state[variable] = value

                print(f"Line {line}: {variable} = {value}")

                save(line, variable, value)

    return trace


def run(code):

    sys.settrace(trace)

    exec(code)

    sys.settrace(None)
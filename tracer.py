import sys

from database import save, clear


class ExecutionTracer:

    def __init__(self):

        self.frame_number = 0

        # Stores the previous values for each frame
        self.previous_locals = {}

    # =========================================================
    # TRACE FUNCTION
    # =========================================================

    def trace(self, frame, event, arg):

        if event == "line":

            self.frame_number += 1

            current_locals = dict(
                frame.f_locals
            )

            current_state = {}

            for variable, value in current_locals.items():

                # Ignore Python internal variables
                if variable.startswith("__"):
                    continue

                try:
                    new_value = repr(value)
                except Exception:
                    new_value = str(value)

                current_state[variable] = new_value

                # New variable
                if variable not in self.previous_locals:

                    save(
                        self.frame_number,
                        frame.f_lineno,
                        variable,
                        new_value,
                        None
                    )

                # Existing variable changed
                elif self.previous_locals[variable] != new_value:

                    save(
                        self.frame_number,
                        frame.f_lineno,
                        variable,
                        new_value,
                        self.previous_locals[variable]
                    )

            self.previous_locals = current_state

        return self.trace

    # =========================================================
    # RUN CODE
    # =========================================================

    def run(self, code):

        clear()

        self.frame_number = 0

        self.previous_locals = {}

        sys.settrace(self.trace)

        try:

            exec(
                compile(
                    code,
                    "<pychronicle>",
                    "exec"
                ),
                {
                    "__name__": "__main__"
                }
            )

        except Exception as error:

            print()
            print("Execution Error:")
            print(error)

        finally:

            sys.settrace(None)


# =============================================================
# SIMPLE RUN FUNCTION
# =============================================================

def run(code):

    tracer = ExecutionTracer()

    tracer.run(code)

    return tracer
import sys
def trace(frame, event, arg):
    if event == "line":
        print("Line:", frame.f_lineno)
        print(frame.f_locals)
    return trace
sys.settrace(trace)
x = 10
y = 20
z = x + y
sys.settrace(None)
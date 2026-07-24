import sys
def trace(frame, event, arg):
    print(event, frame.f_lineno)
    return trace
sys.settrace(trace)
x = 10
y = 20
z = x + y
sys.settrace(None)
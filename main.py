from parser import parse_file
from tracer import run
from database import clear, show_records

TARGET_FILE = "test sample.py"
def main():
    print("starting")
    clear()
    print("\nReading and Parsing Python File\n")
    code = parse_file(TARGET_FILE)
    print("\nStarting Execution Trace\n")
    run(code)
    print("\nHistory:\n")
    show_records()
    print("\nFinished Successfully.")
if __name__ == "__main__":
    main()
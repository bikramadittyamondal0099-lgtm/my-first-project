# main.py

from parser import parse_file
from tracer import run
from database import clear, show_records

TARGET_FILE = "test sample.py"


def main():

    print("=" * 50)
    print("        PYCHRONICLE")
    print("=" * 50)

    # Clear old database records
    clear()

    print("\nReading Python File...\n")

    # Parse the target file
    code = parse_file(TARGET_FILE)

    print("\nStarting Execution Trace...\n")

    # Execute with tracer
    run(code)

    print("\nExecution History\n")

    # Display database records
    show_records()

    print("\nPyChronicle Finished Successfully.")


if __name__ == "__main__":
    main()
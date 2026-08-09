import typer

from parser import parse_file
from tracer import run
from database import clear, show_records


app = typer.Typer()


@app.command()
def run_file(filename: str):

    print("=" * 50)
    print("PYCHRONICLE")
    print("=" * 50)

    print(f"\nRunning: {filename}\n")

    clear()

    try:

        code = parse_file(filename)

        print("Starting tracer...\n")

        run(code)

        print("\nExecution History")
        print("-" * 50)

        show_records()

        print("\nFinished.")

    except FileNotFoundError:

        print("File not found:", filename)

    except Exception as error:

        print("Error:", error)


@app.command()
def version():

    print("PyChronicle v1.0")


if __name__ == "__main__":
    app()
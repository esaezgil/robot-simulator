import sys
from typing import TextIO

from robot_simulator.mars_simulation import MarsInputError, run_mars_simulation


def run(input_stream: TextIO, output_stream: TextIO) -> None:
    input_text = input_stream.read()
    output_text = run_mars_simulation(input_text)
    print(output_text, file=output_stream)


if __name__ == "__main__":
    try:
        run(sys.stdin, sys.stdout)
    except MarsInputError as error:
        raise SystemExit(f"Invalid input: {error}") from None

# Robot simulator

## Prerequisites

Python 3.10+ and Poetry are required. On macOS, install them with Homebrew:

```bash
brew install python@3.10 poetry
```

## Quick start

```bash
make install
poetry run python -m robot_simulator.cli < mars_sample.txt
make check
```

`make install` creates the project virtual environment and installs dependencies.

## Input and output

The program reads standard input and writes one final line per robot to
standard output. The first line creates the planet; each following
position/instruction pair creates and runs one robot.

```text
upper_right_x upper_right_y   # builds the planet boundary, e.g. 5 3
robot_x robot_y orientation   # builds a robot, e.g. 1 1 E
instructions                  # parses commands, e.g. RFRFRF
...                           # robot and instruction lines repeat
```

## Error handling

Malformed input exits with a concise error (input is assumed to meet
the limits stated in the exercise).

## Structure

```
robot_simulator/
  cli.py                 # command-line interface
  mars_simulation.py     # Mars-specific text adapter
  ...                    # robot, planet, navigation, commands, and execution orchestration
tests/
  acceptance/            # Mars text-input/text-output scenarios
  ...                    # focused domain tests
```

## Design decisions

- Robot and planet state

  - `Robot` owns its position, orientation, and lost status.
  - `Planet` owns the rectangular limits and scents.
  - One planet is shared across robot runs, so scents left by earlier robots
    affect later robots.
  - `Coordinates` and `Position` are immutable, allowing coordinates to be used
    safely as scent keys.

- Commands

  - Movement and turn directions use separate types, keeping `FORWARD` apart
    from `LEFT` and `RIGHT`.
  - Commands are immutable and do not have per-run state.
  - The simulation loop dispatches commands through the common `execute(robot, planet)`.
  - To add a command to the Mars text interface, implement `Command` and register
  an instance under its input code in `INSTRUCTION_TO_COMMAND`.

- Parsing and terminal I/O

  - The Mars adapter turns input lines into planets, robots, and commands.
  - The CLI reads standard input and writes each robot's final state to standard output.

## Testing

- `make check` runs linting, formatting checks, type checking, and tests.
- `poetry run pytest` runs the test suite.

from robot_simulator.instructions import Command, parse_instruction_sequence
from robot_simulator.navigation import Coordinates, Orientation, Position
from robot_simulator.planet import Planet
from robot_simulator.robot import Robot
from robot_simulator.simulator import Simulation


class MarsInputError(Exception):
    pass


def run_mars_simulation(input_text: str) -> str:
    planet, robot_runs = _parse_mars_input(input_text)
    simulation = Simulation(planet)
    output_lines: list[str] = []

    for robot, instructions in robot_runs:
        simulation.run(robot, instructions)
        output_lines.append(str(robot))

    return "\n".join(output_lines)


def _parse_mars_input(
    input_text: str,
) -> tuple[Planet, list[tuple[Robot, list[Command]]]]:
    try:
        input_lines = input_text.strip().splitlines()
        planet = _parse_planet(input_lines[0])
        robot_input_lines = input_lines[1:]

        if len(robot_input_lines) % 2 != 0:
            raise ValueError("Each robot position must have an instruction line.")

        robot_runs: list[tuple[Robot, list[Command]]] = []
        for line_index in range(0, len(robot_input_lines), 2):
            robot = _parse_robot(robot_input_lines[line_index])
            instruction_line = robot_input_lines[line_index + 1]
            instructions = parse_instruction_sequence(instruction_line.strip())
            robot_runs.append((robot, instructions))

        return planet, robot_runs
    except (IndexError, KeyError, ValueError) as error:
        raise MarsInputError("Unable to parse simulation input.") from error


def _parse_planet(world_line: str) -> Planet:
    x_coordinate, y_coordinate = world_line.split()
    upper_right_corner = Coordinates(int(x_coordinate), int(y_coordinate))
    return Planet(upper_right_corner)


def _parse_robot(position_line: str) -> Robot:
    x_coordinate, y_coordinate, orientation_name = position_line.split()
    position = Position(
        Coordinates(int(x_coordinate), int(y_coordinate)),
        Orientation[orientation_name],
    )
    return Robot(position)

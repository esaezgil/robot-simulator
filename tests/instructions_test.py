import pytest

from robot_simulator.instructions import (
    INSTRUCTION_TO_COMMAND,
    Command,
    MovementDirection,
    MovementInstruction,
    OrientationChangeInstruction,
    TurnDirection,
    parse_instruction_sequence,
)
from robot_simulator.navigation import Coordinates, Orientation, Position
from robot_simulator.planet import Planet
from robot_simulator.robot import Robot, RobotStatus


class TestOrientationChanges:
    @pytest.mark.parametrize(
        "start_orientation, instruction, expected_orientation",
        [
            pytest.param(
                Orientation.N,
                OrientationChangeInstruction(TurnDirection.LEFT),
                Orientation.W,
                id="from north, left turns west",
            ),
            pytest.param(
                Orientation.W,
                OrientationChangeInstruction(TurnDirection.LEFT),
                Orientation.S,
                id="from west, left turns south",
            ),
            pytest.param(
                Orientation.S,
                OrientationChangeInstruction(TurnDirection.LEFT),
                Orientation.E,
                id="from south, left turns east",
            ),
            pytest.param(
                Orientation.E,
                OrientationChangeInstruction(TurnDirection.LEFT),
                Orientation.N,
                id="from east, left turns north",
            ),
            pytest.param(
                Orientation.N,
                OrientationChangeInstruction(TurnDirection.RIGHT),
                Orientation.E,
                id="from north, right turns east",
            ),
            pytest.param(
                Orientation.E,
                OrientationChangeInstruction(TurnDirection.RIGHT),
                Orientation.S,
                id="from east, right turns south",
            ),
            pytest.param(
                Orientation.S,
                OrientationChangeInstruction(TurnDirection.RIGHT),
                Orientation.W,
                id="from south, right turns west",
            ),
            pytest.param(
                Orientation.W,
                OrientationChangeInstruction(TurnDirection.RIGHT),
                Orientation.N,
                id="from west, right turns north",
            ),
        ],
    )
    def test_changes_orientation(
        self,
        start_orientation: Orientation,
        instruction: Command,
        expected_orientation: Orientation,
    ) -> None:
        planet = Planet(Coordinates(5, 5))
        robot = Robot(Position(Coordinates(0, 0), start_orientation))

        instruction.execute(robot, planet)

        assert robot.orientation == expected_orientation


class TestMovement:
    @pytest.mark.parametrize(
        "start_orientation, expected_coordinates",
        [
            pytest.param(
                Orientation.N,
                Coordinates(5, 6),
                id="move north (up)",
            ),
            pytest.param(
                Orientation.W,
                Coordinates(4, 5),
                id="move west (left)",
            ),
            pytest.param(
                Orientation.S,
                Coordinates(5, 4),
                id="move south (down)",
            ),
            pytest.param(
                Orientation.E,
                Coordinates(6, 5),
                id="move east (right)",
            ),
        ],
    )
    def test_moves_forward(
        self,
        start_orientation: Orientation,
        expected_coordinates: Coordinates,
    ) -> None:
        planet = Planet(Coordinates(100, 100))
        robot = Robot(Position(Coordinates(5, 5), start_orientation))

        MovementInstruction(MovementDirection.FORWARD).execute(robot, planet)

        assert robot.coordinates == expected_coordinates

    def test_ignored_move_keeps_robot_in_place_and_alive(self) -> None:
        planet = Planet(Coordinates(1, 1))
        current_coordinates = Coordinates(0, 0)
        first_robot = Robot(Position(current_coordinates, Orientation.W))
        second_robot = Robot(Position(current_coordinates, Orientation.W))
        forward_instruction = MovementInstruction(MovementDirection.FORWARD)

        forward_instruction.execute(first_robot, planet)
        forward_instruction.execute(second_robot, planet)

        assert first_robot.status == RobotStatus.LOST
        assert second_robot.coordinates == current_coordinates
        assert second_robot.status == RobotStatus.ALIVE


def test_parses_instruction_sequence() -> None:
    instructions = parse_instruction_sequence("LRF")

    assert instructions == [
        INSTRUCTION_TO_COMMAND["L"],
        INSTRUCTION_TO_COMMAND["R"],
        INSTRUCTION_TO_COMMAND["F"],
    ]

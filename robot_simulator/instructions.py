import abc
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from robot_simulator.navigation import Coordinates, Orientation
from robot_simulator.planet import MoveOutcome, Planet
from robot_simulator.robot import Robot


class Command(abc.ABC):
    @abc.abstractmethod
    def execute(self, robot: Robot, planet: Planet) -> None:
        raise NotImplementedError


class MovementDirection(Enum):
    FORWARD = "forward"


class TurnDirection(Enum):
    LEFT = "left"
    RIGHT = "right"


@dataclass(frozen=True)
class MovementInstruction(Command):
    direction: MovementDirection
    DIRECTION_TO_ORIENTATION_DELTAS: ClassVar[
        dict[MovementDirection, dict[Orientation, Coordinates]]
    ] = {
        MovementDirection.FORWARD: {
            Orientation.N: Coordinates(0, 1),
            Orientation.E: Coordinates(1, 0),
            Orientation.S: Coordinates(0, -1),
            Orientation.W: Coordinates(-1, 0),
        },
    }

    def execute(self, robot: Robot, planet: Planet) -> None:
        current_coordinates = robot.coordinates
        movement_deltas = self.DIRECTION_TO_ORIENTATION_DELTAS[self.direction]
        new_coordinates = current_coordinates.compute_new_coordinates(
            movement_deltas[robot.orientation]
        )
        outcome = planet.resolve_move(current_coordinates, new_coordinates)
        if outcome == MoveOutcome.MOVED:
            robot.move_to(new_coordinates)
        elif outcome == MoveOutcome.LOST:
            robot.mark_lost()


@dataclass(frozen=True)
class OrientationChangeInstruction(Command):
    direction: TurnDirection
    ORIENTATION_CYCLES_BY_TURN_DIRECTION: ClassVar[dict[TurnDirection, tuple[Orientation, ...]]] = {
        TurnDirection.LEFT: (
            Orientation.N,
            Orientation.W,
            Orientation.S,
            Orientation.E,
        ),
        TurnDirection.RIGHT: (
            Orientation.N,
            Orientation.E,
            Orientation.S,
            Orientation.W,
        ),
    }

    def execute(self, robot: Robot, planet: Planet) -> None:
        orientation_sequence = self.ORIENTATION_CYCLES_BY_TURN_DIRECTION[self.direction]
        current_index = orientation_sequence.index(robot.orientation)
        new_orientation = None
        if current_index < len(orientation_sequence) - 1:
            new_orientation = orientation_sequence[current_index + 1]
        else:
            new_orientation = orientation_sequence[0]
        robot.set_orientation(new_orientation)


INSTRUCTION_TO_COMMAND: dict[str, Command] = {
    "L": OrientationChangeInstruction(TurnDirection.LEFT),
    "R": OrientationChangeInstruction(TurnDirection.RIGHT),
    "F": MovementInstruction(MovementDirection.FORWARD),
}


def parse_instruction_sequence(instruction_text: str) -> list[Command]:
    instructions: list[Command] = []
    for instruction_code in instruction_text:
        instructions.append(INSTRUCTION_TO_COMMAND[instruction_code])
    return instructions

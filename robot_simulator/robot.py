from dataclasses import dataclass
from enum import Enum

from robot_simulator.navigation import Coordinates, Orientation, Position


class RobotStatus(Enum):
    ALIVE = "ALIVE"
    LOST = "LOST"


@dataclass(init=False)
class Robot:
    _position: Position
    _status: RobotStatus

    def __init__(
        self,
        position: Position,
        status: RobotStatus = RobotStatus.ALIVE,
    ) -> None:
        self._position = position
        self._status = status

    @property
    def coordinates(self) -> Coordinates:
        return self._position.coordinates

    @property
    def orientation(self) -> Orientation:
        return self._position.orientation

    @property
    def status(self) -> RobotStatus:
        return self._status

    def move_to(self, coordinates: Coordinates) -> None:
        self._position = Position(coordinates, self.orientation)

    def set_orientation(self, orientation: Orientation) -> None:
        self._position = Position(self.coordinates, orientation)

    def mark_lost(self) -> None:
        self._status = RobotStatus.LOST

    def __str__(self) -> str:
        output_parts = [
            str(self.coordinates.x),
            str(self.coordinates.y),
            self.orientation.name,
        ]
        if self.status == RobotStatus.LOST:
            output_parts.append(self.status.name)

        return " ".join(output_parts)

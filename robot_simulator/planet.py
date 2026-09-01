from enum import Enum

from robot_simulator.navigation import Coordinates


class MoveOutcome(Enum):
    MOVED = "moved"
    IGNORED_BY_SCENT = "ignored_by_scent"
    LOST = "lost"


class Planet:
    def __init__(self, upper_right_corner: Coordinates) -> None:
        self.upper_right_corner = upper_right_corner
        self._scented_coordinates: set[Coordinates] = set()

    def is_within_bounds(self, coordinates: Coordinates) -> bool:
        return (
            0 <= coordinates.x <= self.upper_right_corner.x
            and 0 <= coordinates.y <= self.upper_right_corner.y
        )

    def resolve_move(
        self,
        current_coordinates: Coordinates,
        destination_coordinates: Coordinates,
    ) -> MoveOutcome:
        if self.is_within_bounds(destination_coordinates):
            return MoveOutcome.MOVED

        if current_coordinates in self._scented_coordinates:
            return MoveOutcome.IGNORED_BY_SCENT

        self._scented_coordinates.add(current_coordinates)
        return MoveOutcome.LOST

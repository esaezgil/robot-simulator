from dataclasses import dataclass
from enum import Enum


class Orientation(Enum):
    N = "north"
    E = "east"
    S = "south"
    W = "west"


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int

    def compute_new_coordinates(
        self,
        coordinates: "Coordinates",
    ) -> "Coordinates":
        return Coordinates(self.x + coordinates.x, self.y + coordinates.y)


@dataclass(frozen=True)
class Position:
    coordinates: Coordinates
    orientation: Orientation

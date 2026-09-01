import pytest

from robot_simulator.navigation import Coordinates
from robot_simulator.planet import MoveOutcome, Planet


class TestPlanetBoundary:
    @pytest.mark.parametrize(
        "coordinates",
        [Coordinates(0, 0), Coordinates(5, 3)],
    )
    def test_includes_boundary_edges(self, coordinates: Coordinates) -> None:
        planet = Planet(Coordinates(5, 3))

        assert planet.is_within_bounds(coordinates)

    @pytest.mark.parametrize(
        "coordinates",
        [
            pytest.param(Coordinates(-1, 0), id="negative x"),
            pytest.param(Coordinates(0, -1), id="negative y"),
            pytest.param(Coordinates(6, 3), id="past maximum x"),
            pytest.param(Coordinates(5, 4), id="past maximum y"),
        ],
    )
    def test_excludes_coordinates_outside_boundary(
        self,
        coordinates: Coordinates,
    ) -> None:
        planet = Planet(Coordinates(5, 3))

        assert not planet.is_within_bounds(coordinates)


class TestPlanetMoveResolution:
    def test_moves_to_valid_destination(self) -> None:
        planet = Planet(Coordinates(1, 1))

        outcome = planet.resolve_move(Coordinates(0, 0), Coordinates(0, 1))

        assert outcome == MoveOutcome.MOVED

    def test_loses_robot_on_first_off_grid_move(self) -> None:
        planet = Planet(Coordinates(1, 1))

        outcome = planet.resolve_move(Coordinates(0, 0), Coordinates(-1, 0))

        assert outcome == MoveOutcome.LOST

    def test_ignores_off_grid_move_from_scented_position(self) -> None:
        planet = Planet(Coordinates(1, 1))
        current_coordinates = Coordinates(0, 0)

        first_outcome = planet.resolve_move(current_coordinates, Coordinates(-1, 0))
        outcome = planet.resolve_move(current_coordinates, Coordinates(0, -1))

        assert first_outcome == MoveOutcome.LOST
        assert outcome == MoveOutcome.IGNORED_BY_SCENT

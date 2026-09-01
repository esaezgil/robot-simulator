from robot_simulator.instructions import (
    MovementDirection,
    MovementInstruction,
    OrientationChangeInstruction,
    TurnDirection,
)
from robot_simulator.navigation import Coordinates, Orientation, Position
from robot_simulator.planet import Planet
from robot_simulator.robot import Robot, RobotStatus
from robot_simulator.simulator import Simulation


def test_stops_executing_commands_after_robot_is_lost() -> None:
    planet = Planet(Coordinates(1, 1))
    simulation = Simulation(planet)
    robot = Robot(Position(Coordinates(1, 1), Orientation.N))
    commands = [
        MovementInstruction(MovementDirection.FORWARD),  # Loses the robot.
        OrientationChangeInstruction(TurnDirection.RIGHT),  # Applies unless the robot is lost.
    ]

    simulation.run(robot, commands)

    assert robot.status == RobotStatus.LOST
    assert robot.orientation == Orientation.N

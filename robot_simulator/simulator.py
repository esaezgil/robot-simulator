from collections.abc import Iterable

from robot_simulator.instructions import Command
from robot_simulator.planet import Planet
from robot_simulator.robot import Robot, RobotStatus


class Simulation:
    def __init__(self, planet: Planet) -> None:
        self.planet = planet

    def run(self, robot: Robot, instructions: Iterable[Command]) -> None:
        for instruction in instructions:
            if robot.status == RobotStatus.LOST:
                break
            instruction.execute(robot, self.planet)

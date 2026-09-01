import pytest

from robot_simulator.mars_simulation import MarsInputError, run_mars_simulation


def test_runs_the_problem_sample() -> None:
    input_text = """\
5 3
1 1 E
RFRFRFRF
3 2 N
FRRFLLFFRRFLL
0 3 W
LLFFFLFLFL
"""

    output_text = run_mars_simulation(input_text)

    assert output_text == """\
1 1 E
3 3 N LOST
2 3 S"""


def test_rejects_malformed_input() -> None:
    input_text = """\
5 3
1 1 Q
F
"""

    with pytest.raises(MarsInputError):
        run_mars_simulation(input_text)

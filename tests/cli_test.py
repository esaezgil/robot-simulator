from io import StringIO

from robot_simulator.cli import run


def test_transforms_standard_input_to_standard_output() -> None:
    input_text = """\
1 1
0 0 N
F
"""
    input_stream = StringIO(input_text)
    output_stream = StringIO()

    run(input_stream, output_stream)

    assert output_stream.getvalue() == "0 1 N\n"

from io import StringIO
from pathlib import Path
from subprocess import check_output

from pybf.interpreter import Interpreter

from .utils import BaseTestCase

HELLO_WORLD = "Hello World!\n"


class TestInterpreter(BaseTestCase):
    def test_hello_world(self):
        string_io = StringIO()
        file = Path("tests/hello_world.bf")
        code = file.read_text()
        interpreter = Interpreter(code, filename=str(file), output=string_io)
        interpreter.run()
        self.assertEqual(string_io.getvalue(), HELLO_WORLD)

    def test_bash_hello_world(self):
        self.assertEqual(
            check_output(
                "python -m pybf hello_world.bf".split(),
                cwd="tests",
            ).decode(),
            HELLO_WORLD,
        )


class TestCompiler(BaseTestCase):
    def test_bash_hello_world(self):
        self.assertEqual(
            check_output(
                "python -m pybf hello_world.bf -cr".split(),
                cwd="tests",
            ).decode(),
            HELLO_WORLD,
        )

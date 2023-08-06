from collections import deque
from sys import stderr, stdin, stdout
from typing import TextIO

from .constants import TOKENS, Actions


class _Array:
    _arr: list[int]
    _ptr: int

    def __init__(self, size):
        self._arr = [0] * size
        self._ptr = 0

    def inc_ptr(self):
        self._ptr += 1

    def dec_ptr(self):
        self._ptr -= 1

    def inc_val(self):
        self._arr[self._ptr] += 1

    def dec_val(self):
        self._arr[self._ptr] -= 1

    def output(self):
        return self._arr[self._ptr]

    def input(self, val=None):
        self._arr[self._ptr] = val or ord(stdin.read(1))


class Interpreter:
    code: str
    filename: str
    size: int
    output: TextIO
    _jumps: deque[int]

    def __init__(
        self,
        code: str,
        filename: str = "<stdin>",
        size=30000,
        output=stdout,
    ):
        self.code = code
        self.filename = filename
        self.arr = _Array(size)
        self.output = output
        self._pos = 0
        self._jumps = deque()

    def run(self):
        if self.code.count("[") != self.code.count("]"):
            stderr.write(f"Error: Mismatched brackets in {self.filename}\n")
            return
        while self._pos < len(self.code):
            self._step()

    def _step(self):
        match TOKENS.get(self.code[self._pos]):
            case Actions.INC_PTR:
                self.arr.inc_ptr()
            case Actions.DEC_PTR:
                self.arr.dec_ptr()
            case Actions.INC_VAL:
                self.arr.inc_val()
            case Actions.DEC_VAL:
                self.arr.dec_val()
            case Actions.OUTPUT:
                self.output.write(chr(self.arr.output()))
                self.output.flush()
            case Actions.INPUT:
                self.arr.input()
            case Actions.LOOP_START:
                self._jumps.append(self._pos)
            case Actions.LOOP_END:
                if self.arr.output():
                    self._pos = self._jumps[-1]
                else:
                    self._jumps.pop()
            case _:
                pass

        self._pos += 1

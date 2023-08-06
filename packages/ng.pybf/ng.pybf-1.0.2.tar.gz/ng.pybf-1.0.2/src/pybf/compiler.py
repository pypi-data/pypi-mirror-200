from collections import deque
from pathlib import Path
from subprocess import run
from sys import stderr, stdout
from typing import TextIO

from setuptools._distutils.ccompiler import new_compiler

from .constants import TOKENS, Actions


class _Transpiler:
    code: str
    filename: str
    size: int
    _c_code_builder: deque[str]

    def __init__(
        self,
        code: str,
        filename: str = "<stdin>",
        size=30000,
    ):
        self.code = code
        self.filename = filename
        self.size = size
        self._pos = 0

    def transpile(self):
        self._c_code_builder = deque()
        if self.code.count("[") != self.code.count("]"):
            stderr.write(f"Syntax Error: Mismatched brackets in {self.filename}\n")
            return
        self._c_code_builder.append(
            f"/*transpiled from brainfuck with py.bf*/\n#include<stdio.h>\nint main(){{char a[{self.size}]={{0}};char*p=a;",
        )
        while self._pos < len(self.code):
            self._step()
        self._c_code_builder.append("return 0;}")
        return "".join(self._c_code_builder)

    def _step(self):
        match TOKENS.get(self.code[self._pos]):
            case Actions.INC_PTR:
                self._c_code_builder.append("p++;")
            case Actions.DEC_PTR:
                self._c_code_builder.append("p--;")
            case Actions.INC_VAL:
                self._c_code_builder.append("(*p)++;")
            case Actions.DEC_VAL:
                self._c_code_builder.append("(*p)--;")
            case Actions.OUTPUT:
                self._c_code_builder.append("putchar(*p);")
            case Actions.INPUT:
                self._c_code_builder.append("*p=getchar();")
            case Actions.LOOP_START:
                self._c_code_builder.append("while(*p){")
            case Actions.LOOP_END:
                self._c_code_builder.append("}")
            case _:
                pass

        self._pos += 1


class Compiler:
    c_code: str
    filename: str
    size: int
    output: TextIO

    def __init__(
        self,
        code: str,
        filename: str = "<stdin>",
        size=30000,
        output=stdout,
    ):
        self.filename = filename
        self.output = output
        self.c_code = _Transpiler(code, filename, size).transpile()

        self.output_filename = "a"
        if self.filename.endswith(".bf"):
            self.output_filename = self.filename[:-3]

    def transpile(self):
        c_file = Path(f"{self.output_filename}.c")
        c_file.write_text(self.c_code)

    def compile(self):
        compiler = new_compiler()
        c_file = Path(f"{self.output_filename}.c")
        o_file = Path(f"{self.output_filename}.o")
        exe_file = Path(f"{self.output_filename}")

        compiler.compile([str(c_file)])
        compiler.link_executable([str(o_file)], str(exe_file))

    def run(self):
        run(f"./{self.output_filename}", stdout=self.output, shell=True)

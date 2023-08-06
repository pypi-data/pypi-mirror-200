from mypyc.build import mypycify
from setuptools import setup

setup(
    ext_modules=mypycify(["src/pybf/interpreter.py", "src/pybf/compiler.py"]),
)

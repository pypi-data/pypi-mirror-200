# `pybf`

`pybf` contains a Python interpreter and a C transpiler/compiler for brainfuck.

## Installation

```bash
pip install ng.pybf
```

## Usage

### CLI

```text
usage: pybf [-h] [-p] [-c] [--compile] [-r] [filename]

Python interpreter and C transpiler/compiler for brainfuck

positional arguments:
  filename      path to bf file; leave blank to read from stdin

options:
  -h, --help    show this help message and exit
  -p, --python  use Python to interpret and run
  -c            transpile to C
  --compile     compile the transpiled C file
  -r, --run     execute
```

You may also call it as a Python module

```bash
python3 -m pybf [-h] [-p] [-c] [--compile] [-r] [filename]
```

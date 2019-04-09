# [Regression Test Utility](https://en.wikipedia.org/wiki/Regression_testing "Regression Testing")

[![Build Status](https://dev.azure.com/markoookeller/regress/_apis/build/status/keller00.regress?branchName=master)](https://dev.azure.com/markoookeller/regress/_build/latest?definitionId=1&branchName=master)

Compare expected output(s) to actual output(s)

## Usage
```
usage: regress [-h] [-a args] [-v] [-e] [-i IN] [-o OUT] [-p PATH] [--version]
               command

Run a program with multiple input files

positional arguments:
  command               Command to run with input files

optional arguments:
  -h, --help            show this help message and exit
  -a args               Additional arguments for command
  -v, --verbose         Increase output verbosity
  -e, --error           Change warnings to errors
  -i IN, --in IN        Input file prefix (default: in)
  -o OUT, --out OUT     Output file prefix (default: out)
  -p PATH, --path PATH  Path to input/output files (default: .)
  --version             Print current version number

```

## Installation
* git clone https://github.com/keller00/regress.git
* cd regress
* python setup.py install

## Development
* git clone https://github.com/keller00/regress.git
* cd regress
* python setup.py develop

## Run Tests
* python setup.py test

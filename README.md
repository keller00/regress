# [Regression Test Utility](https://en.wikipedia.org/wiki/Regression_testing "Regression Testing") [![CircleCI](https://circleci.com/gh/keller00/regress.svg?style=svg)](https://circleci.com/gh/keller00/regress)
Compare expected output(s) to actual output(s)

## Usage
```
usage: regress [-h] [-i IN] [-o OUT] [-p PATH] [-v] [-e] command

Run a program with multiple input files

positional arguments:
  command               Command to run with input files

optional arguments:
  -h, --help            show this help message and exit
  -i IN, --in IN        Input file prefix (default: in)
  -o OUT, --out OUT     Output file prefix (default: out)
  -p PATH, --path PATH  Path to input/output files (default: .)
  -v, --verbose         Increase output verbosity
  -e, --error           Change warnings to errors
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

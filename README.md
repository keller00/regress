# [Regression Test Utility](https://en.wikipedia.org/wiki/Regression_testing "Regression Testing")
Compare expected output(s) to actual output(s)

## Usage
```
usage: regress.py [-h] [-i IN] [-o OUT] [-p PATH] [-v] [-e] command

Run a program with multiple input files

positional arguments:
  command               Command to run with input files

optional arguments:
  -h, --help            show this help message and exit
  -i IN, --in IN        Input file prefix
  -o OUT, --out OUT     Output file prefix
  -p PATH, --path PATH  Path to input/output files
  -v, --verbose         Increase output verbosity
  -e, --error           Change warnings to errors

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

#!/usr/bin/python

# Imports
import argparse
import os
import glob
import subprocess

# Constants

COMMAND = ""
IN = ""
OUT = ""
VERBOSE = False
PATH = ""

# Verbose output
def debug(str):
    if VERBOSE:
        print str

parser = argparse.ArgumentParser(description='Run a program with multiple input files')
parser.add_argument('-i', '--in', help='Input file prefix', default='test')
parser.add_argument('-o', '--out', help='Output file prefix', default='out')
parser.add_argument('-p', '--path', help='Path to input/output files', default='.')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
parser.add_argument('command', help='command to run with input files')
args = vars(parser.parse_args())

# Set Constants
COMMAND = args['command']
IN = args['in']
OUT = args['out']
VERBOSE = args['verbose']
PATH = args['path']

debug(args)

# Find all input/output files
input_files = glob.glob(os.path.join(PATH , IN + '*'))
output_files = glob.glob(os.path.join(PATH , OUT + '*'))

debug("Checking path: " + os.path.join(PATH, IN + '*'))
debug("Detected input Files:")
debug(input_files)

# Make
for test in input_files:
    debug("Checking " + test + "'s output file")
    suffix = test.rsplit(IN)[-1]
    outpath = os.path.join(PATH, OUT + suffix)
    if not os.path.isfile(outpath):
        raise Exception("Output file does not exist: " + outpath)
    else:
        debug("Output file found: " + outpath)

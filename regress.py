#!/usr/bin/python

# Imports
import argparse
import os
import glob
import subprocess
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Constants
COMMAND = ""
IN = ""
OUT = ""
VERBOSE = False
PATH = ""
ERROR = False

def print_warning_error(msg):
	print bcolors.WARNING + msg
	if ERROR:
		print bcolors.FAIL + "Terminating Program."
		sys.exit()
	


# Verbose output
def debug(str):
    if VERBOSE:
        print str

parser = argparse.ArgumentParser(description='Run a program with multiple input files')
parser.add_argument('-i', '--in', help='Input file prefix', default='test')
parser.add_argument('-o', '--out', help='Output file prefix', default='out')
parser.add_argument('-p', '--path', help='Path to input/output files', default='.')
parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
parser.add_argument('-e', '--error', help='Change warnings to errors', action='store_true')
parser.add_argument('command', help='command to run with input files')
args = vars(parser.parse_args())

# Set Constants
COMMAND = args['command']
IN = args['in']
OUT = args['out']
VERBOSE = args['verbose']
PATH = args['path']
ERROR = args['error']

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
    	print_warning_error("Output file does not exist: " + outpath)
    else:
        debug("Output file found: " + outpath)

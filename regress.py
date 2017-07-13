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
    if ERROR:
        print bcolors.FAIL + msg
        sys.exit()
    print bcolors.WARNING + msg


def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

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
parser.add_argument('command', help='Command to run with input files')
args = vars(parser.parse_args())

# Set Constants
COMMAND = args['command']
IN = args['in']
OUT = args['out']
VERBOSE = args['verbose']
PATH = args['path']
ERROR = args['error']

debug(args)

# Check if command is valid
command = COMMAND.split(" ")[0]
debug("Checking if " + command + " is available...")
path_file = which(command) # Command is somewhere in path
local_file = os.path.isfile(command) # Command is a local file
if not (path_file or local_file):
    raise Exception("Command \"" + command + "\" does not exist")

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

    input = open(test)
    process = subprocess.Popen(COMMAND, stdin=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Read in expected output
    output = open(outpath).read()

    for i, (char1, char2) in enumerate(zip(output, stdout)):
        if char1 != char2:
            # Output differs from expected
            print_warning_error("Output of " + test + " differs from the expected output in " + outpath) # TODO Change this to warning/error
            break
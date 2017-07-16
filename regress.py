#!/usr/bin/python

# Imports
import argparse
import os
import glob
import subprocess
import sys

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_warnings(msg):
    print colors.WARNING + msg

def print_errors(msg):
    print colors.FAIL + msg

def print_errors_or_warnings(msg):
    if ERROR:
        print_errors(msg)
        return True
    else:
        print_warnings(msg)

def which(pgm):
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p

# Verbose output
def debug(string):
    if VERBOSE:
        print string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a program with multiple input files')
    parser.add_argument('-i', '--in', help='Input file prefix', default='in')
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
    path_file = which(command)  # Command is somewhere in path
    local_file = os.path.isfile(command)  # Command is a local file
    if not (path_file or local_file):
        print_errors("Command \"" + command + "\" does not exist")
        debug("Terminating Program.")
        exit()

    # Find all input/output files
    input_files = glob.glob(os.path.join(PATH, IN + '*'))
    output_files = glob.glob(os.path.join(PATH, OUT + '*'))

    debug("Checking path: " + os.path.join(PATH, IN + '*'))
    debug("Detected input Files:")
    debug(input_files)

    valid_pairs = []
    terminate_program = False

    # Make
    for test in input_files:
        debug("Checking " + test + "'s output file")
        suffix = test.rsplit(IN)[-1]
        outpath = os.path.join(PATH, OUT + suffix)
        if not os.path.isfile(outpath):
            terminate_program = terminate_program or print_errors_or_warnings("Output file does not exist: " + outpath)
        else:
            valid_pairs.append((test, outpath))
            debug("Output file found: " + outpath)

    if terminate_program:
        debug("Terminating Program.")
        exit()

    for test, outpath in valid_pairs:
        input_file = open(test)
        process = subprocess.Popen(COMMAND, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Read in expected output
        output = open(outpath).read()

        for i, (char1, char2) in enumerate(zip(output, stdout)):
            if char1 != char2:
                # Output differs from expected
                print_errors_or_warnings("Output of " + test + " differs from the expected output of " + outpath)
                break

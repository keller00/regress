#!/usr/bin/python

# Imports
import os
from sys import exit
from glob import glob
from pkg_resources import require
from subprocess import Popen, PIPE
from argparse import ArgumentParser

OPTIONS = {
    'COMMAND': None,
    'IN': '',
    'OUT': '',
    'VERBOSE': 0,
    'PATH': '.',
    'ERROR': False
}

VERSION = '1.0.0'


# Exceptions
class CommandNotFound(Exception):
    """Command is unavailable"""


class OutputNotFound(Exception):
    """There's an unmatched input file"""


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_warnings(msg):
    """Print yellow warning messages"""
    debug(0, Colors.WARNING + msg + Colors.ENDC)


def print_errors(msg):
    """Prints red error messages"""
    debug(0, Colors.FAIL + msg + Colors.ENDC)


def print_errors_or_warnings(msg):
    """Prints warning/error message depending on error flag"""
    if OPTIONS['ERROR']:
        print_errors(msg)
        return True
    else:
        print_warnings(msg)


def which(pgm):
    """
    Checks if a script is available in path
    :param pgm: string of scipt's name
    :return: string of path of script
    """
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p


# NOTE: Verbose output levels:
#   0 - default option; only output errors
#   1 - verbose for regular users; output successful results
#   2 - verbose for advanced users; output all information
def debug(level, string):
    """Prints debug mesages depending on current verbosity level"""
    if level <= OPTIONS['VERBOSE']:
        print string


def regress(command, in_prefix='in', out_prefix='out', path='.', verbose=0, error=False, options=list()):
    """
    Running regress test
    :param command: string of script
    :param in_prefix: string of input file prefix
    :param out_prefix: string of output file prefix
    :param path: string of path to input/output files
    :param verbose: verbosity level of regress
    :param error: error flag
    :param options: list of strings as options to the command
    :return: list of tuple of input file and actual output for each failed tests
    """
    # Set Constants
    OPTIONS['COMMAND'] = command
    OPTIONS['IN'] = in_prefix
    OPTIONS['OUT'] = out_prefix
    OPTIONS['VERBOSE'] = verbose
    OPTIONS['PATH'] = path
    OPTIONS['ERROR'] = error
    OPTIONS['OPTIONS'] = options

    # Check if command is valid
    command_no_args = OPTIONS['COMMAND'].split(" ")[0]
    debug(1, "Checking if %s is available..." % command_no_args)
    path_file = which(command_no_args)  # Command is somewhere in path
    local_file = os.path.isfile(command_no_args)  # Command is a local file
    if not (path_file or local_file):
        print_errors('Command %s not found' % command_no_args)
        raise CommandNotFound

    debug(2, "Checking path: %s" % os.path.join(OPTIONS['PATH'], OPTIONS['IN'] + '*'))
    input_files = glob(os.path.join(OPTIONS['PATH'], OPTIONS['IN'] + '*'))
    debug(1, "Detected input files: %s" % str(input_files))

    valid_pairs = []
    terminate_program = False

    for test in input_files:
        debug(2, "Checking %s's output file" % test)
        suffix = test.rsplit(OPTIONS['IN'])[-1]
        outpath = os.path.join(OPTIONS['PATH'], OPTIONS['OUT'] + suffix)
        if not os.path.isfile(outpath):
            terminate_program = terminate_program or print_errors_or_warnings(
                "Output file does not exist: %s" % outpath
            )
        else:
            valid_pairs.append((test, outpath))
            debug(2, "Output file found: " + outpath)

    if terminate_program:
        debug(2, "Terminating Program.")
        raise OutputNotFound

    failed_tests = []
    for test, outpath in valid_pairs:
        failed = False
        input_file = open(test)
        args = [OPTIONS['COMMAND']] + OPTIONS['OPTIONS']
        process = Popen(args, stdin=input_file, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        output = open(outpath).read()
        if len(output) != len(stdout):
            failed = True
        else:
            for i, (char1, char2) in enumerate(zip(output, stdout)):
                if char1 != char2:
                    failed = True
                    break
        if not failed:
            debug(1, 'Output of %s %s matches %s' % (OPTIONS['COMMAND'], test, outpath))
        elif failed:
            failed_tests.append((test, stdout))
            if print_errors_or_warnings('Output of %s differs from the expected output of %s' % (test, outpath)):
                return failed_tests
    return failed_tests


def main():
    # Parse arguments
    parser = ArgumentParser(description='Run a program with multiple input files')
    parser.add_argument('-i', '--in', help='Input file prefix (default: in)', default='in')
    parser.add_argument('-o', '--out', help='Output file prefix (default: out)', default='out')
    parser.add_argument('-p', '--path', help='Path to input/output files (default: .)', default='.')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='count', default=0)
    parser.add_argument('-e', '--error', help='Change warnings to errors', action='store_true')
    parser.add_argument('--version', action='version', help='Print current version number', version='regress version : %s' % VERSION)
    parser.add_argument('command', help='Command to run with input files')
    # TODO
    parser.add_argument('-a', help='Additional arguments for command', default='')
    args = vars(parser.parse_args())
    # Call regress
    try:
        regress(args['command'], args['in'], args['out'], args['path'], args['verbose'], args['error'], args['arguments'].split(' '))
    except CommandNotFound:
        exit(100)
    except OutputNotFound:
        exit(101)

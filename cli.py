import multiprocessing as mp
import json

import argparse
import tempfile
import sys
import os

# CLI

parser = argparse.ArgumentParser(
    prog='scoreboard-analyser',
    description='analyse EUC scoreboard screenshots',
    epilog='Report any bugs to <https://github.com/WellIDKRealy/EUC-Scoreboard-Analyser>')

parser.add_argument('scoreboard',
                    nargs='*',
                    help='scoreboard screenshots path')
parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='enables debug mode')
parser.add_argument('-s', '--silent',
                    action='store_true',
                    help='suepresses unnecessary output')
parser.add_argument('-b', '--batch',
                    action='store_true',
                    help='reads paths from stdin names')
parser.add_argument('-n', '--nproc',
                    default=mp.cpu_count(),
                    type=int,
                    help='number of processes. defaults to number of cpu\'s')

args = parser.parse_args()

# LOGGING/DEBUG

DEBUG = args.debug
LOG = not args.silent

def print_log(msg):
    if LOG:
        print(msg)

def print_debug(msg):
    if DEBUG:
        print(msg)

# END LOGGING/DEBUGGED

print_debug(args.scoreboard)

# END CLI

# Setup environment

NPROC = args.nproc
if NPROC <= 0:
    print_log('nproc needs to be >= 0')
    exit(1)


CWD = dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(CWD)

# OUTPUT_PARENT ='/tmp/scoreboard-analyser-output'
# if not os.path.isdir(OUTPUT_PARENT):
#     os.mkdir(OUTPUT_PARENT)

scoreboards = []
for scoreboard in args.scoreboard:
    if os.path.exists(scoreboard):
        scoreboards.append(scoreboard)
    else:
        print_log(f'No such file: {scoreboard}')

if scoreboards == [] and not args.batch:
    exit(2)

# END Setup environment

# MAIN

WORKER_NO = 0
def process_scoreboard(scoreboard):
    global WORKER_NO
    debug_output = tempfile.TemporaryDirectory(
        # dir=OUTPUT_PARENT
    ).name
    os.mkdir(debug_output)

    worker_no = WORKER_NO
    WORKER_NO += 1

    io = main.IO_DATA(LOG,
                      DEBUG,
                      print_debug,
                      worker_no)

    x = pool.apply(main.process_image,
                   (scoreboard, io))

    #,
    #                 callback=lambda res: print(res),
     #                error_callback=lambda e: print(e, file=sys.stderr))

with mp.Pool(NPROC) as pool:
    import main
    for scoreboard in scoreboards:
        process_scoreboard(scoreboard)

    if args.batch:
        while scoreboard := sys.stdin.readline():
            if os.path.exists(scoreboard):
                process_scoreboard(scoreboard)
            else:
                print_log(f'No such file: {scoreboard}')

# END MAIN

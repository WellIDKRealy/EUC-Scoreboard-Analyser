import multiprocessing as mp
import json

import argparse
import tempfile
import sys
import os
import traceback

from pathlib import Path

import main
import remote_reader

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
parser.add_argument('--debug-dir',
                    help='directory to which debug data is outputed')
parser.add_argument('--ocr-server',
                    help='ocr server address')
parser.add_argument('--ocr-authkey',
                    help='ocr server authkey')
parser.add_argument('--ocr-port',
                    default=2137,
                    type=int,
                    help='ocr server port')
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
        print(msg, file=sys.stderr)

def print_debug(msg):
    if DEBUG:
        print(msg, file=sys.stderr)

# END LOGGING/DEBUGGED

print_debug(args.scoreboard)

# END CLI

# Setup environment

NPROC = args.nproc
if NPROC <= 0:
    print_log('nproc needs to be >= 0')
    exit(1)


CWD = Path(__file__).parent
os.chdir(CWD)

OUTPUT_PARENT = Path(tempfile.gettempdir()) / 'scoreboard-analyser-output'
if args.debug_dir is not None:
    OUTPUT_PARENT = Path(args.debug_dir)

if not OUTPUT_PARENT.is_dir() and OUTPUT_PARENT.exists():
    print_log(f'{OUTPUT_PARENT} is not a directory!')
    exit(2)

if not OUTPUT_PARENT.exists():
    OUTPUT_PARENT.mkdir()

scoreboards = []
for scoreboard in args.scoreboard:
    real_path = Path(scoreboard).absolute()
    if real_path.exists():
        scoreboards.append(real_path)
    else:
        print_log(f'No such file: {real_path}')

if scoreboards == [] and not args.batch:
    exit(3)

# END Setup environment

# MAIN

OUT = []
WORKER_NO = 0
def process_scoreboard(scoreboard, reader):
    global WORKER_NO
    debug_output = Path(tempfile.TemporaryDirectory(dir=OUTPUT_PARENT).name)
    debug_output.mkdir()

    worker_no = WORKER_NO
    WORKER_NO += 1

    io = main.IO_DATA(LOG,
                      DEBUG,
                      debug_output,
                      worker_no)

    pool.apply_async(main.process_image,
                     (scoreboard, reader, io),
                     callback=lambda res: OUT.append(res),
                     error_callback=lambda e: traceback.print_exception(e))

reader = None if args.ocr_server is None else remote_reader.Reader(args.ocr_server, args.ocr_port, args.ocr_authkey)

with mp.Pool(NPROC) as pool:
    for scoreboard in scoreboards:
        process_scoreboard(scoreboard, reader)

    if args.batch:
        while scoreboard := sys.stdin.readline():
            scoreboard = scoreboard[:-1]
            real_path = Path(scoreboard).absolute()
            if real_path.exists():
                process_scoreboard(real_path, reader)
            else:
                print_log(f'No such file: {scoreboard}')

    pool.close()
    pool.join()

print(json.dumps(OUT))
# END MAIN

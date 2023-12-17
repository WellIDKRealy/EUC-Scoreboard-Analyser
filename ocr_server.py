from multiprocessing import Queue, Process, cpu_count, freeze_support
from multiprocessing.connection import Listener
from traceback import print_exception

import argparse

parser = argparse.ArgumentParser(
    prog='ocr-server',
    description='OCR Server of EUC scoreboard screenshot analyser',
    epilog='Report any bugs to <https://github.com/WellIDKRealy/EUC-Scoreboard-Analyser>')

parser.add_argument('-a', '--address',
                    default='0.0.0.0',
                    help='server address')
parser.add_argument('-p', '--port',
                    default=2137,
                    type=int,
                    help='server port')
parser.add_argument('-k', '--authkey',
                    default='123',
                    help='authentication key')

args = parser.parse_args()

ADDRESS = (args.address, args.port)
AUTHKEY = args.authkey.encode('utf-8')

# Moved down as it takes long time to load
import easyocr

connection_queue = Queue()

def dispatcher(address, authkey):
    global connection_queue
    print('[Dispatcher] Started')
    with Listener(address, authkey=authkey) as listener:
        while True:
            try:
                connection_queue.put(listener.accept())
            except Exception as e:
                print_exception(e)


def queue_process(index):
    global connection_queue
    print(f'[{index}] Started process')

    reader = easyocr.Reader(['en'])

    while True:
        try:
            conn = connection_queue.get()
            print(f'[{index}] Established connection')
            with conn as conn:
                try:
                    data = conn.recv()
                    answer = reader.readtext(data[0], *data[1], **data[2])
                    conn.send(answer)
                except Exception as e:
                    print_exception(e)
                    conn.send(e)
            print(f'[{index}] Ended connection')
        except Exception as e:
            print_exception(e)


if __name__ = '__maim__':
    freeze_support()
    dispatcher_p = Process(target=dispatcher, args=(ADDRESS, AUTHKEY))
    queue_proceses = [Process(target=queue_process, args=(i, ))
                      for i in range(cpu_count())]

    dispatcher_p.start()
    for p in queue_proceses:
        p.start()


    input("TO STOP PRESS ENTER\n")

    dispatcher_p.terminate()
    for p in queue_proceses:
        p.terminate()

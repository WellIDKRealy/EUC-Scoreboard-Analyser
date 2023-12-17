from multiprocessing.connection import Client

class ReaderData:
    def __init__(self, img, args, kwargs):
        self.img = img
        self.args = args
        self.kwargs = kwargs

class Reader:
    def __init__(self, address, port, authkey):
        self.address = (address, port)
        if authkey is None:
            self.authkey = authkey
        else:
            self.authkey = authkey.encode('utf-8')

    def readtext(self, img, *args, **kwargs):
        with Client(self.address, authkey=self.authkey) as conn:
            conn.send((img, args, kwargs))
            return conn.recv()

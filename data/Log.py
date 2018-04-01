from io import BufferedReader
import time

class Log:

    def __init__(self, file_handle: BufferedReader):
        if not file_handle.readable():
            raise IOError("File handle for logfile is not readable!")
        self.file = file_handle
        self.initialize()  # to be used later

    def initialize(self):
        self.data = self.file.read()  # bytes

    def __getitem__(self, item):
        def to_time(byte_array):
            return time.ctime(int.from_bytes(byte_array, "big"))

        if item > len(self):
            raise IndexError
        list_item = self.data[item * 8:(item + 1) * 8]
        result = {"id": list_item[:4].hex().upper(), "timestamp": to_time(list_item[4:])}
        return result

    __setitem__ = None

    def __len__(self):
        return int(len(self.data)/8) - 1

    def close(self):
        self.file.close()
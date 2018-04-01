import csv
from io import BufferedReader


class Database:

    def __init__(self, file_handle: BufferedReader):
        if not (file_handle.readable() and file_handle.writable()):
            raise IOError("File handle for database is not readable nor writable!")
        self.file = file_handle
        self.columns = ("id", "name", "type")
        self.initialize()

    def initialize(self):
        self.data = list(csv.DictReader(self.file))
        self.writer = csv.DictWriter(self.file, self.columns)

    def close(self):
        self.file.close()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def index(self, item):
        for i, row in enumerate(self.data):
            if row["id"] == item:
                return i
        raise ValueError
import csv

from data.Database import Database
from data.Log import Log
from tkinter import font as tkFont

class AppModel:

    def __init__(self):
        self._log = None
        self._db = None
        self.log_items = []
        self.db_items = []

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, val):
        f = Log(val)
        if self._log is not None:
            self._log.close()
        self._log = f

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, val):
        f = Database(val)
        if self._db is not None:
            self._db.close()
        self._db = f

    def close_files(self):
        if self._db is not None:
            self._db.close()
        if self._log is not None:
            self._log.close()

    def _build_tree(self, tree, attr_curr_items_ids, items, item_indexes, columns):

        tree.delete(*getattr(self, attr_curr_items_ids))
        setattr(self, attr_curr_items_ids, [])
        for i, item in enumerate(items):
            values = [i + 1] + [item[k] for k in item_indexes]
            getattr(self, attr_curr_items_ids).append(tree.insert("", "end", values=values))
            for j, val in enumerate(values):
                col_w = tkFont.Font().measure(val)
                if tree.column(columns[j], width=None) < col_w:
                    tree.column(columns[j], minwidth=0, width=col_w)

    def zip_log_db(self):
        for i in self._log:
            try:
                index = self._db.index(i["id"])
            except ValueError:
                yield dict(i, **{"name": "", "type": ""})
            else:
                yield dict(i, **{j: self._db[index][j] for j in ("name", "type")})

    def register_log_tree(self, tree, columns):
        self._log_tree = tree
        self._log_columns = columns

    def register_db_tree(self, tree, columns):
        self._db_tree = tree
        self._db_columns = columns

    def build_log_tree(self):
        if self._db is None:
            self._build_tree(self._log_tree, "log_items", self._log, ("id", "timestamp"), self._log_columns)
        else:
            self._build_tree(self._log_tree, "log_items", self.zip_log_db(), ("id", "timestamp", "name", "type"), self._log_columns)

    def build_db_tree(self):
        self._build_tree(self._db_tree, "db_items", self._db, ("id", "name", "type"), self._db_columns)
        if self._log is not None:
            self.build_log_tree()
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from tkinter import font as tkFont
from AppModel import AppModel


class DatabaseView(tk.Frame):
    def __init__(self, model: AppModel, master=None):
        assert model is not None
        self.model = model

        super().__init__(master=master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_widgets()

    def create_widgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.load_db_button = tk.Button(self, text='Load a database file...', command=self.load_db,
                                        width=len('Load a database file...'))
        self.load_db_button.grid(column=0, row=0, sticky="nwse", rowspan=2)

        self.collumns = ("No.", "Key ID", "Name", "Type", "Class")
        self.tree = ttk.Treeview(self, columns=self.collumns, show="headings")
        vsb = ttk.Scrollbar(self, orient="vertical",
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in self.collumns:
            self.tree.heading(col, text=col)

        self.tree.column(self.collumns[0], width=tkFont.Font().measure("No."))
        self.tree.column(self.collumns[1], width=tkFont.Font().measure("Key ID"))
        self.tree.column(self.collumns[2], width=tkFont.Font().measure("Name"))

        vsb.grid(column=2, row=0, sticky='ns')
        hsb.grid(column=1, row=1, sticky='ew')
        self.tree.grid(column=1, row=0, sticky="nswe")

        self.model.register_db_tree(self.tree, self.collumns)

    def load_db(self):
        options = {}
        options['filetypes'] = [("Comma Separated Values", "*.csv"), ("All files", "*.*")]
        options['initialfile'] = "db.csv"
        options['title'] = "Open database file..."
        p = filedialog.askopenfilename(**options)
        if p != "":
            try:
                self.model.db = open(p, "r+", encoding="utf-8")
            except IOError as e:
                messagebox.showerror(title="IOError", message=str(e))
            else:
                self.master.busy()
                self.update()
                self.model.build_db_tree()
                self.master.not_busy()

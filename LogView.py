import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
from AppModel import AppModel


class LogView(tk.Frame):
    def __init__(self, model: AppModel, master=None):
        assert model is not None
        self.model = model

        super().__init__(master=master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_widgets()

    def create_widgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.load_log_button = tk.Button(self, text='Load a log file...', command=self.load_log, width=len('Load a log file...'))
        self.load_log_button.grid(column=0, row=0, sticky="nwse", rowspan=2)

        self.collumns = ("No.", "Key ID", "Time", "Name", "Type")
        self.tree = ttk.Treeview(self, columns=self.collumns, show="headings")
        vsb = ttk.Scrollbar(self, orient="vertical",
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal",
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in self.collumns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=tkFont.Font().measure(col))

        vsb.grid(column=2, row=0, sticky='ns')
        hsb.grid(column=1, row=1, sticky='ew')
        self.tree.grid(column=1, row=0, sticky="nswe")

        self.model.register_log_tree(self.tree, self.collumns)

    def load_log(self):
        options = {}
        options['filetypes'] = [("Log files", "*.LOG"), ("All files", "*.*")]
        options['initialfile'] = "LOGFILE.LOG"
        options['title'] = "Open log file..."
        p = filedialog.askopenfilename(**options)
        if p != "":
            try:
                self.model.log = open(p, "rb")
            except IOError as e:
                messagebox.showerror(title="IOError", message=str(e))
            else:
                self.master.busy()
                self.update()
                self.model.build_log_tree()
                self.master.not_busy()

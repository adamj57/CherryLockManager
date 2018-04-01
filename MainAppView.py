import tkinter as tk
from tkinter import ttk
from AppModel import AppModel
from DatabaseView import DatabaseView
from LogView import LogView


class MainAppView(tk.Frame):
    def __init__(self, model: AppModel, master=None):
        self.model = model

        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.create_widgets()
        self.master.geometry("750x400")

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)

        self.log_view = LogView(self.model, master=self)
        self.database_view = DatabaseView(self.model, master=self)

        self.notebook.add(self.log_view, text="Log")
        self.notebook.add(self.database_view, text="Database")

        self.notebook.add(tk.Frame(), text="Test Arduino Conncetivity")
        self.notebook.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)

    def busy(self):
        self.master.config(cursor="wait")

    def not_busy(self):
        self.master.config(cursor="")

    def quit(self):
        self.model.close_files()
        super().quit()

if __name__ == '__main__':
    app = MainAppView(AppModel())
    app.master.title('CherryLock Manager')
    app.mainloop()

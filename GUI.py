import tkFileDialog
import tkMessageBox
from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar
import pandas as pd


class KMeansClustering:

    df = pd.DataFrame({})

    def __init__(self, master):
        self.path = None
        self.master = master
        master.title("KMeansClustering")

        self.total = 0
        self.entered_number = 0

        # define path label:
        self.var_path_label = StringVar()
        self.var_path_label.set("Data path:")
        self.path_label = Label(root, textvariable=self.var_path_label)

        # define num of cluster label:
        self.var_cluster_label = StringVar()
        self.var_cluster_label.set("Num of clusters k:")
        self.cluster_label = Label(root, textvariable=self.var_cluster_label)

        # define num of runs label:
        self.var_runs_label = StringVar()
        self.var_runs_label.set("Num of runs:")
        self.runs_label = Label(root, textvariable=self.var_runs_label)

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        vcmd_path = master.register(self.validate_path) # we have to wrap the command
        vcmd_number = master.register(self.validate)

        self.path_entry = Entry(master, validate="focusout", validatecommand=(vcmd_path, '%P'))
        self.cluster_entry = Entry(master, validate="key", validatecommand=(vcmd_number, '%P'))
        self.runs_entry = Entry(master, validate="key", validatecommand=(vcmd_number, '%P'))

        self.Browse_button = Button(master, text="Browse", command=lambda: self.browse())
        self.cluster_button = Button(master, text="Cluster", command=lambda: self.update("subtract"))
        self.preProcess_button = Button(master, text="Pre-process", command=lambda: self.update("reset"))

        # LAYOUT

        self.path_label.grid(row=0, column=0, sticky=W)
        self.cluster_label.grid(row=1, column=0, sticky=W)
        self.runs_label.grid(row=2, column=0, sticky=W)

        self.path_entry.grid(row=0, column=1, columnspan=3, sticky=W+E)
        self.cluster_entry.grid(row=1, column=1, columnspan=1, sticky=W+E)
        self.runs_entry.grid(row=2, column=1, columnspan=1, sticky=W+E)

        self.Browse_button.grid(row=0, column=4)
        self.preProcess_button.grid(row=3, column=1, sticky=W+E)
        self.cluster_button.grid(row=4, column=1)

    # browse for data path
    def browse(self):
        self.path = tkFileDialog.askopenfilename()
        if self.path:
            self.path_entry.delete(0, END)
        self.path_entry.insert(0, self.path)
        if not self.path:
            tkMessageBox.showinfo("K Means Clustering", "Please choose data file")
            return
        if not (self.path[-5:] == ".xlsx" or self.path[-4:] == ".xls"):
            tkMessageBox.showinfo("K Means Clustering", "Please choose excel file")
            self.path_entry.delete(0, END)
            return
        self.df = pd.read_excel(self.path)

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def validate_path(self, new_text):
        self.path = new_text
        if not self.path:
            tkMessageBox.showinfo("K Means Clustering", "Please choose data file")
            return
        if not (self.path[-5:] == ".xlsx" or self.path[-4:] == ".xls"):
            tkMessageBox.showinfo("K Means Clustering", "Please choose excel file")
            self.path_entry.delete(0, END)
            return
        self.df = pd.read_excel(self.path)

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else:  # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.path_entry.delete(0, END)

root = Tk()
my_gui = KMeansClustering(root)
root.mainloop()

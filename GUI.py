import tkFileDialog
import tkMessageBox
from Tkinter import Tk, Label, Button, Entry, END, W, E, StringVar
from Cluster import *
from PreProcess import *
import pandas as pd
from PIL import Image, ImageTk


class KMeansClustering:

    df = pd.DataFrame({})

    def __init__(self, master):

        # attributes
        self.path = None
        self.num_of_clusters = 0
        self.num_of_runs = 0
        self.master = master
        self.is_processed = False
        master.title("KMeansClustering")

        # define path label:
        self.var_path_label = StringVar()
        self.var_path_label.set("Data path:")
        self.path_label = Label(root, textvariable=self.var_path_label)

        # define num of clusters label:
        self.var_cluster_label = StringVar()
        self.var_cluster_label.set("Num of clusters k:")
        self.cluster_label = Label(root, textvariable=self.var_cluster_label)

        # define num of runs label:
        self.var_runs_label = StringVar()
        self.var_runs_label.set("Num of runs:")
        self.runs_label = Label(root, textvariable=self.var_runs_label)

        vcmd_path = master.register(self.validate_path)
        vcmd_number = master.register(self.validate)

        self.path_entry = Entry(master, validate="focusout", validatecommand=(vcmd_path, '%P'))
        self.cluster_entry = Entry(master, validate="key", validatecommand=(vcmd_number, '%P'))
        self.runs_entry = Entry(master, validate="key", validatecommand=(vcmd_number, '%P'))

        self.Browse_button = Button(master, text="Browse", command=lambda: self.browse())
        self.cluster_button = Button(master, text="Cluster", command=lambda: self.k_means())
        self.preProcess_button = Button(master, text="Pre-process", command=lambda: self.pre_process())

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

        if not (self.path[-5:] == ".xlsx" or self.path[-4:] == ".xls"):
            tkMessageBox.showinfo("K Means Clustering", "Please choose excel file")
            self.path_entry.delete(0, END)
            return
        if not self.path:
            tkMessageBox.showinfo("K Means Clustering", "Please choose data file")
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

    def pre_process(self):  # todo: need maybe try - except???
        # pre process the df
        preP = PreProcess(self.df)
        self.df = preP.df
        self.is_processed = True
        tkMessageBox.showinfo("K Means Clustering", "Preprocessing completed successfully!")
        pass

    def k_means(self):
        if not self.is_processed:
            tkMessageBox.showerror("K Means Clustering", "You need to pre-process the data before clustering")
            return
        # check values of runs and cluster numbers
        try:
            n_runs = self.runs_entry.get()
            n_clusters = self.cluster_entry.get()
            if n_runs == "" or n_clusters == "":
                tkMessageBox.showerror("K Means Clustering", "You have to insert numbers")
                return
            n_clusters = int(n_clusters)
            n_runs = int(n_runs)
            if n_clusters <= 0:
                tkMessageBox.showerror("K Means Clustering", "Number of clusters must be positive")
                return

            if n_runs <= 0:
                tkMessageBox.showerror("K Means Clustering", "Number of runs must be positive")
                return
            if n_clusters > len(self.df):
                tkMessageBox.showerror("K Means Clustering", "The number of clusters is too big")
                return


        except Exception:
            tkMessageBox.showerror("K Means Clustering", "Invalid numbers")
            return

        # create cluster object
        k_means = Cluster(self.df, n_clusters, n_runs)
        self.df = k_means.df

        # create label for scatter image and layout
        scatter_img = ImageTk.PhotoImage(Image.open('scatter.png'))
        self.scatter_label = Label(self.master, image=scatter_img)
        self.scatter_label.image = scatter_img
        self.scatter_label.grid(row=6, column=0, columnspan=10)

        horopleth_img = ImageTk.PhotoImage(Image.open('horopleth.png'))
        self.horopleth_label = Label(self.master, image=horopleth_img)
        self.horopleth_label.image = horopleth_img
        self.horopleth_label.grid(row=6, column=10, columnspan=10)

        tkMessageBox.showinfo("K Means Clustering", "Clustering completed successfully!")

root = Tk()
my_gui = KMeansClustering(root)
root.mainloop()

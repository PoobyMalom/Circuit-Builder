import tkinter as tk
from tkinter import ttk
from file_loader import FileLoader
from file_saver import FileSaver

class Toolbar:
    def __init__(self, parent_frame, window):
        self.frame = tk.Frame(parent_frame, height=30, bg="darkgray")
        self.frame.pack(side="bottom", fill="x")

        self.window = window  # reference to main window logic if needed

        style = ttk.Style()
        style.theme_use('default')

        style.configure(
            "Toolbar.TButton",
            background="#1897d6",
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=6,
            relief="flat"
        )

        style.map(
            "Toolbar.TButton",
            background=[('active', '#1580b7'), ('!active', '#1897d6')],
            foreground=[('disabled', 'gray'), ('!disabled', 'white')]
        )

        self.file_button = ttk.Button(
            self.frame,
            text="File",
            style="Toolbar.TButton",
            command=self.show_file_menu
        )
        self.file_button.pack(side="left", padx=0)

        self.and_button = ttk.Button(
            self.frame,
            text="AND",
            style="Toolbar.TButton",
            command=self.place_and
        )
        self.and_button.pack(side="left", padx=0)

        self.not_button = ttk.Button(
            self.frame,
            text="NOT",
            style="Toolbar.TButton",
            command=self.place_not
        )
        self.not_button.pack(side="left", padx=0)

        self.file_menu = tk.Menu(self.frame, tearoff=0, relief='flat', background="#1897d6", foreground="#1897d6")
        self.file_menu.add_command(label='New File', command=self.new_file)
        self.file_menu.add_command(label='Open...', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)

 
    def show_file_menu(self):
        x = self.file_button.winfo_rootx()
        y = self.file_button.winfo_rooty() + self.file_button.winfo_height()
        self.file_menu.tk_popup(x, y)
        self.file_menu.grab_release()

    def new_file(self):
        print("New file")

    def open_file(self):
        FileLoader("test.json", self.window.circuit, self.window.canvas, self.window)

    def save_file(self):
        FileSaver("test.json", self.window.circuit, 'NAND')

    def place_and(self):
        self.window.add_component("AND")

    def place_not(self):
        self.window.add_component("NOT")
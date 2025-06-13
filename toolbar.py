"""Module to define toolbar gui aspects and buttons"""

import tkinter as tk
from tkinter import ttk
from file_loader import FileLoader
from file_saver import FileSaver


class Toolbar:
    """Constructor class for toolbar"""

    def __init__(self, parent_frame, window):
        self.frame = tk.Frame(parent_frame, height=30, bg="darkgray")
        self.frame.pack(side="bottom", fill="x")

        self.window = window  # reference to main window logic if needed

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Toolbar.TButton",
            background="#1897d6",
            foreground="white",
            borderwidth=0,
            focusthickness=0,
            padding=6,
            relief="flat",
        )

        style.map(
            "Toolbar.TButton",
            background=[("active", "#1580b7"), ("!active", "#1897d6")],
            foreground=[("disabled", "gray"), ("!disabled", "white")],
        )

        self.file_button = ttk.Button(
            self.frame,
            text="File",
            style="Toolbar.TButton",
            command=self.show_file_menu,
        )
        self.file_button.pack(side="left", padx=0)

        self.and_button = ttk.Button(
            self.frame, text="AND", style="Toolbar.TButton", command=self.place_and
        )
        self.and_button.pack(side="left", padx=0)

        self.not_button = ttk.Button(
            self.frame, text="NOT", style="Toolbar.TButton", command=self.place_not
        )
        self.not_button.pack(side="left", padx=0)

        self.file_menu = tk.Menu(
            self.frame,
            tearoff=0,
            relief="flat",
            background="#1897d6",
            foreground="#1897d6",
        )
        self.file_menu.add_command(label="New File", command=self.new_file)
        self.file_menu.add_command(label="Open...", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)

    def show_file_menu(self):
        """Logic when file menu pressed"""
        x = self.file_button.winfo_rootx()
        y = self.file_button.winfo_rooty() + self.file_button.winfo_height()
        self.file_menu.tk_popup(x, y)
        self.file_menu.grab_release()

    def new_file(self):
        """Logic for pressing new_file"""
        # TODO add actual logic for creating a new file. clear canvas -> clear circuit ->
        # Reset all the lookup dicts and other bullshit
        print("New file")

    def open_file(self):
        """Logic when open_file pressed"""
        FileLoader("test.json", self.window.circuit, self.window.canvas, self.window)

    def save_file(self):
        """Logic when save_file pressed"""
        FileSaver("test.json", self.window.circuit, "NAND")

    def place_and(self):
        """Logic to place and block"""
        self.window.add_component("AND")

    def place_not(self):
        """Logic to place not block"""
        self.window.add_component("NOT")

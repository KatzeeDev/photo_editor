import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import BACKGROUND_COLOR
import os

class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.import_func = import_func
        ctk.CTkButton(self, text="Abrir Imagen", command=self.open_dialog).pack(
            expand=True
        )

    def open_dialog(self):
        initial_dir = os.path.join(os.path.dirname(__file__), 'images')
        path = filedialog.askopenfilename(initialdir=initial_dir)
        if path:
            self.import_func(path)

class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="ridge")
        self.bind("<Configure>", resize_image)
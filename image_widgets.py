import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import BACKGROUND_COLOR
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
import os
from effects import apply_effect, sepia_effect


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky="nsew")
        self.import_func = import_func
        ctk.CTkButton(self, text="Abrir Imagen", command=self.open_dialog).pack(
            expand=True
        )

    def open_dialog(self):
        initial_dir = os.path.join(os.path.dirname(__file__), "images")
        path = filedialog.askopenfilename(initialdir=initial_dir)
        if path:
            self.import_func(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(
            master=parent,
            background=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.bind("<Configure>", resize_image)


class ImageEditor:
    def __init__(self, image):
        self.original_image = image
        self.edited_image = self.original_image.copy()

    def apply_brightness_contrast(self, brightness, contrast):
        self.edited_image = self.original_image.copy()
        brightness_enhancer = ImageEnhance.Brightness(self.edited_image)
        self.edited_image = brightness_enhancer.enhance(brightness)
        contrast_enhancer = ImageEnhance.Contrast(self.edited_image)
        self.edited_image = contrast_enhancer.enhance(contrast)

    def apply_effect(self, effect):
        self.edited_image = apply_effect(self.edited_image, effect)

    def get_edited_image(self):
        return self.edited_image

    def reset_image(self):
        self.edited_image = self.original_image.copy()

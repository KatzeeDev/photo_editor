import customtkinter as ctk
from image_widgets import ImageImport, ImageOutput
from PIL import Image, ImageTk
import os

class App(ctk.CTk):
    def __init__(self):
        # Configuración inicial
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.title("Editor de Fotos 🐈")
        self.minsize(800, 500)

        # Configuración del diseño
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # Widgets
        self.image_import = ImageImport(self, self.import_image)

        # Iniciar la aplicación
        self.mainloop()

    def import_image(self, path):
        try:
            self.original_image = Image.open(path)
            self.image_import.grid_forget()
            self.image_output = ImageOutput(self, self.resize_image)
            self.image_output.grid(row=0, column=0, columnspan=2, sticky="nsew")
            # Iniciar el redimensionamiento
            self.resize_image(self.image_output.winfo_width(), self.image_output.winfo_height())
        except Exception as e:
            print(f"Error al importar la imagen: {e}")
            # Aquí podrías mostrar un mensaje de error al usuario

    def resize_image(self, event):
        # Obtener dimensiones del canvas y la imagen
        canvas_width, canvas_height = event.width, event.height
        image_width, image_height = self.original_image.size

        # Calcular proporciones
        canvas_ratio = canvas_width / canvas_height
        image_ratio = image_width / image_height

        # Determinar el factor de escala
        if canvas_ratio > image_ratio:
            scale = canvas_height / image_height
        else:
            scale = canvas_width / image_width

        # Calcular nuevo tamaño y redimensionar
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)

        # Crear nueva imagen para Tkinter
        self.image_tk = ImageTk.PhotoImage(resized_image)

        # Calcular posición central
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2

        # Actualizar canvas
        self.image_output.delete("all")
        self.image_output.create_image(x, y, anchor="nw", image=self.image_tk)

App()
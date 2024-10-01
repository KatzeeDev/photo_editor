import customtkinter as ctk
from image_widgets import ImageImport, ImageOutput, ImageEditor
from text_manager import TextOverlay
from PIL import Image, ImageTk
from tkinter import filedialog


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.title("Editor de Fotos 🐈")
        self.minsize(800, 500)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=2)

        self.image_import = ImageImport(self, self.import_image)

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.tabview = ctk.CTkTabview(self.menu_frame, width=180)
        self.tabview.pack(padx=20, pady=(20, 10), expand=True, fill="both")

        self.tabview.add("Brillo")
        self.tabview.add("Contraste")
        self.tabview.add("Efectos")
        self.tabview.add("Texto")
        self.tabview.add("Exportar")

        # Brillo
        ctk.CTkLabel(self.tabview.tab("Brillo"), text="Ajustar brillo:").pack(
            pady=(10, 0)
        )
        self.brightness_slider = ctk.CTkSlider(
            self.tabview.tab("Brillo"), from_=0.5, to=2, command=self.apply_effects
        )
        self.brightness_slider.set(1)
        self.brightness_slider.pack(pady=10)

        # Contraste
        ctk.CTkLabel(self.tabview.tab("Contraste"), text="Ajustar contraste:").pack(
            pady=(10, 0)
        )
        self.contrast_slider = ctk.CTkSlider(
            self.tabview.tab("Contraste"), from_=0.5, to=2, command=self.apply_effects
        )
        self.contrast_slider.set(1)
        self.contrast_slider.pack(pady=10)

        # Botones para efectos
        effects = [
            ("Blanco y Negro", "bw"),
            ("Sepia", "sepia"),
            ("Invertir Colores", "invert"),
            ("Desenfoque", "blur"),
            ("Realce de Bordes", "edge_enhance"),
        ]
        for effect_name, effect_value in effects:
            btn = ctk.CTkButton(
                self.tabview.tab("Efectos"),
                text=effect_name,
                command=lambda ev=effect_value: self.apply_effect(ev),
            )
            btn.pack(pady=5)

        # Pestaña de Texto
        self.text_entry = ctk.CTkEntry(
            self.tabview.tab("Texto"), placeholder_text="Ingrese texto"
        )
        self.text_entry.pack(pady=10)

        ctk.CTkLabel(self.tabview.tab("Texto"), text="Color del texto:").pack()
        self.text_color = ctk.StringVar(value="white")
        self.color_menu = ctk.CTkOptionMenu(
            self.tabview.tab("Texto"),
            values=["white", "black", "red", "green", "blue"],
            variable=self.text_color,
        )
        self.color_menu.pack(pady=10)

        ctk.CTkLabel(self.tabview.tab("Texto"),
                     text="Posición del texto:").pack()
        self.text_position = ctk.StringVar(value="center")
        self.position_menu = ctk.CTkOptionMenu(
            self.tabview.tab("Texto"),
            values=["top", "center", "bottom"],
            variable=self.text_position,
        )
        self.position_menu.pack(pady=10)

        ctk.CTkLabel(self.tabview.tab("Texto"),
                     text="Tamaño de fuente:").pack()
        self.font_size = ctk.IntVar(value=20)
        self.font_size_slider = ctk.CTkSlider(
            self.tabview.tab("Texto"),
            from_=10,
            to=100,
            variable=self.font_size,
            command=self.update_text,
        )
        self.font_size_slider.pack(pady=10)

        ctk.CTkLabel(self.tabview.tab("Texto"), text="Ancho del borde:").pack()
        self.outline_width = ctk.IntVar(value=0)
        self.outline_slider = ctk.CTkSlider(
            self.tabview.tab("Texto"),
            from_=0,
            to=10,
            variable=self.outline_width,
            command=self.update_text,
        )
        self.outline_slider.pack(pady=10)

        ctk.CTkLabel(self.tabview.tab("Texto"),
                     text="Posición vertical:").pack()
        self.vertical_position = ctk.DoubleVar(value=0.5)
        self.vertical_slider = ctk.CTkSlider(
            self.tabview.tab("Texto"),
            from_=0,
            to=1,
            variable=self.vertical_position,
            command=self.update_text,
        )
        self.vertical_slider.pack(pady=10)

        ctk.CTkLabel(self.tabview.tab("Texto"),
                     text="Posición horizontal:").pack()
        self.horizontal_position = ctk.DoubleVar(value=0.5)
        self.horizontal_slider = ctk.CTkSlider(
            self.tabview.tab("Texto"),
            from_=0,
            to=1,
            variable=self.horizontal_position,
            command=self.update_text,
        )
        self.horizontal_slider.pack(pady=10)

        self.add_text_button = ctk.CTkButton(
            self.tabview.tab("Texto"),
            text="Añadir/Actualizar Texto",
            command=self.add_text,
        )
        self.add_text_button.pack(pady=10)

        self.delete_text_button = ctk.CTkButton(
            self.tabview.tab("Texto"), text="Eliminar Texto", command=self.delete_text
        )
        self.delete_text_button.pack(pady=10)

        # Pestaña de Exportar
        export_formats = [("PNG", ".png"), ("JPEG", ".jpg")]
        for format_name, format_extension in export_formats:
            btn = ctk.CTkButton(
                self.tabview.tab("Exportar"),
                text=f"Exportar como {format_name}",
                command=lambda ext=format_extension: self.save_image(ext),
            )
            btn.pack(pady=5)

        # Botón Restablecer fuera de las pestañas
        self.reset_button = ctk.CTkButton(
            self.menu_frame, text="Restablecer", command=self.reset_image
        )
        self.reset_button.pack(pady=(10, 20), padx=20, fill="x")

        self.image_editor = None
        self.image_output = None
        self.text_overlay = None

        self.mainloop()

    def import_image(self, path):
        try:
            image = Image.open(path)
            self.image_editor = ImageEditor(image)
            self.text_overlay = TextOverlay(image.size)

            if self.image_output:
                self.image_output.grid_forget()

            self.image_output = ImageOutput(self, self.resize_image)
            self.image_output.grid(row=0, column=0, sticky="nsew")

            self.resize_image(event=None)
        except Exception as e:
            print(f"Error al importar la imagen: {e}")

    def resize_image(self, event):
        if self.image_editor:
            canvas_width = self.image_output.winfo_width()
            canvas_height = self.image_output.winfo_height()

            image = self.image_editor.get_edited_image()
            image_width, image_height = image.size
            canvas_ratio = canvas_width / canvas_height
            image_ratio = image_width / image_height

            if canvas_ratio > image_ratio:
                scale = canvas_height / image_height
            else:
                scale = canvas_width / image_width

            new_width = int(image_width * scale)
            new_height = int(image_height * scale)

            resized_image = image.resize(
                (new_width, new_height), Image.LANCZOS)
            resized_overlay = self.text_overlay.get_overlay().resize(
                (new_width, new_height), Image.LANCZOS
            )

            combined_image = Image.alpha_composite(
                resized_image.convert("RGBA"), resized_overlay
            )

            self.image_tk = ImageTk.PhotoImage(combined_image)

            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2

            self.image_output.delete("all")
            self.image_output.create_image(
                x, y, anchor="nw", image=self.image_tk)

    def apply_effects(self, _):
        if self.image_editor:
            brightness_value = self.brightness_slider.get()
            contrast_value = self.contrast_slider.get()
            self.image_editor.apply_brightness_contrast(
                brightness_value, contrast_value
            )
            self.resize_image(event=None)

    def apply_effect(self, effect):
        if self.image_editor:
            self.image_editor.apply_effect(effect)
            self.resize_image(event=None)

    def add_text(self):
        self.update_text()

    def update_text(self, _=None):
        if self.image_editor and self.text_overlay:
            text = self.text_entry.get()
            color = self.text_color.get()
            position = self.text_position.get()
            font_size = self.font_size.get()
            outline_width = self.outline_width.get()
            vertical_pos = self.vertical_position.get()
            horizontal_pos = self.horizontal_position.get()

            self.text_overlay.clear()
            self.text_overlay.add_text(
                text,
                position,
                color,
                font_size,
                outline_width,
                vertical_pos,
                horizontal_pos,
            )
            self.resize_image(event=None)

    def delete_text(self):
        if self.text_overlay:
            self.text_overlay.clear()
            self.text_entry.delete(0, "end")
            self.resize_image(event=None)

    def reset_image(self):
        if self.image_editor:
            self.image_editor.reset_image()
            self.text_overlay.clear()
            self.brightness_slider.set(1)
            self.contrast_slider.set(1)
            self.font_size.set(20)
            self.outline_width.set(0)
            self.vertical_position.set(0.5)
            self.horizontal_position.set(0.5)
            self.resize_image(event=None)

    def save_image(self, extension):
        if self.image_editor:
            save_path = filedialog.asksaveasfilename(
                defaultextension=extension,
                filetypes=[(f"{extension.upper()} files", f"*{extension}")],
            )
            if save_path:
                combined_image = Image.alpha_composite(
                    self.image_editor.get_edited_image().convert("RGBA"),
                    self.text_overlay.get_overlay(),
                )
                combined_image = combined_image.convert("RGB")
                combined_image.save(save_path)


App()

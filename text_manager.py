from PIL import Image, ImageDraw, ImageFont


class TextOverlay:
    def __init__(self, image_size):
        self.overlay = Image.new("RGBA", image_size, (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.overlay)

    def add_text(
        self,
        text,
        position,
        color,
        font_size,
        outline_width,
        vertical_pos,
        horizontal_pos,
    ):
        width, height = self.overlay.size
        font = ImageFont.truetype("arial.ttf", font_size)

        left, top, right, bottom = font.getbbox(text)
        text_width = right - left
        text_height = bottom - top

        if position == "top":
            y_position = height * 0.1
        elif position == "bottom":
            y_position = height * 0.9 - text_height
        else:  # center
            y_position = (height - text_height) / 2

        y_position += (vertical_pos - 0.5) * height
        x_position = (width - text_width) * horizontal_pos
        text_position = (x_position, y_position)

        if outline_width > 0:
            for offset_x in range(-outline_width, outline_width + 1):
                for offset_y in range(-outline_width, outline_width + 1):
                    self.draw.text(
                        (text_position[0] + offset_x,
                         text_position[1] + offset_y),
                        text,
                        font=font,
                        fill="black",
                    )

        self.draw.text(text_position, text, font=font, fill=color)

    def get_overlay(self):
        return self.overlay

    def clear(self):
        self.overlay = Image.new("RGBA", self.overlay.size, (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.overlay)

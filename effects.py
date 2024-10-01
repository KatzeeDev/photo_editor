from PIL import ImageOps, ImageFilter


def apply_effect(image, effect):
    if effect == "bw":
        return image.convert("L").convert("RGB")
    elif effect == "sepia":
        return sepia_effect(image)
    elif effect == "invert":
        return ImageOps.invert(image)
    elif effect == "blur":
        return image.filter(ImageFilter.BLUR)
    elif effect == "edge_enhance":
        return image.filter(ImageFilter.EDGE_ENHANCE)
    return image


def sepia_effect(image):
    width, height = image.size
    pixels = image.load()
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))
    return image

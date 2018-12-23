from PIL import Image


class ImageProcessor(object):

    def __init__(self, image_path, zoom, left=0, top=0, right=None, bottom=None):
        self.image = Image.open(image_path)
        self.zoom_value = zoom
        self.left = left
        self.top = top
        self.right, self.bottom = (right, bottom) if right and bottom else self.image.size

    def zoom(self, zoom_value=None):
        zoom_value = zoom_value or self.zoom_value
        if not zoom_value:
            return self.image.copy()
        image_size = tuple(map(lambda x: int(x / (2 ** zoom_value)), self.image.size))
        self.image = self.image.resize(image_size)

    def save(self, file_path):
        self.image.save(file_path)

    def crop(self, left=None, top=None, right=None, bottom=None):
        width, height = self.image.size
        left = min(left or self.left, width)
        right = min(right or self.right, width)
        top = min(top or self.top, height)
        bottom = min(bottom or self.bottom, height)
        return self.image.crop((left, top, right, bottom))

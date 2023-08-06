from io import BytesIO
from typing import Union

import pyqrcode
from PIL.PngImagePlugin import PngImageFile
from PIL import Image, ImageDraw, ImageFont


class QrCodeGen:
    def __init__(self):
        self._image_size = (512, 512)
        self.pil_save_options = {
            'quality': 50,
            'optimize': True
        }

    @property
    def width(self):
        return self._image_size[0]

    @property
    def height(self):
        return self._image_size[1]

    def set_size(self, size: tuple):
        if not isinstance(size[0], int) or not \
                isinstance(size[1], int):
            raise Exception("provide a tuple")
        self._image_size = size

    def create(self,
               text: str,
               color_from=(170, 43, 43),
               color_to=(230, 51, 51)) -> Image:
        """
        Create transparent QR code image.
        :param text: input text
        :param color_from: gradient from color
        :param color_to:  gradient to color
        :return:
        """
        created = pyqrcode.create(text, error='L')
        buffer = BytesIO()
        created.png(buffer, scale=14, quiet_zone=2)

        im = Image.open(buffer)
        im = im.convert("RGBA")
        im.thumbnail(self._image_size)

        im_data = im.getdata()

        # make black color transparent
        im_transparent = []
        for color_point in im_data:
            if sum(color_point[:3]) == 255 * 3:
                im_transparent.append(color_point)
            else:
                # get rid of the subtle grey borders
                alpha = 0 if color_from and color_to else 1
                im_transparent.append((0, 0, 0, alpha))
                continue

        if not color_from and not color_to:
            return im

        # turn QR into a gradient
        im.putdata(im_transparent)

        gradient = Image.new('RGBA', im.size, color=0)
        draw = ImageDraw.Draw(gradient)

        for i, color in enumerate(QrCodeGen.gradient_interpolate(color_from, color_to, im.width * 2)):
            draw.line([(i, 0), (0, i)], tuple(color), width=1)

        im_gradient = Image.alpha_composite(gradient, im)
        return im_gradient

    @staticmethod
    def gradient_interpolate(color_from, color_to, interval):
        det_co = [(t - f) / interval for f, t in zip(color_from, color_to)]
        for i in range(interval):
            yield [round(f + det * i) for f, det in zip(color_from, det_co)]
